---
applyTo: "docs/**/index.md"
---

# Landing page instructions

These rules apply to section landing pages, which in this repository are the
`index.md` files at the root of each Diátaxis section and each subsection. A
landing page orients readers and guides them into the section's content through
grouped links with explanatory text. General page rules in
[`documentation.instructions.md`](documentation.instructions.md) also apply.

## What a landing page should do

- Start with a brief orientation: what this section contains and its purpose.
- Group linked pages by a coherent organization — user goals, product areas,
  interfaces, workflows, or lifecycle stages — whichever best reflects the
  content. Do not force a lifecycle grouping when another structure fits better.
- Add short explanatory text where it materially helps a reader choose a page.
  Keep group and page descriptions concrete.
- Avoid unexplained flat lists of links with no context.
- Preserve a logical progression where one exists.
- Reference related explanation material when it helps users choose an approach,
  not as a mandatory checkbox.

## Keep it proportionate

- Keep small landing pages lightweight. Do not manufacture groups or prose just to
  fill a template.
- Do not repeat a linked page's full introduction on the landing page.
- Do not make landing pages marketing-oriented.

## Navigation consistency

- This repository builds navigation with Sphinx `{toctree}` directives. Keep the
  `toctree` entries and any visible link groupings consistent with each other.
- Some Landscape areas cross documentation types or product boundaries; group them
  where they help the reader most, and keep cross-references accurate.
