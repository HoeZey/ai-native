---
name: implement
description: >-
  Build one Story: do not invent a new approach, drive tdd at PRD seams,
  typecheck, full suite once, then review. A preliminary decision can still
  change. Use when the user says "/implement", "implement this ticket", or
  points at a Story after to-issues. One ticket per session (own worktree if
  running in parallel). Remove that worktree before the session ends.
disable-model-invocation: true
---

# Implement

Session orchestrator for one Story. Read the Story, trust the current plan, write the code. Do not grill, do not grow the feature, and do not invent an approach the user did not ask for.

Read `decision_policy` in `{root}/.ai-native.yml` when it is set. If it is `locked_on_record`, or a project instruction locks the store, do not rewrite those records and do not apply the pack default over them. Supersede only when that project already does; otherwise stop and ask.

Otherwise a preliminary decision is the working plan, not a law. If the user wants a different choice, or the written choice cannot ship, edit it and continue. On `layout: features` that file is `features/<feature>/decisions/<id>.md`. On `sprints` or `epics` it is that folder's `decisions.md` log. Do not answer "this has already been decided." A record in `{root}/decisions/` is final because that feature has merged. Change it by superseding, and put the new choice on the feature that will change the code. If a preliminary choice already shipped in an earlier ticket on the same feature, the change includes the code. If you replace an id, update references that cite it.

`tdd` is the test loop this skill drives. `qa` is not this skill — file bugs there after the fact.

## When to use

| The work is… | Reach for |
|---|---|
| A Jira Story on the board | `/implement PROJ-123` (confirm the title back first) |
| A markdown Story | `/implement S01-01` (same: confirm the title) |
| A spec not yet sliced | `to-issues` first |
| Not written down | `grill-me` / `wayfinder` — not this skill |
| One behaviour, no ticket | `tdd` directly |
| User reporting a bug | `qa` (file it) |
| Hard bug / "debug this" | `diagnosing-bugs` |

Discover the memory root: `context/INDEX.md` then `docs/INDEX.md`. `{root}` is that folder. When `layout` is `features`, the Story is `{root}/features/<feature>/tickets/<KEY>/`. Otherwise `{root}/planning/tickets/<KEY>/`.

## Hard rules

1. **One Story per invocation.** Confirm the title before touching code.
2. **Do not redesign.** No interview, no "better approach" the user did not ask for. Wrong ticket → stop; send it back to the PRD / `to-issues`. A needed correction to a preliminary decision is an edit, not a refusal.
3. **Seams come from the PRD** (`Testing / seams` plus the ticket's Seam(s) field). Confirm if missing; then drive `tdd`.
4. **Drive local `tdd`** — red → green → **refactor while green** (Beck). Refactor includes the test suite: collapse twins, fold asserts, drop tests that never call changed production code. This is not current Matt `tdd` (he moved refactor into review).
5. **Typecheck often.** Run the focused test file each cycle; **full suite once** at the end. Before that suite, collapse overlapping tests added this ticket. Do not ship input/output (or similar) twins of the same assertion.
6. **Checkout:** never two `implement` sessions in the same working copy. Parallel-eligible Stories (no graph blockers) each get their **own git worktree + branch**. File overlap is fine; merge later. Do not use `git stash` (`refs/stash` is shared). After the commit, and before this session ends, remove every worktree this session created. Leave the branch. A later session can add a worktree again. Do not `rm -rf` the directory. From the user checkout, not from inside the worktree: if `git -C <path> status --porcelain` prints anything, leave that path and name it. If it prints nothing, run `git worktree remove --force <path>`. Do not remove a worktree this session did not create. Do not remove the user checkout. Nested under BUILD-PROGRAM, do not remove the worktree. The coordinator closes it when the story no longer needs a checkout.
7. **Commit when the slice is green.** Follow the repo's commit-message rules. Do not open a PR unless the user asks. Do not skip hooks.
8. **Do not close the ticket.** Set INDEX `status: in_review`. Do not run `ship-ticket` from this chat. Do not transition an external tracker. After merge, `ship-ticket` applies only when `board` is markdown. Feature decision promotion is never this step. Sprint planning is not required to finish the ticket.
9. **Review after there is a commit** (or in a fresh session against the branch point). Reviewing an empty `git diff main...HEAD` is a no-op. Prefer a **fresh session** so the author does not grade its own exam. Two axes: **Standards** vs **Spec** (see `code-review` if present).

## One run

1. Fetch the Story (Jira, URL, or the markdown ticket dir). Restate what you will build. Stop if it is a wayfinder *decision* ticket, not a Story.
2. Read the PRD section it points at. Name the seam(s). Read preliminary decisions the plan cites. They can still change.
3. If parallel with another in-flight Story: work in a dedicated worktree. If the board marked it blocked, refuse.
4. For each acceptance criterion: `tdd` (red → green → refactor, including test collapse).
5. Typecheck + that test file as you go. Collapse overlapping tests from this ticket, then full suite once, green.
6. Set the ticket `status: in_review`. Move it to `in_review` on the feature or sprint `progress.md`. Do not set `done`. Do not run `ship-ticket`.
7. Commit on the Story branch. Show the SHA. Remove every worktree this session created, unless nested under BUILD-PROGRAM. PR only if asked. Emit the 10x-engineer Phase exit paste for `/code-review` (fresh chat, merge-base). The paste names the branch and the commit to review. Do not start that review in this chat.

## Nested under BUILD-PROGRAM

When the parent is a long-running coordinator:

- Do not remove the worktree. The coordinator closes it when the story no longer needs a checkout.
- Do not emit a phase-exit paste or tell the user to open another chat.
- Do not start `code-review`.
- Run the manifest's focused checks instead of the solo full suite; the coordinator owns integrated full checks.
- Do not run `ship-ticket`, transition an external tracker, or promote feature decisions. The coordinator owns accepted bookkeeping, and only when the manifest names that write.
- Return to the coordinator: head SHA, focused checks run, remaining risks.

## Lineage

Orchestrator shape from [Matt Pocock's implement](https://www.aihero.dev/skills-implement). Local deltas: Beck `tdd`, worktrees for parallel-eligible tickets, remove those worktrees before the session ends, commit when green, review in a fresh session, `qa` stays a separate loop. Preliminary decisions stay editable until the feature merges.
