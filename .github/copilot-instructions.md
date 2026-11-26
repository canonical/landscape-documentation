# Copilot instructions: Landscape documentation

The full guidance is in [`AGENTS.md`](../AGENTS.md). Read it before substantial
work. Some Copilot surfaces read only this file, so it repeats the core rules.

This repository holds Landscape's product documentation: MyST Markdown under
`docs/`, built with Sphinx (Canonical Sphinx Stack) and organized by Diátaxis.

- Change only what the task needs. Preserve existing SME wording. List other
  problems you notice instead of fixing them.
- Don't infer Landscape behavior from terminology, UI labels, or nearby prose.
  Don't invent commands, configuration keys, defaults, output, file paths, API
  behavior, navigation paths, prerequisites, or troubleshooting causes.
- State applicability where it matters: release; edition (Landscape SaaS,
  Managed Landscape, or self-hosted Landscape); install method; fresh install or
  upgrade; component (Landscape Server, Landscape Client, web portal, or API).
- Distinguish current behavior from planned or preview behavior. Report missing
  or contradictory information instead of resolving it with an assumption.
- Don't hand-edit generated content: `docs/_static/openapi.yaml`, regions
  between `BEGIN_TF_DOCS` and `END_TF_DOCS` markers, or `changelog-bot` regions.
  `AGENTS.md` lists where to make those changes.
- Use `{ref}` for internal links. When you move, rename, or delete a page, add a
  line to `docs/redirects.txt`.
- Open PRs against `main`.
- For any docs edit, run `make html` and `make spelling` from `docs/`. Also run
  `make linkcheck` when links change.
- Never put internal links or confidential details in public docs, commit
  messages, or PR text.

Task workflows for planning, updating, editing, testing, and reviewing docs are
in `.agents/skills/*/SKILL.md`.
