---
name: to-issues
description: >-
  Slice a PRD into vertical tickets with explicit blocked-by links. Quiz the
  breakdown before publishing. Use when the user says
  "/to-issues", "turn this PRD into tickets", or "break this down", after
  write-a-prd. Next is implement, not coding in this skill.
---

# To Issues

Each ticket is a thin **vertical** slice — a little frontend, a little backend — testable end-to-end the moment it's done. These are implementation tickets under the feature (or under the Jira epic when that is the tracker), **not** wayfinder decision tickets. A ticket may name a parent. Do not invent nested ticket directories; grouping is links and parent keys.

## Vertical, not horizontal

| Good slice | Bad slice |
|---|---|
| "User can submit feedback (DB + endpoint + minimal form)" | "Feedback table migration" |
| "Pipeline list shows status badge (field + API + UI)" | "Add `status` column" |
| "Login with email/password (DB + endpoint + form + redirect)" | "Build the auth middleware" |

**Read [`examples.md`](examples.md)** for a worked comparison.

## The board is a graph

- **Parallel-eligible = no graph blockers.** Shared files do not serialize. Merge conflicts later beat idle time.
- If a ticket needs another's *behavior*, **draw the block**. When the tracker is Jira, that is `is blocked by`.
- Prefactor goes first only when it is a real dependency ("the change is not easy until this tangle is gone") — not because of file overlap.

## Prefactor and wide refactors

- Look for "make the change easy, then make the easy change." If a prefactor must land before any vertical slice can stay green, it is ticket 0 and **blocks** the rest.
- **Wide mechanical change** (rename a column, retype a shared symbol) is the exception to vertical slicing. Sequence **expand → migrate in batches → contract**. Don't force it into a fake tracer bullet.

## One-window size

Each Story should fit **one fresh agent context window**. If it doesn't fit on a screen or would blow a session, split.

## Workflow

1. Read the PRD (user stories, success criteria, **Testing / seams**). Do not slice a wayfinder map — collapse it with `write-a-prd` first.
2. Draft vertical slices. Each names the **seam(s)** it covers (point at the PRD Testing section).
3. **Quiz before any publish.** For each ticket show: Title, Blocked by, Parent (if any), What it delivers, Parallel-eligible (yes iff no blockers), Seam(s). Ask: granularity, edges, merge/split. Iterate until approved.
4. Only then publish where the project tracks work. Discover `{root}` from `context/INDEX.md`, else `docs/INDEX.md`, and `layout` / `board` / `tracker` from `{root}/.ai-native.yml`. Local: write each ticket into that layout's ticket directory (`features/<feature>/tickets/<ID>/` or `planning/tickets/<ID>/`) and a thin card when `board` is markdown. Jira: only if the user agrees and `tracker.kind` is `jira` — the project's story type, parent link when hierarchy is a declared capability, and blocked-by links. Do not close or edit the parent. If a capability is missing, explain and leave the local tickets as the record.
5. **Stop.** Next skill is `implement` (one Story per session). Do not start coding in this skill.

Draft path if needed: `.handoff/<feature>-tickets.md` until the quiz passes.

## Template

```markdown
**Title:** <imperative, user-facing>
**Type:** Story
**Parent:** <feature, or epic key when the tracker is Jira>
**From PRD:** [<feature>](link#section)
**Seam(s):** <from PRD Testing / seams>

**What it delivers:** <end-to-end behavior, user's perspective>
**Scope (in):** <observable behaviors>
**Scope (out):** <deferred>
**Touches:** migration / repo / service / router / schema / UI / tests

**Acceptance criteria:**
- [ ] <observable, testable>

**Blocked by:** <keys> | none
**Blocks:** <keys> | none
**Parallel-eligible:** yes | no
```

No file paths in the body (they go stale). Exception: a prototype snippet that encodes a decision more precisely than prose — trim to the decision.

## Anti-patterns

- One ticket per layer (DB / API / UI). That's not a slice; it's a stack trace.
- Publishing before the quiz.
- Dumping wayfinder decision tickets into the sprint.
- "Refactor X" with no user-facing acceptance criteria → fold into a slice, or expand–contract.
- Hidden dependencies → draw the block.
- Mega-tickets that don't fit one context window → split.
- Handing off to `tdd` here — `implement` wraps `tdd`. This skill only publishes the board.
