---
name: tdd
description: >-
  Red / green / refactor loop at a public seam. Agent runs the tests each
  step. Use when the user says "/tdd" or "TDD this", or when implement drives
  it on a Jira Story. Not current Matt tdd (refactor stays in this loop).
---

# TDD

The test **loop**, not the session orchestrator. `implement` owns one ticket, worktrees, typecheck, and close-out. This skill owns red → green → refactor.

**Not Matt's current `tdd`.** His later skill is red → green only; refactor moved to `code-review`. This fork keeps **Beck**: refactor **while green**, toward deep modules. `code-review` is a two-axis check (standards vs spec), not a substitute for that refactor step.

Invoke `/tdd` directly only for one behaviour with no Story. Otherwise `implement` drives this.

## The loop, per behavior

1. **Confirm the behavior** (Story acceptance criteria).
2. **Confirm the seam** — public interface from the PRD `Testing / seams` field. No test at an unconfirmed seam. Read `CONTEXT.md` so names match the glossary.
3. **Write one failing test.** Run it. Watch it go **red**.
4. **Implement minimum to pass.** Run it. Watch it go **green**.
5. **Refactor while green.** Deep modules (narrow interface, substantial implementation). No new behavior. Rerun after each step.

Then back to 3 for the next behavior.

## Diagnostics

- **No red in step 3** → test isn't testing what you think.
- **Green needs lots of code in step 4** → testing too much at once; split.
- **Refactor breaks tests** → undo; smaller step. If they break repeatedly, tests are coupled to implementation — rewrite against the public interface.

## Hard rules

- **One test per loop.** No bulk-adding (horizontal slicing).
- **The agent runs the tests** — every red and green verified.
- **No new behavior in refactor.**
- **No mocks of code you own.** Mock at trust boundaries (HTTP, FS, time, external SDKs).
- **No tautological tests.** Expected values come from a spec, a worked example, or a known-good literal — not by reimplementing the code in the assertion.
- **Tests survive internal refactors.** Behavior through the seam, not private methods.

## Per-ticket flow (when `implement` is not wrapping)

```
1. List acceptance criteria as a checklist.
2. For each: red → green → refactor.
3. Full suite green → PR if asked → link the Story.
4. Bugs that aren't this ticket → `qa` (not a guess-fix).
```
