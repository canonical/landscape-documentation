---
applyTo: "docs/reference/release-notes/**/*.md"
---

# Release notes instructions

These rules apply to Landscape release notes. Follow the structure and style of
the existing release-note pages; do not impose a new format. General page rules in
[`documentation.instructions.md`](documentation.instructions.md) also apply.

The rules below govern content you write or change. Trust existing,
contributor-provided content by default — contributors are typically engineers
with direct knowledge of the change. Do not routinely re-verify or rewrite
existing entries. Raise a concern only when you have a specific, strong reason to
think something is wrong, and then flag it for the contributor or a subject-matter
expert rather than silently removing or downgrading it.

## Preserve meaning and category

- Keep the distinction between added, changed, fixed, deprecated, removed, and
  known behavior. Do not move an entry between these categories without evidence.
- Describe the user-visible effect of a change rather than only restating
  implementation detail, but do not invent user benefits.
- Do not turn internal engineering notes into unsupported public claims.
- Preserve exact technical terminology when it affects meaning.

## Applicability

When you write or edit an entry, make its applicability explicit:

- State the Landscape release the entry applies to.
- State whether it applies to self-hosted, SaaS, or Managed, and to Landscape
  Server, Landscape Client, or another specific component. Do not imply that all
  editions receive a feature at the same time.
- Distinguish current availability from planned, preview, experimental, or future
  behavior.

## Do not overstate

- Do not invent migration requirements, compatibility implications, upgrade steps,
  or security impact.
- Do not call something a breaking change unless the source establishes that.
- Do not describe a fix as comprehensive when the source only establishes a
  narrower result.
- Keep wording factual, concise, and non-promotional. Preserve unresolved
  limitations and known issues.
- If version or applicability information is missing, ask for it or report it
  rather than guessing.
