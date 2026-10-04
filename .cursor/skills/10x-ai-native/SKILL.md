---
name: 10x-ai-native
description: >-
  Maps 10x skills onto this repo: markdown board and/or local ticket dirs
  instead of assuming Jira paths. CONTEXT.md glossary at repo root, decisions
  under context/decisions/. Adapter only — does not run grill, PRD, or implement.
---

<!-- ai-native:generated:begin -->
# Ai Native adapter

Adapter. Not a second 10x. Invoke **one** 10x skill per turn; this file only remaps paths.

Read `context/.ai-native.yml` for `packs`, `board`, `default_branch`, `decision_policy`, and `tracker`. Read `.cursor/rules/ai-native-project.mdc` for project conventions.

## Paths

| 10x default | Here |
|-------------|------|
| `CONTEXT.md` glossary | `CONTEXT.md` (repo root, glossary only) |
| `docs/adrs/` | `context/decisions/` after the whole feature has merged and promotion evidence passes. Until then: preliminary records for this `layout` |
| Jira board | `context/planning/board.md` when `board` is markdown, or the configured tracker |
| Jira issue | `layout: features` → `context/features/<feature>/tickets/<ID>/INDEX.md` + `plan.md`. Otherwise `context/planning/tickets/<ID>/INDEX.md` + `plan.md` |
| Working memory | `context/` (`context/INDEX.md` router) |
| Changelog | `context/CHANGELOG.md` or `CHANGELOG.md` |

## Phase remaps

- **grill-me-with-docs** — read root `CONTEXT.md`. Pack default: new decisions are preliminary, not accepted history. If `decision_policy` is `locked_on_record`, honor that store and do not relocate it.
- **wayfinder** — one destination, one map. Markdown maps live under `context/planning/maps/` when present. A Jira epic only when `tracker.kind` is `jira` and the user asks to publish.
- **to-issues** — quiz, then write the ticket dir for this `layout` (`features/<feature>/tickets/<ID>/` or `planning/tickets/<ID>/`) with `## current` / `## ac` and a thin card when the board is markdown. Parent/child grouping is links, not nested directories. `plan.md` is the plan chat, not this skill. Tracker writes only when the user asks.
- **implement** — Story is `context/INDEX.md`'s `ticket` → that dir's INDEX.md + plan.md. Execute the plan; set `in_review`, not `done`. After merge to `main`, `ship-ticket` if `board` is markdown. Do not promote feature decisions from a ticket close.
- **code-review** — spec source is INDEX.md + plan.md. Report only.
- **qa** — missing feature or bug → that layout's ticket dir, plus a board card when the board is markdown.

## Do not

- Run grill / PRD / implement from this skill
- Invent a WIP limit. A project that wants one sets it in `.cursor/rules/ai-native-project.mdc`
- Treat INDEX or `progress.md` as the board
- Write the tracker unless the user explicitly asks
<!-- ai-native:generated:end -->

<!-- ai-native:project:begin -->
This repo dogfoods the catalog. Markdown board, merge branch `main`, decision policy `preliminary_until_feature_merge`. S00 is not shipped.
<!-- ai-native:project:end -->
