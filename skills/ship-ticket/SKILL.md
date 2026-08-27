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

Closer for repos that track work in markdown. Jira-only repos: skip this skill.

Discover the memory root: `context/INDEX.md` then `docs/INDEX.md`. `{root}` is that folder. Board: `{root}/planning/board.md`. Changelog: `{root}/CHANGELOG.md` or repo-root `CHANGELOG.md`.

Run **after merge** to that repo's default branch (`develop` if `.cursor/rules/branch-naming.mdc` says so, otherwise `main`). Implement sets INDEX `in_review`; this skill sets `done` and closes the board. Do not ship from an implement chat that has not merged.

## Discover

Need both a board and a changelog (else stop with a one-line reason).

Ticket body, first match:

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

Ids look like `S01-01` or `BUG-01` (two-digit sprint). Require an ID already on the board. If missing, stop.

## Do

1. Confirm which ID. Confirm changelog section: Added / Changed / Fixed (ask if unclear; default **Added**).
2. Remove the card from Todo, In progress, or Blocked.
3. Append it under `## Done` as `- [x] **ID**: title`. Ticket link: `tickets/<ID>/INDEX.md` if that file exists, else keep the existing href.
4. Under changelog `## Unreleased` → the chosen `###` heading, append `- **ID**: <same title>`.
5. If `tickets/<ID>/INDEX.md` exists: set frontmatter `status: done`. If `plan.md` exists, set its `status: done` too.
6. If sprint/epic `progress.md` exists: move the key from `doing` / `in_review` to `done`.
7. If that folder `INDEX.md` has a status cell for the key, set it to `done`.
8. Stop. Do not edit sprint-log, pm-state, or start another ticket.
9. **Git / PR is not this skill’s default.** Only if the user asks to commit or open a PR: follow `.cursor/rules/branch-naming.mdc` if that file exists, commit **only** files for this ticket, push, then open a PR with `gh pr create` or GitHub MCP `pull_request_create`. Do not auto-commit. Do not mix unrelated WIP onto the branch.

If the ID is already in Done **and** already in the changelog **and** (when an INDEX exists) INDEX `status` is `done`, say so and stop.

INDEX `in_review` with a still-open PR is not ready to ship. Stop and say merge first, unless the user explicitly wants the board closed anyway.
