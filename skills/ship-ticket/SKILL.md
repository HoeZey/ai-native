---
name: ship-ticket
description: >-
  Move a finished ticket to Done on the repo markdown board, mark the ticket
  dir done, and append a parseable changelog line. Use when the user says
  /ship, "close this ticket", a Story is merged to the default branch, or a
  QA fix is actually done. Does not invent Jira. Does not start the next ticket.
disable-model-invocation: true
---

# Ship ticket

Closer for one merged ticket. It does not promote feature decisions.

Discover the memory root: `context/INDEX.md` then `docs/INDEX.md`. `{root}` is that folder. Read `{root}/.ai-native.yml` for `board`, `default_branch`, `layout`, and `decision_policy`. Board file, when `board` is markdown: `{root}/planning/board.md`. Changelog: `{root}/CHANGELOG.md` or repo-root `CHANGELOG.md`.

Run **after merge** to `default_branch` from that file. If `default_branch` is missing, ask. Do not infer the branch from `branch-naming.mdc`. Implement sets INDEX `in_review`; this skill sets `done` only after that merge. Do not ship from an implement chat that has not merged.

Engineering work does not need sprint planning to close. If `board` is `jira`, or the markdown board file is absent: do not stop for a missing board, and do not create one. Update the local ticket when it exists. Do not write the tracker unless the user explicitly asks in this conversation.

## Discover

A markdown close needs the board file and a changelog (else stop with a one-line reason). A tracker-only close needs neither.

Read `{root}/INDEX.md` `layout`.

When `layout` is `features`:

1. Ticket body: `{root}/features/<feature>/tickets/<ID>/INDEX.md` (one match).
2. Feature folder: that ticket's `features/<feature>/`.
3. Sprint notes, optional: `{root}/sprint-planning/<sprint>/` from the ticket frontmatter `sprint:`.

Otherwise, first match:

1. `{root}/planning/tickets/<ID>/INDEX.md`
2. `{root}/planning/tickets/<ID>.md` (legacy flat file)

Sprint folder (optional): `{root}/planning/sprints/<sprint>/` using INDEX frontmatter `sprint:` or the ID prefix (`S00-02` → `S00`). Epic layout: `{root}/planning/epics/<KEY>/`. Then `progress.md` and folder `INDEX.md` if they exist.

Do not invent Jira. Do not no-op silently.

## ID contract

Board card and changelog line share an ID. After `- ` the first token is `**TICKET-ID**:`.

```markdown
- [ ] **S01-01**: Boot Month 1 with real GameState fields
```

```markdown
- **S01-01**: Boot Month 1 with real GameState fields
```

Ids look like `S01-01` or `BUG-01` (two-digit sprint). A markdown close requires an ID already on the board. A tracker close uses the local ticket id or the tracker key the user named. If neither exists, stop.

## Do

When `board` is markdown, update the board and changelog. Otherwise skip those files. If a local ticket dir exists, update it. If it does not, do not invent one.

1. Confirm which ID. Confirm changelog section when a changelog exists: Added / Changed / Fixed (ask if unclear; default **Added**).
2. On a markdown board, remove the card from Todo, In progress, or Blocked.
3. On a markdown board, append it under `## Done` as `- [x] **ID**: title`. Ticket link: the ticket `INDEX.md` path from `{root}`, after the move in step 5 when `layout` is `features`.
4. When a changelog exists, under `## Unreleased` → the chosen `###` heading, append `- **ID**: <same title>`. If that ID already has an Unreleased bullet, update it instead of adding a second one.
5. When merge to `default_branch` is confirmed, set frontmatter `status: done` on `INDEX.md`. If `plan.md` exists, set its `status: done` too. When `layout` is `features`, move `features/<feature>/tickets/<ID>/` to `features/<feature>/done/<ID>/`. If the user only asked to close the card before merge, skip this step.
6. If feature, sprint, or epic `progress.md` exists: move the key from `doing` / `in_review` to `done`.
7. If that folder `INDEX.md` has a status cell for the key, set it to `done`.
8. Do not promote feature decisions while closing this ticket.
9. Do not edit sprint-log, pm-state, or start another ticket. A sprint accounting label is not merge evidence and does not belong in a decision record.
10. **Git / PR is not this skill’s default.** Only if the user asks to commit or open a PR: follow `.cursor/rules/branch-naming.mdc` if that file exists, commit **only** files for this ticket, push, then open a PR with `gh pr create` or GitHub MCP `pull_request_create`. Do not auto-commit. Do not mix unrelated WIP onto the branch.

If the ID is already in Done **and** already in the changelog **and** (when an INDEX exists) INDEX `status` is `done`, say so and stop.

INDEX `in_review` with a still-open PR is not ready to ship. Stop and say merge first. If the user explicitly wants the board card closed anyway: move that card, say merge was not verified, leave the ticket status `in_review`, and do not promote.

## Promote feature decisions

Not part of closing one ticket. Run only when the user asks to promote this feature. If `decision_policy` is `locked_on_record`, stop. Do not move or rewrite that store.

Positive evidence, all required:

1. The feature INDEX status table is the agreed scope.
2. Every row is `done`, `parked`, `dropped`, or `dup`. Any other or unknown status blocks promotion.
3. Every `done` row has a ticket record (under `tickets/` or `done/`, or a tracker key on the row) whose status is `done`, and this conversation has confirmed merge to `default_branch`. A missing record blocks promotion.
4. Nested children listed on a row or ticket must each be `done`, `parked`, `dropped`, or `dup`. An open child blocks promotion.
5. At least one in-scope row is `done`. An empty table or an empty `tickets/` directory is not evidence.
6. Parked, dropped, and dup rows stay out of accepted history.

Then, for `layout: features`, copy each preliminary file to `{root}/decisions/`, set status `accepted`, and leave a pointer in the old file (same id, status `promoted`, link to the new path) so references still resolve. Stop if the destination filename exists. Do not delete the pointer. On `sprints` or `epics`, copy the settled entries out of that folder's `decisions.md` log the same way, and leave a pointer line in the log.
