---
name: implement
description: >-
  Build one already-decided Jira Story: do not redesign, drive tdd at PRD
  seams, typecheck, full suite once, then review. Use when the user says
  "/implement", "implement this ticket", or points at a Story after to-issues.
  One ticket per session (own worktree if running in parallel).
disable-model-invocation: true
---

# Implement

Session orchestrator for work that is **already decided**. Read the Story, trust the PRD, write the code. Do not grill, do not reopen the plan, do not grow an epic.

`tdd` is the test loop this skill drives. `qa` is not this skill — file bugs there after the fact.

## When to use

| The work is… | Reach for |
|---|---|
| A Jira Story on the board | `/implement PROJ-123` (confirm the title back first) |
| A markdown Story (`docs/planning/tickets/`) | `/implement S01-01` (same: confirm the title) |
| A spec not yet sliced | `to-issues` first |
| Not written down | `grill-me` / `wayfinder` — not this skill |
| One behaviour, no ticket | `tdd` directly |
| User reporting a bug | `qa` (file it) |
| Hard bug / "debug this" | `diagnosing-bugs` |

## Hard rules

1. **One Story per invocation.** Confirm the Jira title before touching code.
2. **Do not redesign.** No interview, no "better approach." Wrong ticket → stop; send it back to the PRD / `to-issues`.
3. **Seams come from the PRD** (`Testing / seams` + the ticket's Seam(s) field). Confirm if missing; then drive `tdd`.
4. **Drive local `tdd`** — red → green → **refactor while green** (Beck). This is not current Matt `tdd` (he moved refactor into review).
5. **Typecheck often.** Run the focused test file each cycle; **full suite once** at the end.
6. **Checkout:** never two `implement` sessions in the same working copy. Parallel-eligible Stories (no graph blockers) each get their **own git worktree + branch**. File overlap is fine; merge later. Do not use `git stash` (`refs/stash` is shared).
7. **Do not auto-commit** on a job repo unless the user asks. Default: leave the diff; they commit / open the PR.
8. **Do not close Jira.** The human does that. If the repo has `docs/planning/board.md` **and** a changelog (`docs/CHANGELOG.md` or `CHANGELOG.md`), run `ship-ticket` after acceptance criteria are met. Skip SHIP when there is no markdown board.
9. **Review after there is a commit** (or in a fresh session against the branch point). Reviewing an empty `git diff main...HEAD` is a no-op. Prefer a **fresh session** so the author does not grade its own exam. Two axes: **Standards** vs **Spec** (see `code-review` if present).

## One run

1. Fetch the Story (Jira, URL, or `docs/planning/tickets/<ID>.md` if that folder exists). Restate what you will build. Stop if it is a wayfinder *decision* ticket, not a Story.
2. Read the PRD section it points at. Name the seam(s).
3. If parallel with another in-flight Story: work in a dedicated worktree. If the board marked it blocked, refuse.
4. For each acceptance criterion: `tdd` (red → green → refactor).
5. Typecheck + that test file as you go. Full suite once, green.
6. If a markdown board+changelog exist, run `ship-ticket` for this Story’s ID. Otherwise stop without closing Jira.
7. Show the diff. Commit / PR only if asked. Suggest `code-review` in a new chat against the merge-base.
