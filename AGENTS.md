# Landscape documentation – agent guide

Guidance for AI agents working in this repository. It complements the contributor
guide in [`docs/contributing.md`](docs/contributing.md); it doesn't replace review.

## Purpose, audience, and repository map

- Landscape is Canonical's systems management tool for Ubuntu desktops, servers,
  cloud instances, and IoT devices. Landscape Client runs on each managed machine
  and talks to Landscape Server, which is administered through the web portal or
  the API.
- This repository holds the product documentation only, not product source code.
- Readers are system administrators and technical operators, plus related
  security, IT, and compliance roles.
- Content is MyST Markdown under `docs/`, built with Sphinx (Canonical Sphinx
  Stack) and organized by [Diátaxis](https://diataxis.fr/):
  - `docs/tutorial.md`, `docs/how-to-guides/`, `docs/reference/` (including
    `docs/reference/release-notes/`), `docs/explanation/`.
  - `docs/what-is-landscape.md`: product overview and the edition definitions.
  - `docs/index.md` and each section's `index.md`: landing pages and `{toctree}`.
  - `docs/reuse/` and `**/_includes/`: snippets pulled in with `{include}`
    (excluded from the build as standalone pages). `docs/reuse/substitutions.yaml`
    defines MyST substitutions.
  - `docs/redirects.txt`: redirects for moved, renamed, or deleted pages.
  - `docs/.custom_wordlist.txt`: spelling exceptions.
  - `docs/conf.py`: Sphinx configuration. `docs/_dev/`: Sphinx Stack tooling.
  - `docs/scripts/`: helper scripts. `.github/workflows/`: CI and sync bots.

## Build and checks

The first build creates `docs/.venv` and installs dependencies. Prerequisites:
`make`, `python3`, `python3-venv`, `python3-pip`.

Targets: `make install`, `make html` (fails on warnings), `make run` (build,
watch, and serve at `http://127.0.0.1:8000`), `make spelling`, `make linkcheck`,
`make vale`, `make woke`, `make lint-md`, `make pa11y`.

Run them from the repository root or from `docs/`. They're equivalent except for
`html` and `run`: from the root, these first run `docs/scripts/apply_overlay.py`,
which merges the Debarchive OpenAPI examples into
`docs/_static/openapi-with-examples.yaml` (as Read the Docs does). From `docs/`
they skip that step, so the Debarchive API reference can be stale locally.

Check policy (run what applies, nothing more):

- Any docs edit: `make html` and `make spelling`.
- Links added or changed: also `make linkcheck`.
- Overlay or OpenAPI changes: also, from the root,
  `docs/.venv/bin/python docs/scripts/apply_overlay.py`.
- Don't run `vale`, `woke`, `pa11y`, or `lint-md` unless asked or CI reports a
  failure.

`make html` doesn't catch broken Markdown-style internal links (`[text](#label)`,
`[text](page.md)`): `docs/conf.py` suppresses `myst.xref_missing` for
terraform-docs output, and `make linkcheck` checks only external URLs. Prefer
`{ref}`, which still fails the build. If you add a Markdown-style internal link,
confirm that its target exists.

## Scope and proportionality

- Change only what the task needs. List other observations at the end of your
  response instead of fixing them.
- Ask only questions whose answer changes the result. Batch them and keep them
  precise.
- Match effort to the change. A small, correct change gets a short answer.
- Never run product installs or product commands on the user's machine. Test
  procedures only on request, in a disposable environment (see the
  `test-procedure` skill).

## Accuracy and applicability

- Trust existing, contributor-provided content by default; don't routinely
  re-verify or rewrite it. Raise a concern only when you have a specific reason,
  and flag it for the contributor or a subject-matter expert (SME) rather than
  silently changing it.
- Don't infer Landscape behavior from terminology, UI labels, or nearby prose.
  Verify claims you write against the sources below.
- Don't invent commands, configuration keys, defaults, output, file paths, API
  behavior, navigation paths, prerequisites, limitations, or troubleshooting
  causes. In examples, use real content from this repository or neutral
  placeholders.
- Distinguish current availability from planned, preview, or future behavior.
- Preserve uncertainty. Report missing or contradictory information; don't
  resolve it with an assumption or a silent rewrite. Prefer exact, limited claims.

When a claim depends on applicability, check each of these and state the ones
that matter:

- **Release**: which Landscape release or releases.
- **Edition**: Landscape SaaS, Managed Landscape, or self-hosted Landscape (terms
  as in `docs/what-is-landscape.md`).
- **Install method**: Quickstart, manual, Juju or Terraform, cloud images.
- **Path**: fresh install, or upgrade or migration.
- **Component**: Landscape Server, Landscape Client, charms, snaps, web portal,
  REST API, or legacy API.

## Sources and access

Prefer, roughly in this order: product source, supplied design documents, current
docs, official Canonical or Ubuntu docs, official upstream docs. Public sources:

- This repository and its Git history.
- Public Canonical repositories, such as `canonical/landscape-ui`,
  `canonical/landscape-client`, `canonical/landscape-server-operator`, and
  `canonical/landscape-scripts`.
- Charmhub and `snap info` for charm and snap channels.
- Launchpad PPA publishing history for package versions.
- Discourse history of the pre-migration docs.

Rules:

- Prefer release tags over branch tips when checking behavior for a release.
- Some product source repositories are internal. If you can't access a source,
  say what you couldn't verify and ask. Don't guess.
- Never put internal links, internal discussion, or confidential details in
  public docs, commit messages, or PR text. Cite public changelog or release-note
  entries instead.
- Existing docs aren't authoritative when the task is to correct them.

## Generated and synced content

| What | Source | Edit instead |
| --- | --- | --- |
| `docs/_static/openapi.yaml` (Debarchive API) | Generated with `protoc-gen-openapi` from the Landscape proto definitions; updated by "update openapi.yaml from landscape-proto" PRs | Don't edit by hand. |
| Debarchive API examples | `docs/_static/openapi-overlay.yaml`, merged by `docs/scripts/apply_overlay.py` | The overlay. Targets must be literal JSONPaths (no `*` or `[?`); then run the overlay script. |
| Regions between `<!-- BEGIN_TF_DOCS -->` and `<!-- END_TF_DOCS -->` in `docs/reference/charm/terraform-*.md` | `terraform-docs`, run by `.github/workflows/update-terraform-docs.yml` against `canonical/landscape-server-operator` | Don't edit by hand. Fix the upstream Terraform module. Prose outside the markers is editable. |
| Regions between `<!-- changelog-bot:*:start -->` and `<!-- changelog-bot:*:end -->` in release notes | Changelog bots, which keep the draft release notes updated until release | Don't edit by hand. Edit outside the markers. |

`docs/_static/openapi-with-examples.yaml` is build output and is gitignored.

## Writing conventions

Follow neighboring pages for headings, code blocks, directives, admonitions,
tables, images, and version tabs. If you have access to the Landscape team's
internal language and style guide, follow it. Otherwise follow neighboring pages.

- **Page opening**: MyST `html_meta` `description` frontmatter, a `(label)=`
  anchor directly above the single `#` title, then a short introduction before
  the first `##` heading.
- **Links and navigation**: `{ref}` with descriptive link text for internal
  links; `{toctree}` for navigation. Keep toctrees and visible link groups on
  landing pages consistent. When a change affects navigation, landing pages,
  includes, or cross-references, update those too.
- **Reuse**: shared text goes in `docs/reuse/` with `{include}`; shared values go
  in `docs/reuse/substitutions.yaml`. A snippet edit affects every page that
  includes it.
- **Moves**: when you move, rename, or delete a page, add a line to
  `docs/redirects.txt` (`old/path/ new/path/`, trailing slashes, no extension).
  Keep or alias anchors that other pages use.
- **Diátaxis**: identify the page type before restructuring. Tutorials teach;
  how-to guides get a task done; reference is factual and scannable; explanation
  covers concepts. Don't mix or invent types.
- **Prerequisites**: include one only when it must be true before the reader can
  complete the task.
- **UI docs**: keep them lightweight. Don't narrate interactions the interface
  already makes obvious.
- **Wording**: use direct, precise language and shorter sentences. Avoid
  marketing language, filler, and idioms. Preserve good SME wording; don't
  substitute synonyms or polish prose that isn't part of the task.
- **Landing pages**: a brief orientation, then links grouped by a structure that
  fits the content, keeping any logical progression, with short descriptions
  where they help readers choose. Keep small landing pages small; don't repeat
  each page's introduction.
- **Terminology**: "Managed Landscape" (not "Landscape Managed"); "REST API" and
  "legacy API"; "web portal" and "legacy web portal"; "instances" for managed
  machines in prose, keeping "computers" where it's a literal UI label or API
  name.

Release notes:

- Follow the existing page structure. State the release at page level, and name
  the edition or component only where it differs.
- Keep entry categories (added, changed, fixed, deprecated, removed, known
  issues). Don't move entries between categories without evidence.
- Describe the user-visible effect. Don't invent upgrade steps, compatibility
  implications, breaking changes, or security impact.
- Never add notes for a later release than the one being documented.

## Versions

Follow `docs/contributing.md` for which branch to target.

## Skills

Task-specific workflows live in `.agents/skills/`. If your agent doesn't load
skills automatically, read the `SKILL.md` file before starting that kind of task.

| Skill | Purpose | Path |
| --- | --- | --- |
| `plan-docs-for-change` | Decide what docs a product change needs, without editing | `.agents/skills/plan-docs-for-change/SKILL.md` |
| `update-docs` | Make a defined docs change or carry out an approved plan | `.agents/skills/update-docs/SKILL.md` |
| `edit-technical-draft` | Editorial pass on an engineer's technically correct draft | `.agents/skills/edit-technical-draft/SKILL.md` |
| `test-procedure` | Check whether a documented procedure works | `.agents/skills/test-procedure/SKILL.md` |
| `review-docs-change` | Review a docs PR or diff | `.agents/skills/review-docs-change/SKILL.md` |

`docs/scripts/find_references.py` reports labels, inbound references, includes,
toctree entries, redirects, substitutions, and generated markers for a page.
Run it before renaming, moving, or deleting a page, or changing an anchor,
include, or snippet.
