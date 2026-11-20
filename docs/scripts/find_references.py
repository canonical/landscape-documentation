#!/usr/bin/env python3
"""Report what depends on a documentation page or snippet, and what it uses.

Run it before renaming, moving, or deleting a page, or changing an anchor,
include, or snippet. Standard library only.

Usage:
  python3 docs/scripts/find_references.py PATH_OR_LABEL [PATH_OR_LABEL ...] [--json]

Each argument is a Markdown file under docs/ (relative to the current
directory, the repository root, or docs/) or a `(label)=` reference label. A
label is reported as the file that defines it.

For each file, the report lists:
  * labels defined in the file (`(label)=`);
  * inbound uses of those labels: {ref}`label`, {ref}`text <label>`, and
    MyST links `[text](#label)` or `[text](label)`;
  * inbound {doc} roles and Markdown links to the file;
  * {include} directives that include the file, and files the file includes;
  * {toctree} entries that list the file (including :glob: patterns);
  * lines in docs/redirects.txt that mention its path;
  * substitution keys it uses (`{{ key }}`) and whether
    docs/reuse/substitutions.yaml defines them;
  * generated-region markers it contains (terraform-docs, changelog bots).

Exit status: 0 on success, 1 on a parse error, 2 on a usage error (unknown
path or label). Nothing is reported after an error.
"""

import argparse
import json
import posixpath
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
REPO = DOCS.parent
REDIRECTS = DOCS / "redirects.txt"
SUBSTITUTIONS = DOCS / "reuse" / "substitutions.yaml"
SKIP_DIRS = {"_build", ".venv", "node_modules"}

FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>`{3,}|~{3,})\s*(?P<info>.*?)\s*$")
DIRECTIVE_RE = re.compile(r"^\{(?P<name>[\w:-]+)\}\s*(?P<arg>.*)$")
LABEL_DEF_RE = re.compile(r"^\s*\((?P<label>[^()\s]+)\)=\s*$")
REF_RE = re.compile(r"\{ref\}`(?P<body>[^`]+)`")
DOC_RE = re.compile(r"\{doc\}`(?P<body>[^`]+)`")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
SUBST_RE = re.compile(r"\{\{\s*(?P<key>[A-Za-z_][\w.-]*)\s*\}\}")
MARKER_RE = re.compile(
    r"<!--\s*(?P<marker>(?:BEGIN|END)_[A-Z_]+|changelog-bot:[\w.-]+:(?:start|end))\s*-->"
)
URL_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
CODE_DIRECTIVES = {"code", "code-block", "code-cell", "sourcecode", "mermaid"}


class ParseError(Exception):
    pass


@dataclass
class Use:
    file: str
    line: int
    kind: str
    target: str
    text: str


@dataclass
class Page:
    path: Path
    rel: str  # path relative to docs/, e.g. "reuse/x.md"
    docname: str  # rel without ".md"
    labels: list = field(default_factory=list)  # (label, line)
    refs: list = field(default_factory=list)  # Use(kind="ref"|"link-label")
    links: list = field(default_factory=list)  # Use(kind="doc"|"link"), target=docname
    includes: list = field(default_factory=list)  # Use(kind="include"), target=rel
    toctree: list = field(default_factory=list)  # (entry, line, glob)
    substitutions: list = field(default_factory=list)  # (key, line)
    markers: list = field(default_factory=list)  # (marker, line)


def rel_to_docs(path: Path) -> str:
    return path.resolve().relative_to(DOCS).as_posix()


def resolve_doc_target(target: str, page: Page) -> str:
    """Return a docs-relative POSIX path (no normalization of extension)."""
    if target.startswith("/"):
        joined = target.lstrip("/")
    else:
        joined = posixpath.join(posixpath.dirname(page.rel), target)
    return posixpath.normpath(joined)


def strip_md(path: str) -> str:
    return path[:-3] if path.endswith(".md") else path


BACKTICKS_RE = re.compile(r"`+")
ROLE_PREFIX_RE = re.compile(r"\{[\w:-]+\}$")


def blank_code_spans(line: str) -> str:
    """Replace inline code spans with spaces; keep role bodies such as {ref}`x`.

    MyST doesn't process roles, links, or substitutions inside inline code, so
    text there is literal and must not be reported as a reference.
    """
    out, pos = [], 0
    while True:
        opener = BACKTICKS_RE.search(line, pos)
        if not opener:
            break
        ticks = opener.group(0)
        closer = re.compile(r"(?<!`)" + ticks + r"(?!`)").search(line, opener.end())
        if not closer:
            break  # an unmatched backtick run is literal text
        if ROLE_PREFIX_RE.search(line, 0, opener.start()):
            out.append(line[pos:closer.end()])
        else:
            out.append(line[pos:opener.start()] + " " * (closer.end() - opener.start()))
        pos = closer.end()
    out.append(line[pos:])
    return "".join(out)


def sphinx_glob_match(name: str, pattern: str) -> bool:
    """Match a docname as Sphinx toctree :glob: does: * and ? don't cross '/'."""
    regex, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            regex.append(".*")
            i += 2
            continue
        char = pattern[i]
        if char == "*":
            regex.append("[^/]*")
        elif char == "?":
            regex.append("[^/]")
        elif char == "[":
            end = pattern.find("]", i + 1)
            if end == -1:
                regex.append(re.escape(char))
            else:
                body = pattern[i + 1:end]
                if body.startswith("!"):
                    body = "^" + body[1:]
                regex.append("[" + body.replace("\\", "\\\\") + "]")
                i = end
        else:
            regex.append(re.escape(char))
        i += 1
    return re.fullmatch("".join(regex), name) is not None


def scan_inline(page: Page, lineno: int, line: str) -> None:
    line = blank_code_spans(line)
    for match in REF_RE.finditer(line):
        body = match.group("body").strip()
        angle = re.search(r"<([^<>]+)>\s*$", body)
        label = angle.group(1) if angle else body
        page.refs.append(Use(page.rel, lineno, "ref", label.strip(), match.group(0)))
    for match in DOC_RE.finditer(line):
        body = match.group("body").strip()
        angle = re.search(r"<([^<>]+)>\s*$", body)
        target = strip_md(resolve_doc_target(angle.group(1) if angle else body, page))
        page.links.append(Use(page.rel, lineno, "doc", target, match.group(0)))
    for match in LINK_RE.finditer(line):
        target = match.group("target").strip("<>")
        if URL_SCHEME_RE.match(target):
            continue
        if target.startswith("#"):
            page.refs.append(Use(page.rel, lineno, "link-label", target[1:], match.group(0)))
            continue
        path_part, _, _anchor = target.partition("#")
        if not path_part:
            continue
        resolved = resolve_doc_target(path_part, page)
        if resolved.endswith(".md"):
            page.links.append(Use(page.rel, lineno, "link", strip_md(resolved), match.group(0)))
        elif "." not in posixpath.basename(path_part):
            # Extensionless target: MyST resolves it as a doc or a label.
            page.links.append(Use(page.rel, lineno, "link", resolved, match.group(0)))
            if "/" not in path_part:
                page.refs.append(Use(page.rel, lineno, "link-label", path_part, match.group(0)))
    for match in SUBST_RE.finditer(line):
        page.substitutions.append((match.group("key"), lineno))
    for match in MARKER_RE.finditer(line):
        page.markers.append((match.group("marker"), lineno))


def parse_page(path: Path) -> Page:
    rel = rel_to_docs(path)
    page = Page(path=path, rel=rel, docname=strip_md(rel))
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ParseError(f"{rel}: cannot read: {exc}") from exc

    # Stack of open fences: dicts with char, length, kind, name, line, glob.
    stack = []
    in_frontmatter = bool(lines) and lines[0].strip() == "---"
    for lineno, line in enumerate(lines, start=1):
        if in_frontmatter:
            if lineno > 1 and line.strip() == "---":
                in_frontmatter = False
            continue

        fence = FENCE_RE.match(line)
        top = stack[-1] if stack else None
        if fence:
            char, length, info = fence.group("fence")[0], len(fence.group("fence")), fence.group("info")
            closes = (
                top is not None
                and not info
                and char == top["char"]
                and length >= top["length"]
            )
            if closes:
                stack.pop()
                continue
            if top is None or top["kind"] == "directive":
                directive = DIRECTIVE_RE.match(info)
                name = directive.group("name") if directive else None
                if name and name not in CODE_DIRECTIVES:
                    entry = {"char": char, "length": length, "kind": "directive",
                             "name": name, "line": lineno, "glob": False}
                    stack.append(entry)
                    if name == "include":
                        arg = directive.group("arg").strip()
                        if not arg:
                            raise ParseError(f"{rel}:{lineno}: include directive without a path")
                        target = resolve_doc_target(arg, page)
                        page.includes.append(Use(rel, lineno, "include", target, line.strip()))
                    continue
                stack.append({"char": char, "length": length, "kind": "code",
                              "name": name, "line": lineno, "glob": False})
                continue
            # A fence line inside a code block that doesn't close it is content.
            continue

        if top is not None and top["kind"] == "code":
            continue

        if top is not None and top["name"] == "toctree":
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(":"):
                if stripped.split()[0] == ":glob:":
                    top["glob"] = True
                continue
            angle = re.search(r"<([^<>]+)>\s*$", stripped)
            entry = angle.group(1) if angle else stripped
            if entry == "self" or URL_SCHEME_RE.match(entry):
                continue
            page.toctree.append((strip_md(resolve_doc_target(entry, page)), lineno, top["glob"]))
            continue

        label = LABEL_DEF_RE.match(line)
        if label:
            page.labels.append((label.group("label"), lineno))
            continue
        scan_inline(page, lineno, line)

    # Fences still open here close at the end of the document, as in CommonMark.
    return page


def iter_markdown_files():
    for path in sorted(DOCS.rglob("*.md")):
        parts = path.relative_to(DOCS).parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        yield path


def load_substitution_keys() -> set:
    """Read top-level keys of the flat substitutions.yaml without PyYAML."""
    if not SUBSTITUTIONS.exists():
        raise ParseError(f"{rel_to_docs(SUBSTITUTIONS)} not found")
    keys = set()
    for lineno, line in enumerate(SUBSTITUTIONS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        match = re.match(r"^([A-Za-z_][\w.-]*)\s*:", line)
        if not match:
            raise ParseError(f"{rel_to_docs(SUBSTITUTIONS)}:{lineno}: unexpected line: {line!r}")
        keys.add(match.group(1))
    return keys


def load_redirects() -> list:
    if not REDIRECTS.exists():
        raise ParseError(f"{rel_to_docs(REDIRECTS)} not found")
    result = []
    for lineno, line in enumerate(REDIRECTS.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) != 2:
            raise ParseError(f"{rel_to_docs(REDIRECTS)}:{lineno}: expected two paths: {line!r}")
        result.append((lineno, stripped, [p.strip("/") for p in parts]))
    return result


def url_path(docname: str) -> str:
    """dirhtml URL path for a docname, without slashes."""
    if docname == "index":
        return ""
    if docname.endswith("/index"):
        return docname[: -len("/index")]
    return docname


def resolve_argument(arg: str, pages: dict) -> tuple:
    """Return (rel, queried_label or None)."""
    for base in (Path.cwd(), REPO, DOCS):
        candidate = (base / arg).resolve()
        if candidate.is_file():
            try:
                rel = rel_to_docs(candidate)
            except ValueError:
                raise SystemExit(f"error: {arg} is not under {DOCS}") from None
            if rel not in pages:
                raise SystemExit(f"error: {arg} is not a Markdown file scanned under docs/")
            return rel, None
    owners = [p.rel for p in pages.values() for label, _ in p.labels if label == arg]
    if not owners:
        raise SystemExit(f"error: {arg!r} is neither a file under docs/ nor a defined label")
    if len(owners) > 1:
        print(f"warning: label {arg!r} is defined in several files: {', '.join(owners)}",
              file=sys.stderr)
    return owners[0], arg


def build_report(rel: str, queried_label, pages: dict, subst_keys: set, redirects: list) -> dict:
    page = pages[rel]
    labels = {label for label, _ in page.labels}
    others = [p for p in pages.values()]

    def use_dict(use):
        return {"file": use.file, "line": use.line, "kind": use.kind,
                "target": use.target, "text": use.text}

    inbound_refs = [use_dict(u) for p in others for u in p.refs if u.target in labels]
    inbound_links = [use_dict(u) for p in others for u in p.links
                     if u.target == page.docname and p.rel != rel]
    included_by = [use_dict(u) for p in others for u in p.includes if u.target == rel]

    toctree = []
    for p in others:
        for entry, line, glob in p.toctree:
            if entry == page.docname or (
                glob and any(c in entry for c in "*?[") and sphinx_glob_match(page.docname, entry)
            ):
                toctree.append({"file": p.rel, "line": line, "entry": entry})

    page_url = url_path(page.docname)
    redirect_lines = [
        {"line": lineno, "text": text}
        for lineno, text, parts in redirects
        if page_url and page_url in parts
    ]

    includes = [{"line": u.line, "target": u.target,
                 "exists": (DOCS / u.target).is_file()} for u in page.includes]
    substitutions = [{"key": key, "line": line, "defined": key in subst_keys}
                     for key, line in page.substitutions]

    return {
        "file": f"docs/{rel}",
        "queried_label": queried_label,
        "labels_defined": [{"label": label, "line": line} for label, line in page.labels],
        "inbound_label_refs": inbound_refs,
        "inbound_doc_links": inbound_links,
        "included_by": included_by,
        "includes": includes,
        "toctree_entries": toctree,
        "redirects": redirect_lines,
        "substitutions": substitutions,
        "generated_markers": [{"marker": m, "line": line} for m, line in page.markers],
    }


def print_report(report: dict) -> None:
    title = report["file"]
    if report["queried_label"]:
        title += f"  (defines label {report['queried_label']})"
    print(f"== {title}")

    def section(name, items, fmt):
        print(f"{name}:")
        if not items:
            print("  none")
        for item in items:
            print(f"  {fmt(item)}")

    section("Labels defined", report["labels_defined"], lambda i: f"{i['label']}  (line {i['line']})")
    section("Inbound label references", report["inbound_label_refs"],
            lambda i: f"docs/{i['file']}:{i['line']}  {i['kind']} -> {i['target']}  {i['text']}")
    section("Inbound doc links", report["inbound_doc_links"],
            lambda i: f"docs/{i['file']}:{i['line']}  {i['kind']}  {i['text']}")
    section("Included by", report["included_by"],
            lambda i: f"docs/{i['file']}:{i['line']}  {i['text']}")
    section("Includes", report["includes"],
            lambda i: f"docs/{i['target']}  (line {i['line']})" + ("" if i["exists"] else "  MISSING"))
    section("Toctree entries", report["toctree_entries"],
            lambda i: f"docs/{i['file']}:{i['line']}  {i['entry']}")
    section("Redirects (docs/redirects.txt)", report["redirects"],
            lambda i: f"line {i['line']}: {i['text']}")
    section("Substitutions used", report["substitutions"],
            lambda i: f"{i['key']}  (line {i['line']})" + ("" if i["defined"] else "  UNDEFINED"))
    section("Generated-region markers", report["generated_markers"],
            lambda i: f"{i['marker']}  (line {i['line']})")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("targets", nargs="+", help="file under docs/ or a reference label")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = parser.parse_args()

    try:
        pages = {}
        for path in iter_markdown_files():
            page = parse_page(path)
            pages[page.rel] = page
        subst_keys = load_substitution_keys()
        redirects = load_redirects()
    except ParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        resolved = [resolve_argument(arg, pages) for arg in args.targets]
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2

    reports = [build_report(rel, label, pages, subst_keys, redirects) for rel, label in resolved]
    if args.json:
        print(json.dumps(reports, indent=2))
    else:
        for report in reports:
            print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
