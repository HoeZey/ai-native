---
name: 10x-engineer
description: >-
  Route a non-trivial idea through planning then execution: grill or wayfinder
  → PRD → Jira board → multi-agent-implement (implement, tdd, review) ⇄ qa;
  hard bugs → diagnosing-bugs.
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
                    one Story ── multi-agent-implement KEY
                                   (nested implement / review / fix until green)
                    many Stories ── multi-agent-implement plan
                                                    ↓ approve
                                               multi-agent-implement run
                                                    (waves of nested implement / review / integrate)
                    hands-on fallback ── implement ── code-review (fresh chat)
```

Do not start multi-agent-implement or implement until the board exists. Do
not use tdd, implement, or multi-agent-implement to plan.

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
| 05b · PROGRAM-PLAN | multi-agent-implement plan | Switch to Plan mode. After a multi-story board: fill the manifest template, write .runs/<id>/manifest.md, and stop for approval. Same PRD/issue contract; no second ticket format. |
| 06 · BUILD | multi-agent-implement KEY | Default. One Story; nested implementer and fresh two-axis reviewers loop until green; fix forward, stop only for human-only decisions. |
| 06 · BUILD (hands-on) | implement | Fallback when you want to be in the loop, or no subagents. One Story; no redesign; drives tdd. Also the nested implementer role. |
| 06 · BUILD (loop) | tdd | Red / green / **refactor while green** (Beck; collapse overlapping tests in that refactor). |
| 06b · BUILD-PROGRAM | multi-agent-implement run | After approval, a fresh Agent chat runs /multi-agent-implement run <manifest-path>. Waves of the same loop, then integrate. |
| 07 · QA | qa | Acceptance: run the ticket AC with the repo Playwright setup; report per AC in ACCEPTANCE.md. |
| 07 · DIAGNOSE | diagnosing-bugs | Hard bugs: red loop first, then cause, then tdd regression. |
| 08 · REVIEW | code-review | Standards vs Spec, fresh session, after a commit. Report only; do not implement. |

## Operating rules

- **If it will not fit one session** → wayfinder. Else grill.
- **No PRD before shared understanding.**
- **Ungrillable interrupt:** leave grill, prototype, return.
- **Skip research/prototype** on well-trodden ground; don't skip new SDKs / regulated / unfamiliar code.
- **PRD is a contract.** Not in the PRD = not in scope.
- **Board is a graph.** Parallel-eligible = no blockers (file overlap is fine).
- **Build trusts the board.** After a full board: one ticket →
  /multi-agent-implement KEY. Many tickets → /multi-agent-implement plan,
  then a fresh /multi-agent-implement run <manifest-path>. Hands-on, or no
  subagents → /implement KEY, then /code-review in a fresh chat. Each Story
  gets its own worktree; commit when green; leave the branch; PR only if
  asked. The coordinator removes each story worktree when that story is
  done, and the program worktree when the run ends. Nested agents do not
  delete worktrees. Solo implement removes its own worktree before the
  session ends.
- **code-review opens its own worktree.** Detached checkout of the reviewed
  commit. Do not switch the user checkout. Remove that worktree before the
  session ends. Nested reviewers use the coordinator's worktree and do not
  remove it.
- **Nested Task is allowed inside multi-agent-implement only.** A fresh subagent is the fresh session for implement and code-review. Do not paste "open a new chat" at the user.
- **Mode boundary is mandatory.** PROGRAM-PLAN runs in Plan mode and stops for
  approval. BUILD-PROGRAM and ticket mode run in Agent mode.
- **qa accepts; diagnosing-bugs hunts.** qa runs the ticket AC after build. Obvious bug → implement or tdd. No red loop yet / intermittent / "debug this" → diagnosing-bugs. Neither is planning.
- **tdd here is Beck** (refactor in the loop). Current Matt tdd is red-green only.
- **Phase done → Phase exit paste.** Last message is a fenced prompt for the next chat. The agent cannot open a new IDE chat. Nested Task is the same conversation — do not start the next phase that way. multi-agent-implement is the exception: nested implement / review / integrate are roles inside that one phase.

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
| board or ticket spec+plan ready | /multi-agent-implement <KEY> |
| board ready, many stories | /multi-agent-implement plan |
| multi-agent-implement plan approved | /multi-agent-implement run <manifest-path> |
| multi-agent-implement ticket green | (no paste; open a PR or merge, then /ship-ticket <KEY> when board is markdown) |
| implement committed (solo) | /code-review |
| implement committed (nested) | (no paste; coordinator continues) |
| review has findings | /multi-agent-implement <KEY> (read plan.md code-review section) |
| implement or code-review green | /qa <KEY> |
| qa has a failing AC | /multi-agent-implement <KEY> (read ACCEPTANCE.md) |

## Worth adopting once

- **CONTEXT.md** — glossary only.
- **Working memory** — `/ai-native-init` seeds `context/` (or `docs/`) INDEX + ticket dirs. Do not invent a second board. After merge to the configured default branch, `/ship-ticket` when `board` is markdown and that skill is installed. Tracker transitions only when the user asks. Do not require sprint planning to finish a ticket.
- **ADRs** — hard to reverse, surprising, and a real trade-off. Under the pack default, in-flight choices stay preliminary until the whole feature merges. Accepted history is `{root}/decisions/`. If `decision_policy` is `locked_on_record`, honor that store.

## Lineage

[Matt Pocock](https://github.com/mattpocock/skills) (grill / wayfinder / spec /
tickets / implement-as-orchestrator). Local tdd stays Beck. Jira via Atlassian
MCP. Theo Depraetere
([BONDage](https://www.linkedin.com/feed/update/urn:li:activity:7463151557669228546/)).
