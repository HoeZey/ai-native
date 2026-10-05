---
purpose: agent-lookup-and-mutate-protocol
process: /10x-engineer
adapter: .cursor/skills/10x-ai-native/SKILL.md
---

# Docs / working memory

This repo has no Jira. Product, PM, and engineering contract live under `context/`. `context/` is committed working memory.

Process lives in `/10x-engineer`, `/10x-ai-native`, and `.cursor/rules/ai-native-ai-native-engineering.mdc`. Do not copy skill graphs here.

Honor `INDEX.md` `layout`. Ticket dirs are the engineering contract. Do not paste PRD or ADR bodies into ticket INDEX files.

## Agent read order

1. This file (once).
2. [`TOOLS.md`](TOOLS.md) if the job needs code location or a PR.
3. [`INDEX.md`](INDEX.md) — honor `layout`, `current`, `current_feature`, and path keys. Then the folder INDEX it points at.
4. Honor `phase`, `skill`, and `ticket`.
5. That ticket's `plan.md` if it exists — implementer SoT (how + the decisions that apply).
6. Decisions: see below. Do not treat a preliminary decision as final.
7. Next: that folder's `progress.md`. For a features layout, sprint schedule is `sprint-planning/`, not the spec.

### `layout: features`

```
features/<feature>/INDEX.md
features/<feature>/tickets/<KEY>/INDEX.md    spec — AC, current, out_of_scope, seams
features/<feature>/tickets/<KEY>/plan.md     implementer SoT
features/<feature>/decisions/<id>.md         preliminary — editable until this feature merges
features/<feature>/done/<KEY>/               after the ticket is closed post-merge
sprint-planning/README.md                    active sprint, tracker facts, write lock
sprint-planning/<sprint>/sprint.yaml         source — commitment, pull-in, capacity, dates
sprint-planning/<sprint>/sprint.md           generated, read-only
decisions/                                   final — only after the feature has merged
```

`sprint.yaml` is membership, order, and capacity. It does not store the spec. `sprint.md` is generated from it.

### `layout: sprints`, `epics`, or `flat`

```
planning/tickets/<KEY>/INDEX.md    spec — AC, current, out_of_scope, seams
planning/tickets/<KEY>/plan.md     implementer SoT — how, inlined decisions, test matrix
```

Sprint or epic `decisions.md` is the working log for that folder. Look up an `id` cited in `plan.md`. Do not require a full read at implement time.

`plan.md` is required before `/implement` on a code slice. Parked / not-yet-grilled tickets may be INDEX only. If `plan.md` is silent on a choice, **stop and ask**. Do not guess.

INDEX keys: `seams` (public surface), `tests` (existing test files), `create` (new files — dir or purpose, not a filename). Extra key for this repo: `none` (`scenes` = packed scenes dir+purpose; `alembic` = dir+head, not a revision filename; `none` = omit).

`current` vs `ac` is the hop. Graft to verify, not to learn whether a thing exists.

## Decisions

Read `decision_policy` in `.ai-native.yml` when it is set. `locked_on_record` keeps that project's existing store: do not relocate those records and do not apply the pack default over them.

- **Preliminary** records are the working plan until the whole feature has merged to `main`. On `layout: features`, that store is `features/<feature>/decisions/<id>.md` (status `preliminary`). On `sprints` or `epics`, it is that folder's `decisions.md` log. On `flat`, keep the choice in the ticket plan until promotion. Rewrite the preliminary record when the choice changes. If you replace an id, update references that cite it. An agent that needs a different choice edits the preliminary record and continues. It does not answer "this has already been decided."
- **Final** (`decisions/`) receives a record only after the whole feature has merged and promotion evidence passes. Status is `accepted` or `superseded`. Do not rewrite an accepted record in place. Supersede it.
- One ticket merging does not freeze the rest of the feature. Closing a ticket, including a board close before merge, does not promote decisions.
- Promotion is a separate explicit request. It needs the feature INDEX scope table, every in-scope row `done`, `parked`, `dropped`, or `dup`, a real merged record for every `done` row, and the same accounting for nested children. An empty ticket directory, or the absence of `todo` / `doing` / `in_review`, is not evidence. Parked, dropped, and dup rows are not accepted history.
- If a preliminary choice already shipped in an earlier ticket on the same feature, changing it includes the code.

## Status

- `todo` — spec exists, not started
- `doing` — implement chat is on it
- `in_review` — slice implemented; not yet merged to `main`
- `done` — **only** when merged to `main`
- `parked` / `dropped` / `dup`

Implement **must not** set `done`. After a slice: `in_review`. Then `/code-review` in a new chat. `ship-ticket` closes the markdown board after merge. On a features layout it also moves the ticket dir into that feature's `done/`.

## Sessions

1. **Plan** — INDEX.md + `plan.md`. No product code. Do not spawn `/implement` from this chat.
2. **Implement** — `/implement <KEY>` in a new chat. Execute the plan. Set `in_review`.
3. **Review** — `/code-review` after a commit. Report only. Do not patch.

## Human reading order

1. [../CONTEXT.md](../CONTEXT.md) — glossary (repo root)
2. This folder's INDEX and board
3. `CHANGELOG.md` — what has shipped
4. `decisions/` — final decisions, after merge
