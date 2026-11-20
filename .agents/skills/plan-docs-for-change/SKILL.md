---
name: plan-docs-for-change
description: "Decide what Landscape documentation should change for a product change. Use when someone brings a product PR, issue, changelog entry, or description and asks what docs need to change, where, and whether any change is needed at all. Produces a short plan and makes no edits. Not for: writing or editing the docs change (use update-docs), editing an existing draft (use edit-technical-draft), or reviewing a docs diff (use review-docs-change)."
---

# Plan docs for a product change

Turn a product change into a short, evidence-backed docs plan. Shared rules
(applicability checklist, sources, generated content, conventions) are in
`AGENTS.md`; this skill doesn't repeat them.

## Inputs

- The product change: a PR, issue, changelog or release-note entry, or a plain
  description. Note which of these you actually have.
- Optional: the target release, and any constraints from the requester.

## Steps

1. **Work out what changes for the administrator.** Describe the change as the
   reader experiences it: a new or changed command, configuration key, default,
   UI behavior, API endpoint, requirement, or limitation. Run through the
   applicability checklist in `AGENTS.md` and record which items the change
   depends on and which are unknown. Ignore internal refactoring that has no
   visible effect.
2. **Find where readers meet the change.** Search `docs/` for the feature name,
   UI labels, configuration keys, commands, and endpoint paths. Check:
   - how-to guides for the affected task, including install, upgrade, and
     migration guides for each install method the change touches;
   - reference pages (configuration, API, charm, logs);
   - explanation pages that describe the behavior;
   - landing pages and toctrees, if a new page might be needed;
   - snippets in `docs/reuse/` and `**/_includes/`. Use
     `docs/scripts/find_references.py` to see which pages include them.
3. **Choose the smallest change that serves the reader.** Prefer extending an
   existing page over creating one. One sentence, one table row, or one
   configuration entry may be enough. "No docs change needed" is a valid result;
   say why. Propose a new page only when no existing page fits the reader's task,
   and name the landing page and toctree it belongs in.
4. **Check ownership.** If the change lands in a generated or synced region (see
   `AGENTS.md`), plan the change at its source instead.
5. **Ask only blocking questions.** At most five, batched, each one precise and
   answerable. Ask only when the answer changes the plan. Good examples:
   - "Is the schedule interpreted in UTC or in the server's local time?"
   - "Is this applied once at registration, or continuously enforced?"
   - "Optional for whom, and required for whom?"
   - "Does this apply to Landscape SaaS, or only to self-hosted Landscape?"

## Output

A short plan, then the questions:

| Page | Change | Doc type | Why | Evidence | Open questions |
| --- | --- | --- | --- | --- | --- |
| `docs/...` path, or "new: ..." | One line | How-to, reference, explanation, or release notes | The reader need | PR, file, or line that supports it | Question numbers, or "none" |

- Keep the plan to the rows the change needs. One row is fine.
- After the table, list the numbered blocking questions.
- If you noticed unrelated problems, list them separately as observations.

## Stop conditions

- Stop after the plan. Make no edits, even small ones.
- Stop and ask first if you can't tell what the change does for the
  administrator. Don't plan around a guess.
- If the evidence conflicts (for example, the PR description and the diff
  disagree), report the conflict as a question instead of picking one.

## Without internal access

- Product repositories may be internal. If you have only a description or a
  public changelog entry, plan from that, mark the evidence as "description
  only", and turn unverified behavior into questions.
- Check public sources from `AGENTS.md` (public repositories at release tags,
  Charmhub, `snap info`, Launchpad) before asking.
