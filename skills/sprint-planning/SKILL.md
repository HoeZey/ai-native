---
name: sprint-planning
description: >-
  Plan a sprint from local notes: membership, carry-over, capacity, and
  review timing. Refresh tracker facts only when asked. Use when the user
  says /sprint-planning, "plan the sprint", or asks about load, carry-over,
  or capacity. Does not implement.
disable-model-invocation: true
---

# Sprint planning

Schedule and load for one sprint. The feature contract stays under `features/<feature>/` (or the legacy ticket dir). This skill does not move specs into the sprint folder.

Discover `{root}` from `context/INDEX.md`, else `docs/INDEX.md`. Read `{root}/.ai-native.yml` for `board`, `default_branch`, `tracker`, and `packs`. Sprint notes, when present: `{root}/sprint-planning/<sprint>/` (`tickets.md`, `schedule.md`, `people.md`).

Read the notes before answering a planning or status question. If a local fact is missing, say so. Do not fetch the tracker to fill the gap unless the user asks for a refresh.

## Notes and the tracker

Local notes are the working plan. They may differ from the tracker on purpose.

- **Refresh** (only when the user asks): read the tracker and reconcile tracker-owned facts. Do not write to the tracker during a refresh.
- **Write** (create, edit, comment, transition): only when the user explicitly asks in this conversation. A local edit is not a sync.
- TickTick or any personal list is out of this skill unless the project companion configures it. Do not ship personal list or task ids.

### Field ownership

| Tracker-owned (refresh may update the local copy) | Local-owned (refresh must not change) |
| --- | --- |
| issue key, type, status, assignee, sprint id, estimate as stored in the tracker, parent key | schedule dates, review-ready dates, capacity assumptions, buffers, scenario choices, sprint order overrides, feature decisions |

When a tracker-owned fact disagrees with the note, update the note's tracker-fact line and append a conflict:

```markdown
## Conflicts
- <field>: local `<value>` vs tracker `<value>` (source: <tracker kind>)
```

When a local-owned choice disagrees with the tracker, keep the local choice, append the same conflict line, and do not overwrite it. Changing a local-owned choice requires the user to authorize that change.

## Team schedule

Generalize from the project's own units. Do not copy another team's names, dates, ids, or formulas. Do not invent capacity.

- **Membership and order** live in `tickets.md` and `schedule.md`. A feature may span sprints. Moving a ticket between sprints does not move or copy its contract.
- **Carry-over** stays visible. Do not count it in the current sprint's load, and do not include another sprint's tickets in this sprint's totals.
- **People** (`people.md`): availability, capacity, estimates, and assigned load. Derive figures from configured units, the calendar or availability the user stated, and named assumptions.
- **Review-ready** is not the sprint end. Record the project's implementation and merge deadlines, and time for QA or acceptance, separately from the sprint end date.
- **Scenarios**: multi-sprint scope, alternative capacity assumptions, optional scope, and explicit buffers. Show the assumptions and the overload. Do not hide them in one total.
- **Parent/child**: group with parent keys and blocked-by links. Do not invent nested ticket directories.
- A sprint accounting label (done for this sprint's load) is not feature merge and does not promote decisions.

## Tracker support

Load mappings from `tracker` in `.ai-native.yml`. Jira is the first supported kind: see [jira.md](jira.md). The profile supplies site, project, issue types, fields, statuses, estimates, owners, sprints, and hierarchy. No ids or people are hardcoded here.

Check `tracker.capabilities` before hierarchy, sprint, estimate, or owner operations. If a capability is missing, say what is unsupported. Do not make another tracker mimic Jira. `kind: markdown` needs no tracker call. Any other kind is an extension point: explain that no adapter is shipped, and keep the local notes as the record.
