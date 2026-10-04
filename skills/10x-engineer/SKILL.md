---
name: 10x-engineer
description: >-
  Route a non-trivial idea through planning then execution: grill or wayfinder
  → PRD → Jira board → implement (tdd) ⇄ qa; hard bugs → diagnosing-bugs.
  One skill per phase. Use when the user says "10x engineer" or "ai-native workflow".
---

# 10x Engineer

One phase, one goal, one agent at a time — so agents don't develop main-character syndrome and "plan, prompt, pray" doesn't ship.

**This skill is a router.** Invoke **one** skill per turn.

```
too big for one session? ─ yes → wayfinder (decision map)
                         └ no  → grill-me / grill-me-with-docs
                                      ↓
                         research / prototype  (ungrillable → prototype)
                                      ↓
                                 write-a-prd
                                      ↓
                                  to-issues      (vertical tickets)
                                      ↓
                    one Story ── implement ── code-review (fresh chat)
                    many Stories unattended ── long-running plan
                                                    ↓ approve
                                               long-running run
                                                    (nested implement / review / integrate)
```

Do not start implement or long-running until the board exists. Do not use tdd,
implement, or long-running to plan.

| Phase | Skill | What it does |
|---|---|---|
| 00 · SCALE | wayfinder | Multi-session **decision** map. One destination = one map (a Jira epic when that is the tracker). Plan, don't do. |
| 01 · IDEA | grill-me | Interrogate until shared understanding (one sitting). |
| 01 · IDEA (alt) | grill-me-with-docs | Same, glossary + ADRs inline. |
| 02 · RESEARCH *(opt)* | research | Cited primary-source research.md. |
| 03 · PROTOTYPE *(opt)* | prototype | Throwaway probe — one ungrillable question. |
| — · CROSS-CUTTING | handoff | Package decisions when context will reset. |
| 04 · PRD | write-a-prd | Short contract, seams included. |
| 05 · BOARD | to-issues | Vertical tickets on the project's board; quiz; then publish. |
| 05b · PROGRAM-PLAN | long-running plan | Switch to Plan mode. After a multi-story board: fill Cursor's plan artifact from the manifest template and stop for approval. Same PRD/issue contract; no second ticket format. |
| 06 · BUILD | implement | One Story; no redesign; drives tdd. |
| 06 · BUILD (loop) | tdd | Red / green / **refactor while green** (Beck; collapse overlapping tests in that refactor). |
| 06b · BUILD-PROGRAM | long-running run | After approval, save the manifest at .runs/<id>/manifest.md. Fresh Agent chat runs /long-running run with that path. Nested implement, review, remediation, integrate. |
| 07 · QA | qa | User-reported problems → durable issues. Obvious bugs → implement. |
| 07 · DIAGNOSE | diagnosing-bugs | Hard bugs: red loop first, then cause, then tdd regression. |
| 08 · REVIEW | code-review | Standards vs Spec, fresh session, after a commit. Report only; do not implement. |

## Operating rules

- **If it will not fit one session** → wayfinder. Else grill.
- **No PRD before shared understanding.**
- **Ungrillable interrupt:** leave grill, prototype, return.
- **Skip research/prototype** on well-trodden ground; don't skip new SDKs / regulated / unfamiliar code.
- **PRD is a contract.** Not in the PRD = not in scope.
- **Board is a graph.** Parallel-eligible = no blockers (file overlap is fine).
- **implement trusts the board.** One ticket, own worktree if parallel, commit
  when green. PR only if asked. After a full board: one ticket with you in
  the loop → /implement KEY. Many tickets unattended → /long-running plan,
  then save .runs/<id>/manifest.md and start a fresh
  /long-running run <manifest-path>.
- **Nested Task is allowed inside BUILD-PROGRAM only.** A fresh subagent is the fresh session for implement and code-review. Do not paste "open a new chat" at the user.
- **Mode boundary is mandatory.** PROGRAM-PLAN runs in Plan mode and stops for
  approval. BUILD-PROGRAM runs in Agent mode after approval.
- **qa files; diagnosing-bugs hunts.** Obvious bug → ticket then implement. No
  red loop yet / intermittent / "debug this" → diagnosing-bugs. Neither is
  planning.
- **tdd here is Beck** (refactor in the loop). Current Matt tdd is red-green only.
- **Phase done → Phase exit paste.** Last message is a fenced prompt for the next chat. The agent cannot open a new IDE chat. Nested Task is the same conversation — do not start the next phase that way. BUILD-PROGRAM is the exception: nested implement / review / integrate are roles inside that one phase.

## Phase exit

When this phase’s goal is met, the last message includes a fenced copy-paste prompt for the next chat. Fill command, key, and paths from the work just finished. Do not wait to be asked. Do not spawn the next skill from this chat.

The agent **cannot** open a new IDE chat. Nested Task / subagent is not a new chat.

Next command comes from the table below, unless the active folder's progress.md
or the ticket plan.md next_chat section names a pickup — then use that.

If there is no next phase (grill still open, map still foggy, user said stop), omit the block.

```text
/<skill> <KEY>
<one-line constraints>
```

| This phase done | Next prompt starts with |
|---|---|
| grill-me (shared understanding) | /write-a-prd |
| wayfinder map clear | /write-a-prd |
| PRD signed | /to-issues |
| board or ticket spec+plan ready | /implement <KEY> |
| board ready, many stories, unattended | /long-running plan |
| long-running plan approved | /long-running run <manifest-path> |
| implement committed (solo) | /code-review |
| implement committed (BUILD-PROGRAM) | (no paste; coordinator continues) |
| review has findings | /implement <KEY> (read plan.md code-review section) |
| qa filed a ticket | /implement <KEY> |

## Worth adopting once

- **CONTEXT.md** — glossary only.
- **Working memory** — `/ai-native-init` seeds `context/` (or `docs/`) INDEX + ticket dirs. Do not invent a second board. After merge to the configured default branch, `/ship-ticket` when `board` is markdown and that skill is installed. Tracker transitions only when the user asks. Do not require sprint planning to finish a ticket.
- **ADRs** — hard to reverse, surprising, and a real trade-off. Under the pack default, in-flight choices stay preliminary until the whole feature merges. Accepted history is `{root}/decisions/`. If `decision_policy` is `locked_on_record`, honor that store.

## Lineage

[Matt Pocock](https://github.com/mattpocock/skills) (grill / wayfinder / spec /
tickets / implement-as-orchestrator). Local tdd stays Beck. Jira via Atlassian
MCP. Theo Depraetere
([BONDage](https://www.linkedin.com/feed/update/urn:li:activity:7463151557669228546/)).
