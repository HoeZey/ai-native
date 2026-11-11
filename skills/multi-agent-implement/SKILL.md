---
name: multi-agent-implement
description: >-
  Default build step after the board: nested subagents implement, review on
  two axes, and fix until green. Ticket mode loops one Story in this chat.
  Program mode plans a frozen manifest, then runs waves of Stories on a
  program branch. Fix forward; stop only for decisions that need a human.
  Use when the user says /multi-agent-implement, multi-agent implement,
  implement this ticket, long-running, overnight, unattended, many stories,
  PROGRAM-PLAN, or BUILD-PROGRAM.
disable-model-invocation: true
---

# Multi-agent implement

Coordinator for already-sliced Stories. Nested subagents implement, review,
and fix. The coordinator triages and keeps state. Not another planning
system. Grill, PRD, and issues stay the 10x contract.

This is the default build step once the board exists. Solo `implement` is the
fallback when the user wants to work hands-on. If the Task tool or subagents
are not available, say so and run the `implement` flow in this chat.

## Modes

| Invocation | Mode | Read |
|---|---|---|
| /multi-agent-implement KEY | Ticket. One Story, loop until green, in this chat. Agent mode. | this file, prompts.md |
| /multi-agent-implement plan | Program plan. Fill the manifest and write .runs/<run-id>/manifest.md. Stop. Do not branch, worktree, or launch. | program.md, manifest-template.md |
| /multi-agent-implement run <manifest-path> | Program run. Fresh Agent-mode chat. Waves of Stories on a program branch. Execute only that manifest. | program.md, prompts.md, scoreboard-template.md |

Ticket mode does not read program.md, write a manifest, create a program
branch, or integrate.

## References

- [program.md](program.md) — program plan and run
- [prompts.md](prompts.md) — subagent prompt contracts
- [manifest-template.md](manifest-template.md)
- [scoreboard-template.md](scoreboard-template.md)

## Ticket mode

The contract is the ticket's INDEX.md and plan.md (paths as in `implement`).
Confirm the title back first.

Preflight:

1. Record the repository root, `default_branch` from `.ai-native.yml`, and
   the merge-base SHA with that branch.
2. Record dirty user-checkout files without changing them.
3. Create the story branch and worktree. Do not switch the user checkout.
4. Write .runs/<date>-<KEY>/scoreboard.md (one story row, from
   scoreboard-template.md) and events.log. Keep .runs local through an
   existing ignore rule or Git exclude.

Run the Story loop. Focused checks every round; the full suite once before
acceptance.

When the Story is green:

1. Set the ticket `status: in_review` and move it to `in_review` on
   progress.md. Commit that on the story branch. Do not set `done`. Do not
   run `ship-ticket`.
2. Close the story worktree (Worktree close). Leave the branch.
3. Write summary.txt: rounds, findings fixed, nits and out-of-scope items
   recorded, checks, head SHA.
4. Show COMPLETE with the branch and head SHA. Next: open a PR or merge, then
   `ship-ticket` when `board` is markdown. No `/code-review` paste. Fresh
   reviewers already covered both axes.

A human-only item stops the ticket: STOPPED with the exact question.

## Story loop

The same loop in both modes, one per Story.

1. Freeze Scope and acceptance criteria.
2. Launch one implementer. Require a committed head SHA and focused checks.
3. If production composition changed, require a test through the real
   factory or handler before review. Inner-adapter tests alone do not pass
   this gate.
4. Launch fresh Standards and Spec reviewers directly, in parallel, against
   the same base and head. Keep the axes separate.
5. Triage every failed check and every finding.
6. Any fixable item open: launch one remediation with all of them. When its
   checks pass, go to step 4.
7. Green: accept. Human-only: stop the ticket, or park the Story in a program.

Green means required checks pass, no blocking finding remains, and no
in-scope major or minor remains on either axis. Nits are recorded, not fixed.

Record every round in scoreboard.md (round, open findings) and events.log.

## Triage

Fix forward. Put every failed check, review finding, smoke failure, and
integration conflict in exactly one class.

- **Fixable** — resolvable inside the frozen contract with allowed writes:
  failing checks, including failures already on the base; blocking findings;
  in-scope majors and minors; smoke failures that break an acceptance
  criterion; merge conflicts. Send to remediation, or to the program fixer on
  the program branch. Never a stop. Never a question to the user.
- **Out of scope** — real, but outside the frozen contract. Record it in the
  scoreboard and summary. Write a follow-up issue only when that write is
  allowed. Do not fix it. Not a stop.
- **Nit** — record only.
- **Human-only** — only these five:
  1. Contract: the fix needs a change to a frozen acceptance criterion, the
     PRD, or a product decision, or two criteria contradict.
  2. Permission: the fix needs an undeclared write, push, live mutation,
     process termination, or protected resource.
  3. No progress: the same finding key comes back after 2 remediations, or
     the blocking count does not drop for 2 rounds in a row.
  4. Budget: the review round budget is spent. Default 6 rounds per Story. A
     manifest can set another number.
  5. Infrastructure: still fails after 2 documented safe retries.

The coordinator owns triage. Judge each finding against the frozen contract.
A reviewer can be wrong: reclassify with a one-line reason in events.log. A
disagreement between reviewer and implementer is not a stop. When a
remediation returns `needs-human`, check it against the five classes. If none
fits, triage the item as fixable with the coordinator's reading of the
contract.

The finding key is the reviewer's path plus title.

## Status

After every subagent, continue or show:

```text
RUNNING | WAITING_PERMISSION | STOPPED | COMPLETE
on: <story or gate>
next: <specific action>
```

Subagent completion alone never ends the coordinator chat. Do not offer the
user a choice between continuing and fixing. Fix, then continue.

WAITING_PERMISSION is only for the Permission class. Name the exact approval.
Every stop updates scoreboard.md, events.log, and summary.txt, then names the
next human action.

## Worktree close

A new worktree is cheap. Close it when this run is done with that checkout.

The coordinator does this. Nested agents do not. Remove only a path this run
recorded (`program_worktree` or a story row). Leave the branch. Do not
`rm -rf` the directory. Do not remove the user checkout.

From the user checkout, not from inside the worktree:

1. If `git -C <path> status --porcelain` prints anything, leave the worktree
   and name the path.
2. If it prints nothing, run `git worktree remove --force <path>`.
3. Set that scoreboard cell, or `program_worktree`, to `removed`. Append an
   events.log line.

Close a story worktree after the Story is accepted (ticket mode) or
integrated (program), or after it stops with an empty porcelain status.

## Nested roles

Read implement, tdd, and code-review as nested roles. Do not rewrite TDD or
the two-axis split.

- Implementer: one Story, no redesign, focused checks, commit, return
  SHA/checks/risks. No review or new-chat handoff.
- Axis reviewer: one axis, under 400 words, findings only, no patch or
  implicit publish.
- Remediation: only the fixable items from the last triage.
- Integrator: accepted wave SHAs, frozen contracts, current program head.
- Program fixer: the resumed integrator, fixing fixable items on the program
  branch.

## Gates

- PRD/issue is the contract. No redesign.
- Standards and Spec stay separate.
- Record fixture-green and user-path-green separately. Do not describe
  required skipped user-path work as complete.
- No undeclared write, push, promotion, or process termination.
- Nested agents do not delete worktrees.

## Hard nos

- No stop and no user question for a fixable item.
- No COMPLETE while a fixable item is open.
- No user-checkout switch.
- No nested-agent worktree deletion. The coordinator closes run worktrees
  only through Worktree close.
- No undeclared external or live mutation.
- No push or promotion unless explicitly authorized. Program completion and
  ticket acceptance are not merge evidence for a feature.
- No silent stop after subagent completion.
- No run-state or integration helper in v1. Add automation only after logs
  prove a recurring failure.
