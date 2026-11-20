---
name: edit-technical-draft
description: "Do an editorial pass on a technically correct Landscape docs draft written by an engineer or SME. Use when asked to edit, tidy, or restructure a draft page or PR so readers can follow it, while keeping its technical content. Edits structure, placement, conditions, headings, and terminology; never changes commands, values, or technical claims. Not for: verifying technical behavior or testing procedures (use test-procedure), reviewing a PR without editing it (use review-docs-change), or writing new content from a product change (use update-docs)."
---

# Edit a technical draft

Make an expert's draft easy to follow without changing what it says
technically. Shared rules are in `AGENTS.md`; this skill doesn't repeat them.

## Inputs

- The draft: a PR, branch, or file.
- What the draft is for: its issue, PR description, or the author's summary.
- Optional: which parts the author is unsure about.

## Steps

1. **Read the whole draft and its neighbors first.** Identify the reader, the
   task, and the paths the draft covers. Read the pages it sits next to and
   the pages that cover the same task.
2. **Check placement and doc type before line edits.** Does this belong in an
   existing guide, as a step, a section, or a troubleshooting entry? For
   example, in canonical/landscape-documentation#371 a separate page about
   scripted WSL deployments raised the question of whether it belonged in the
   existing WSL host registration guide.
   Does the content match its Diátaxis type?
3. **Decide the scope.** Light restructuring is fine: moving prerequisites up,
   reordering sections, splitting a conditional step into its own subsection,
   fixing headings. Anything more (moving content to another page, merging or
   splitting pages, changing the doc type) needs agreement first: propose it and
   stop.
4. **Edit for these problems:**
   - **Late prerequisites**: requirements that appear after the reader needs
     them. Move them before the first step that depends on them.
   - **Paths hard to tell apart**: deployment methods, editions, or fresh install
     versus upgrade or migration mixed in one sequence. Separate them the way
     neighboring pages do (sections or version tabs), and make each path
     complete on its own.
   - **Conditional steps without a condition**: say who a step applies to,
     before the step. A step that runs unconditionally for an optional service
     is a real defect: in canonical/landscape-documentation#372 a migration
     guide enabled an optional service for every reader, while a later section
     said it was only for WSL.
   - **Obvious UI narration**: remove clicks and descriptions the interface
     already makes clear. Keep anything non-obvious.
   - **Headings, anchors, and terminology**: follow `AGENTS.md`. When you change
     a heading that has a label, or a label, check inbound references with
     `docs/scripts/find_references.py`.
5. **Never change technical content.** Leave commands, values, configuration
   keys, versions, names, and claims exactly as written, even if you suspect
   they're wrong. Raise each doubt as a question with its location.
6. **Run the tiered checks** in `AGENTS.md` if you edited files.

## Output

- The edits (or, if a restructure is needed, the proposal and no edits).
- A short rationale per change: one line each, grouped if several changes have
  the same reason.
- Questions for the author: technical doubts, unclear conditions, and
  applicability gaps, each with a location.

## Stop conditions

- Stop after proposing if the draft needs more than light restructuring or
  should move to another page.
- Stop and ask if you can't tell which readers a section or step applies to.
  Don't guess the condition.
- Don't extend the edit to pages the draft doesn't touch. List them as
  observations.

## Without internal access

- You don't need product source access for this skill: you aren't verifying
  behavior. Where a technical doubt can only be settled with internal sources,
  ask the author instead of checking.
- Keep questions in public PR comments free of internal links and details.
