---
applyTo: "docs/**/*.md"
---

# Documentation authoring instructions

These rules apply when creating or editing Landscape documentation pages. See
[`AGENTS.md`](../../AGENTS.md) for repository-wide context and
[`docs/contributing.md`](../../docs/contributing.md) for contributor guidance.
Formatting and style rules enforced by CI (spelling, links, Markdown lint, Vale)
do not need to be restated here.

## Structure and Diátaxis

- Use MyST Markdown and the syntax already used in neighboring pages.
- Identify the intended Diátaxis type before restructuring a page:
  - Tutorials stay learning-oriented (a guided lesson).
  - How-to guides stay goal-oriented and practical (steps to achieve a task).
  - Reference pages stay factual, structured, and scannable.
  - Explanation pages stay focused on concepts and reasoning.
- Do not mix or invent Diátaxis labels such as "reference how-to".
- Keep the page opening consistent with the repository: a `(slug)=` anchor above
  the single `#` title, then a short introduction before the first `##` heading.
- Use `{ref}` for internal cross-references with descriptive link text, and
  `{toctree}` for navigation.

## Content accuracy

These rules govern content you write or change. Trust existing,
contributor-provided content by default; do not routinely re-verify or rewrite it.
Raise a concern only when you have a specific, strong reason to think something is
wrong, and then flag it for the contributor or a subject-matter expert rather than
silently removing or rewriting it.

- Do not invent missing procedural steps, commands, configuration, or expected
  output. Do not over-document obvious UI interactions.
- Include a prerequisite only when it must be true before the user can complete
  the task. Avoid unnecessary prerequisites.
- Check whether behavior differs by edition (SaaS, Managed, self-hosted), release,
  installation method, interface (web portal or API), or deployment type, and make
  the applicability explicit when it matters.
- Preserve technically meaningful distinctions between Landscape Server, Landscape
  Client, and the management interfaces.

## Language

- Use direct, precise, practical language. Prefer shorter sentences and explicit
  antecedents.
- Avoid marketing language, vague motivation, filler, and exaggerated benefit
  claims.
- Avoid idioms that are hard for non-native English readers or translators.
- Preserve good existing wording unless the requested change identifies a
  specific clarity or accuracy problem. Do not do synonym substitution for its own
  sake.

## Before finishing

- When a change affects navigation, parent landing pages, shared includes, or
  cross-references, check and update those too.
- When you move, rename, or delete a page, add a redirect in
  `docs/redirects.txt`.
- Run the relevant checks from `docs/` (for example `make spelling`,
  `make linkcheck`, `make html`).
