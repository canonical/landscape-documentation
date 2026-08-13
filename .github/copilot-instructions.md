# GitHub Copilot instructions – Landscape documentation

Consult [`AGENTS.md`](../AGENTS.md) before substantial work. It holds the full
repository guidance; this file summarizes the highest-impact rules because not
every Copilot surface loads `AGENTS.md`.

This repository is Landscape's product documentation, written in MyST Markdown
under `docs/` and built with Sphinx (Canonical Sphinx Stack), organized by
Diátaxis.

Core rules:

- Make focused changes that address the requested task. Avoid unrelated cleanup
  and cosmetic rewording; preserve technically precise, existing SME wording.
- Do not infer Landscape behavior from terminology, UI labels, or nearby prose.
  Verify technical claims against authoritative sources for the task.
- Do not invent commands, configuration, defaults, output, file paths, API
  behavior, UI navigation paths, prerequisites, or troubleshooting causes.
- Check edition and version applicability when it matters. Distinguish Landscape
  SaaS, Landscape Managed, and self-hosted Landscape, and distinguish Landscape
  Server, Landscape Client, the web portal, and the API. Do not generalize a
  feature across editions or releases without evidence.
- Distinguish current availability from planned, preview, or future behavior.
- Preserve uncertainty. Report missing or contradictory information instead of
  resolving it with an assumption.
- Run the checks relevant to your change from `docs/` (for example
  `make spelling`, `make linkcheck`, `make html`). Do not restate the mechanical
  formatting rules already enforced in CI.

Path-specific guidance lives in `.github/instructions/`.
