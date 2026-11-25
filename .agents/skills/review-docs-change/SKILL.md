---
name: review-docs-change
description: "Review a Landscape docs PR or diff and report findings, without editing it. Use when asked to review, check, or approve a docs change. Checks whether the change resolves its issue, whether readers can complete the affected task, applicability, generated content, and ripple effects. Produces evidence-backed findings marked blocking or non-blocking, or a short approval. Not for: editing the change (use edit-technical-draft or update-docs) or running procedures (use test-procedure)."
---

# Review a docs change

Decide whether a docs change is ready, and say exactly what blocks it. Shared
rules are in `AGENTS.md`; this skill doesn't repeat them.

## Inputs

- The change: a PR number, branch, or diff.
- The stated purpose: the linked issue or the PR description.

## Steps

1. **Read the purpose, then the diff.** Does the change resolve its stated
   issue? Read the changed sections in context, and ask: can a reader on each
   affected path complete the task?
2. **Review only changed content.** Read surrounding text for context, but don't
   report problems in lines the change didn't touch, unless the change makes
   them wrong (for example, a new step that contradicts an unchanged one).
3. **Check applicability.** For new or changed claims, run through the checklist
   in `AGENTS.md`. Look for steps that apply only to some readers but don't say
   so, and for one path's steps leaking into another.
4. **Check generated content.** Make sure the diff doesn't hand-edit a region
   listed in "Generated and synced content" in `AGENTS.md`.
5. **Check ripple effects for ripple-prone files.** These are snippets in
   `docs/reuse/` and `**/_includes/`, `docs/reuse/substitutions.yaml`, changed
   or removed labels and headings, and renamed, moved, or deleted pages. Using
   "Checking references" in `AGENTS.md`, check that inbound references,
   toctrees, and `docs/redirects.txt` are updated. For a snippet change, check
   that the new text reads correctly on every page that includes it. Check
   new Markdown-style internal links by hand; the build doesn't (see
   `AGENTS.md`).
6. **Weigh each finding.** Report only what you can support with evidence: a
   location and a quote, a source, or a contradiction within the docs. Mark it:
   - **Blocking**: technical content that contradicts the docs or a source, a
     reader can't complete the task, broken references or navigation, or the
     change doesn't resolve its issue.
   - **Non-blocking**: a real but minor improvement. Report at most three; drop
     the weakest.
   Don't suggest synonyms or rewrites based on style preference.
7. **Suggest `test-procedure` only** when the change alters steps a reader runs
   and running them would settle a doubt.

## Output

- **Verdict**: approve, approve with non-blocking notes, or changes needed.
- **Blocking findings**: each with location (`file:line`), evidence, and what
  would resolve it.
- **Non-blocking findings**: at most three, same format.
- **Questions**: only ones whose answer could change the verdict.

A small, correct change gets a one-sentence approval and nothing else.

## Stop conditions

- Don't edit files or push suggestions as commits.
- Stop at the verdict. Don't expand the review to unchanged pages or to a
  general audit of the section.
- Trust the author's technical claims by default (see `AGENTS.md`). Being
  unable to verify a claim isn't a reason to block. Block only when you have
  evidence that it's wrong; otherwise, at most, ask one non-blocking question.

## Without internal access

- Check claims against public sources from `AGENTS.md` when a claim looks
  doubtful. If it can only be checked in an internal repository, say what you
  couldn't verify; that's a question for the author, not a blocking finding.
