---
name: update-docs
description: "Make a defined change to the Landscape documentation, or carry out an approved docs plan. Use when the task already says what should change (for example 'document the new configuration key in the manual installation guide' or 'apply this plan'). Edits files, keeps references and navigation intact, and runs the required checks. Not for: deciding what to document (use plan-docs-for-change), editorial passes on someone else's draft (use edit-technical-draft), or reviewing a change (use review-docs-change)."
---

# Update docs

Make a scoped docs change and leave the build, references, and navigation
working. Shared rules are in `AGENTS.md`; this skill doesn't repeat them.

## Inputs

- The change to make: a request, an issue, or an approved plan from
  `plan-docs-for-change`.
- The evidence for any technical claim you'll write (PR, source, public
  changelog). If there's none, see "Stop conditions".

## Steps

1. **Find the maintained source.** Check "Generated and synced content" in
   `AGENTS.md`. If the text you'd change is generated or bot-owned, change its
   source (the overlay, the upstream module) or stop and report. If the text
   comes from a snippet in `docs/reuse/` or `**/_includes/`, the edit belongs in
   the snippet, and it affects every page that includes it.
2. **Read the surroundings.** Read the whole target page and its neighbors in the
   same section. Note how they handle headings, version or edition differences,
   prerequisites, and code blocks.
3. **Integrate the change in place.** Put new content where a reader doing the
   task needs it, not in a new section appended at the end. Describe how the
   product works now, not how it changed; change history belongs in release
   notes. State applicability only where it matters (see the checklist in
   `AGENTS.md`).
4. **Check ripple effects.** When you rename, move, or delete a page, or change
   a label, an include, a snippet, or a substitution, run:

   ```bash
   python3 docs/scripts/find_references.py <path-or-label>
   ```

   Update every inbound reference and toctree entry it reports, and any
   redirect it lists that points to the old path. For a moved or deleted page,
   also add a new redirect (format in `AGENTS.md`). To retire a label that other
   pages or external links may use, keep it as an alias: a second `(label)=`
   line above the heading that replaces it.
5. **Run the tiered checks** from "Build and checks" in `AGENTS.md`, and fix
   failures your change caused. Don't fix unrelated failures; report them.

## Output

- The edits.
- Checks run, with their result (pass, or the failure and what you did).
- Claims you couldn't verify, if any.
- Observations not acted on: problems you noticed outside the task, each with a
  location. Keep this list short.

For a small change, keep the summary to a few lines.

## Stop conditions

- Stop and ask if the request is ambiguous about what to change or where, or if
  the change seems to need a new page or a restructure that the plan didn't
  cover.
- Stop and ask if a claim you'd need to write has no evidence. Don't fill the gap
  with a plausible default, command, or path.
- Stop if the only way to make the change is to hand-edit generated content.
- Don't keep going past a failing check you can't explain. Report it.

## Without internal access

- Write only what the request and public sources establish. If the request says
  something that you can't confirm publicly, don't silently drop it or expand
  it: write what's given and list it under "Claims you couldn't verify".
