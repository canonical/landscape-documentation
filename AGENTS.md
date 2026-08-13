# Landscape documentation – agent guide

This file orients AI coding agents working in this repository. It is context to
improve agent-generated changes, not an enforcement mechanism and not a
replacement for the contributor guide in [`docs/contributing.md`](docs/contributing.md).
Support for `AGENTS.md` and GitHub instruction files varies by tool, so keep the
most important rules here durable and concise.

## Repository purpose

- Landscape is Canonical's systems management tool for managing and monitoring
  Ubuntu deployments (desktops, servers, cloud instances, and IoT devices).
- This repository contains the Landscape product documentation. It does not
  contain Landscape's source code.
- The main audience is system administrators and technical operators who deploy and
  run Landscape, along with related security, IT, and compliance roles.
- Landscape uses a client–server model: an agent (Landscape Client) runs on each
  managed machine and communicates with Landscape Server, which is administered
  through the web portal or the API.
- The documentation covers different Landscape editions (SaaS, Managed, and
  self-hosted), different interfaces (web portal and API), different installation
  methods (for example Quickstart, manual, Juju/charm), and multiple product
  releases. Applicability often differs between these.

## Repository structure

Documentation source lives under `docs/`. Content follows the
[Diátaxis](https://diataxis.fr/) framework with some additions:

- `docs/tutorial.md` – learning-oriented getting-started tutorial.
- `docs/how-to-guides/` – task-oriented guides, grouped by topic.
- `docs/reference/` – technical reference (API, configuration, logs, database,
  networking, terms, and `docs/reference/release-notes/`).
- `docs/explanation/` – concept and background material.
- `docs/what-is-landscape.md` – product overview, including the edition
  definitions.
- `docs/contributing.md` – contributor documentation.

Supporting files:

- `docs/conf.py` – Sphinx configuration.
- `docs/index.md` and the `index.md` file at the root of each section – landing
  pages and `toctree` navigation.
- `docs/reuse/` – reusable snippets and `substitutions.yaml` (MyST
  substitutions).
- `docs/redirects.txt` – redirects for moved, renamed, or deleted pages.
- `docs/.custom_wordlist.txt` – spelling exceptions for the Vale spell check.
- `docs/_dev/` – Canonical Sphinx Stack tooling and check configuration.

## Build and validation

Run all commands from the `docs/` directory (the top-level `Makefile` forwards
targets there, but running from `docs/` is the reliable path). The first build
creates a Python virtual environment and installs dependencies.

```bash
make install     # set up the virtualenv and dependencies
make html        # build the docs (fails on Sphinx warnings)
make run         # build, watch, and serve at http://127.0.0.1:8000
make spelling    # spell check (Vale; exceptions in .custom_wordlist.txt)
make linkcheck   # verify links
make lint-md     # Markdown lint (pymarkdown)
make vale        # Canonical style-guide check
make woke        # inclusive-language check
```

Prerequisites for a local build: `make`, `python3`, `python3-venv`, and
`python3-pip`.

`make spelling` and `make linkcheck` are the two checks contributors are expected
to pass, and they also run in CI. Run the checks relevant to your change; you do
not need to restate their mechanical rules in prose.

## Authoring format and structure

- Pages are Markdown (`.md`) using MyST syntax.
- Follow the existing Diátaxis organization. Keep tutorials learning-oriented and
  keep how-to guides task-oriented; do not turn a how-to guide into a tutorial.
- Each page starts with a reference anchor `(slug)=` immediately above the single
  `#` H1, followed by a short introduction before the first `##` heading.
- Frontmatter uses a MyST `html_meta` `description`, as on existing pages.
- Use `{ref}` for internal cross-references and descriptive link text. Use
  `{toctree}` for navigation. Reuse shared content with `{include}` and MyST
  substitutions from `docs/reuse/`.
- Follow the conventions already visible in neighboring pages for headings,
  anchors, code blocks, directives, admonitions, tables, images, and UI
  terminology.
- Keep UI documentation proportionate and lightweight. Do not describe every 
  obvious interaction that the interface already makes clear.
- Preserve good existing wording from subject-matter experts. Do not perform
  broad cosmetic rewriting or unsolicited prose polishing.
- When you move, rename, or delete a page, add a redirect to `docs/redirects.txt`
  (the site uses the `dirhtml` builder; include trailing slashes and no file
  extension).

## Landscape-specific accuracy rules

Accuracy matters more than completeness. Treat these as the highest-value rules:

- Do not infer Landscape behavior from terminology, nearby prose, or UI labels
  alone. Verify technical claims against authoritative sources for the task.
- Do not invent commands, configuration keys, default values, output, file paths,
  API behavior, navigation paths, prerequisites, limitations, or troubleshooting
  causes.
- Distinguish between the editions when applicability matters: Landscape SaaS,
  Landscape Managed, and self-hosted Landscape. Some features are not available in
  every edition. Do not generalize behavior across editions without evidence.
- Distinguish Landscape Server, Landscape Client, and the interfaces used to
  manage Landscape (web portal and API).
- Identify version-specific behavior where relevant. Do not generalize current
  behavior to every supported Landscape release, and do not describe planned,
  preview, or unreleased behavior as currently available unless the task and
  sources establish that context.
- Preserve uncertainty when sources are incomplete or contradictory. Report
  missing information rather than resolving it with an unsupported assumption.
- Prefer exact, limited claims over broad claims that merely sound complete.
- Use the edition and product terminology already used in the repository (see
  `docs/what-is-landscape.md`). Do not introduce a new product taxonomy.

## Editing scope

- Make focused changes that address the requested task. Avoid unrelated cleanup.
- Avoid synonym substitution that does not improve accuracy or clarity, and
  preserve technically precise language.
- When a change affects navigation, terminology, version applicability, or shared
  content, check the surrounding pages, parent landing pages, and includes.
- Do not silently resolve an apparent product inconsistency by rewriting the
  documentation. Flag inconsistencies that need product or SME judgment.

## Sources and verification

Source availability depends on the task. When sources are available, prefer, in
roughly this order:

- Landscape source repositories.
- Supplied design or engineering documents for the task.
- Existing current Landscape documentation.
- Official Canonical or Ubuntu documentation.
- Official upstream documentation.

Existing public documentation is a useful reference, but it is not automatically
authoritative when the task is specifically to correct it. Do not fabricate
support for a claim; if you cannot verify something, say so.
