---
name: sprint-planning
description: >-
  Plan and track team sprints from a sprint.yaml per sprint: commit what fits
  under the load limit, rank the rest to pull in, keep review-ready order, and
  answer status from a check script. Use when the user says /sprint-planning,
  "plan the sprint", asks about load, capacity, carry-over, what is left, who
  owns a ticket, or when a ticket should be review-ready. Does not implement.
---

# Sprint planning

Agent-first. You edit sprint.yaml, the script checks it and renders sprint.md. The user reads sprint.md and validates. Never hand-edit sprint.md.

## Where things live

- `{root}` is `context/`, else `docs/`.
- Project config: `{root}/sprint-planning/README.md`. Active sprint, tracker site and project, which statuses count as done, write lock, merge deadline rule. Read it first. If a fact is missing, ask. Do not invent capacity.
- Sprints: `{root}/sprint-planning/**/sprint-NN/sprint.yaml` plus generated `sprint.md`. Sprints that span a program may be grouped under one folder with a README for the calendar, capacity method, and scenarios.
- Script: `scripts/sprint.py` in this skill folder. Run with `uv run <skill>/scripts/sprint.py check|render PATH`. PATH is a sprint.yaml or a folder; a folder checks every sprint under it and across them.
- The feature contract (INDEX, plan.md, decisions) stays under the feature or ticket dir. Sprint files hold membership, order, owners, and dates only.

## Rules

- **Commit, then pull in.** `tickets` is the commitment and must fit under the load limit (default 80% of capacity). `pull_in` is ranked and not counted. No stretch. Better to pull in than to push out.
- **Row order of `tickets` is the review order.** Carry-over goes first, so it takes room before new work.
- **Owner is a person from `capacity`, or a pool name** (BE, FE) when nobody is assigned yet.
- **Review-ready is not sprint end.** Every `ready` date is on or before `merge_by`. A ticket is ready after its blockers.
- **Numbers come from the script.** Do not type loads, room, or totals into goal, notes, or open questions. They drift. Write the decision instead ("Hoshe is over capacity, move TCD-1 or accept").
- **Every edit gets a `changes` line**, newest first: `YYYY-MM-DD what changed`.
- After any edit: `render`, then `check`. Report what `check` flags. Do not silently change a plan choice to clear a flag.

## Intents

Detect which one the user wants. Load only what it needs.

### plan (new sprint)

1. Read the config, the previous sprint.yaml (carry-over), and the feature INDEX files that list slices, points, and blocked-by.
2. Write `capacity` from the config method and stated days off.
3. Readiness gate per candidate ticket: points, owner or pool, a spec link or Jira key, and every blocker done or placed earlier in this or an earlier sprint. A ticket that fails stays out or goes to `pull_in`, with the reason in `open_questions`.
4. Add carry-over first, then fill `tickets` in review order until each person is at the load limit. Set `ready` dates in blocker order.
5. Rank what did not fit in `pull_in`.
6. Write a one-sentence `goal`. Mark it proposed in `changes` until the user confirms.
7. Render, check, and show the user the check output plus open questions.

### status ("what is left", "who owns X", "when is X review-ready")

1. Run `check` on the sprint or the program folder.
2. Answer from its output and sprint.yaml. Do not fetch the tracker unless the user asks for a refresh.

### replan (move, reassign, pull in, drop)

1. Edit sprint.yaml. Pulling in moves the item from `pull_in` to `tickets` with an owner, status, and `ready`. Moving between sprints removes it from one file and adds it to the other.
2. Add a `changes` line, render, check.

### refresh (only when asked)

1. Read the tracker (Jira through Atlassian MCP). Tracker-owned fields: key, type, status, assignee, sprint id, stored estimate, parent.
2. Show the differences first. Then update only tracker-owned fields. Local-owned fields stay: order, `ready` dates, capacity, load limit, pull-in ranking, goal.
3. Each conflict becomes a `changes` line: `YYYY-MM-DD refresh: TCD-1 status local To Do, tracker In Review`.
4. Never write to the tracker unless the user explicitly asks for that write.

## sprint.yaml

```yaml
sprint: TCD Sprint 21
dates: [2026-10-07, 2026-10-20]
merge_by: 2026-10-16
jira: 2574                      # optional sprint id
jira_browse: https://site.atlassian.net/browse/   # optional, builds key links
goal: One sentence.
load_limit: 0.8                 # optional, default 0.8

capacity:
  - {person: Ana, pool: BE, points: 9.5, note: "0.75 of 13"}
  - {person: FE, pool: FE, points: 13, note: "one FE capacity"}

tickets:                        # committed, review order
  - key: TCD-1
    title: "[BE] Short title"
    story: TCD-0                # optional parent
    owner: Ana                  # person or pool
    points: 3
    status: To Do
    ready: 2026-10-08           # optional review-ready date
    blocked_by: [TCD-2]         # optional
    link: ../path/INDEX.md      # optional local spec; else jira_browse + key

pull_in:                        # ranked, not counted
  - {key: TCD-3, title: "[BE] Next", story: TCD-0, points: 2, blocked_by: []}

not_counted: ["Done design work, other teams, won't do"]
open_questions: ["Decisions the user still owes"]
changes: ["2026-10-05 What changed"]
```

Quote any free text that contains a comma inside a `{...}` mapping.

## What check flags

Over capacity or over the load limit (per person, and per pool with more than one person). A `ready` after `merge_by`. A ticket ready on or before its blocker. A blocker in a later sprint, or only in some `pull_in`. A ticket in two live sprints, or in both `tickets` and `pull_in`. A stale or missing sprint.md. Schema errors stop with the file, ticket, and field (exit 2). An unknown top-level key, ticket key, or capacity key is a schema error.
