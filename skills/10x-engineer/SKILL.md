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
                                  to-issues      (Jira Stories)
                                      ↓
                                  implement      (drives tdd; worktree if parallel)
                                      ⇄ qa       (file the bug)
                                      ⇄ diagnosing-bugs  (hard: red loop → cause → fix)
                                      ↓
                                 code-review     (fresh session, after a commit)
```

Do not start `implement` until the board exists. Do not use `tdd` / `implement` to plan.

| Phase | Skill | What it does |
|---|---|---|
| 00 · SCALE | `wayfinder` | Multi-session **decision** map. One epic = one map. Plan, don't do. |
| 01 · IDEA | `grill-me` | Interrogate until shared understanding (one sitting). |
| 01 · IDEA (alt) | `grill-me-with-docs` | Same, glossary + ADRs inline. |
| 02 · RESEARCH *(opt)* | `research` | Cited primary-source `research.md`. |
| 03 · PROTOTYPE *(opt)* | `prototype` | Throwaway probe — one ungrillable question. |
| — · CROSS-CUTTING | `handoff` | Package decisions when context will reset. |
| 04 · PRD | `write-a-prd` | Short contract, seams included. |
| 05 · BOARD | `to-issues` | Vertical Jira Stories; quiz; then publish. |
| 06 · BUILD | `implement` | One Story; no redesign; drives `tdd`. |
| 06 · BUILD (loop) | `tdd` | Red / green / **refactor while green** (Beck, not current Matt). |
| 07 · QA | `qa` | User-reported problems → durable issues. Obvious bugs → `implement`. |
| 07 · DIAGNOSE | `diagnosing-bugs` | Hard bugs: red loop first, then cause, then `tdd` regression. |
| 08 · REVIEW | `code-review` | Standards vs Spec, fresh session, after a commit. Report only; do not implement. |

## Operating rules

- **If it will not fit one session** → `wayfinder`. Else grill.
- **No PRD before shared understanding.**
- **Ungrillable interrupt:** leave grill, `prototype`, return.
- **Skip research/prototype** on well-trodden ground; don't skip new SDKs / regulated / unfamiliar code.
- **PRD is a contract.** Not in the PRD = not in scope.
- **Board is a graph.** Parallel-eligible = no blockers (file overlap is fine).
- **`implement` trusts the board.** One ticket, own worktree if parallel, no auto-commit unless asked.
- **`qa` files; `diagnosing-bugs` hunts.** Obvious bug → ticket then `implement`. No red loop yet / intermittent / "debug this" → `diagnosing-bugs`. Neither is planning.
- **`tdd` here is Beck** (refactor in the loop). Current Matt `tdd` is red-green only.

## Worth adopting once

- **`CONTEXT.md`** — glossary only.
- **Working memory** — `/ai-native-init` seeds `context/` (or `docs/`) INDEX + ticket dirs. Do not invent a second board. Standups: `/scrum-master`. Markdown closer: `/ship-ticket` after merge.
- **ADRs** — `{root}/decisions/` when a call is hard to reverse, surprising, and a real trade-off.
