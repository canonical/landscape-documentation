---
name: test-procedure
description: "Check whether a documented Landscape procedure works, by a static walkthrough and, only with approval, by running it in a disposable environment. Use when asked to test, try, validate, or walk through the steps of a how-to guide or tutorial. Produces a test report with proposed fixes and doesn't edit the docs. Not for: editorial review or restructuring (use edit-technical-draft or review-docs-change), or testing anything beyond the requested procedure."
---

# Test a procedure

Find out whether a reader starting from a stated state can complete the
documented procedure. Shared rules are in `AGENTS.md`; this skill doesn't repeat
them.

## Inputs

- The procedure: a page, a section, or a diff.
- Which path to test, if the page has several (edition, install method, release,
  fresh install or upgrade).
- Whether you may execute commands, and in which disposable environment.

## Steps

1. **State the starting state and the success criterion first.** Write down,
   before testing:
   - Ubuntu release; Landscape release; edition; install method; fresh install
     or upgrade (and from which release); snap or charm channel, if any.
   - One observable success criterion, such as a service state, a page that
     loads, or a command's output.

   If the page doesn't determine one of these, ask, or pick the one the page
   most clearly targets and say so.
2. **Do a static walkthrough.** Read the procedure as the reader would, from the
   stated starting state:
   - prerequisites: are they all stated, and stated before they're needed?
   - order: does each step have what it needs from earlier steps?
   - placeholders: are they explained, and consistent across steps and
     examples?
   - branches and version tabs: is it clear which steps apply to your path?
   - channels, package names, and versions: do they agree across the page and
     with public sources (Charmhub, `snap info`, Launchpad)?
3. **Execute only with approval, and never on the host.** Run commands only if
   the user approves and a disposable environment is available (an LXD
   container, a Multipass VM, or another VM). Match the starting state the docs
   assume, not an empty machine: a stock install can differ from an empty
   container. In canonical/landscape-documentation#289, a port that was free in
   an empty container was already taken by `apache2` on a stock Quickstart
   install.
4. **Test one path per run** unless asked for more. Stop at the first blocking
   failure; don't improvise workarounds and keep going as if the step passed.
5. **Record exact commands and output**, including commands you ran that the
   docs don't contain (for diagnosis), marked as such.

## Output

A report with these sections:

- **Starting state and success criterion**: as stated in step 1.
- **Tested and passed**: steps, with the evidence (command and key output).
- **Failed**: the step, the exact command and output, and the likely cause if
  the evidence shows it.
- **Not tested**: steps or paths you didn't cover, and why.
- **Needs SME confirmation**: behavior you couldn't settle from the docs or
  public sources.
- **Proposed fixes**: for each failure or gap, a concrete docs change. Don't
  apply it.

For a static walkthrough only, say so at the top, and put anything that needs
execution under "Not tested".

## Stop conditions

- Don't execute anything without approval and a disposable environment.
  Without both, do the static walkthrough only.
- Stop at the first blocking failure.
- Stop and ask if the procedure needs credentials, a paid subscription token, or
  access you don't have. Never ask for secrets in chat.
- Don't edit the docs.

## Without internal access

- Use public artifacts only: public PPAs, the Snap Store, Charmhub, and public
  repositories at release tags.
- If a step depends on unreleased packages, internal channels, or internal
  infrastructure, mark it "Not tested" and say what access it needs.
