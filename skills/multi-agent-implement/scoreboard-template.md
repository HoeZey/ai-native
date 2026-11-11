# Scoreboard {run-id}

Copy to .runs/<run-id>/scoreboard.md at preflight. This file is authoritative
run state. Keep every planned story visible, including remaining todo rows.
Ticket mode uses one story row and sets the program fields to none.

```text
status: PLANNING | RUNNING | WAITING_PERMISSION | STOPPED | COMPLETE
on: {story id, gate, or none}
next: {specific action}
program_branch: {branch or none}
program_head: {full sha or none}
program_worktree: {absolute path, removed, or none}
manifest_sha256: {hash or none}
delivery_base: {branch}@{full sha}
round_budget: {number}
started: {ISO-8601}
updated: {ISO-8601}
```

## Stories

Status: todo, claimed, implementing, review, remediating, accepted, parked,
integrated, stopped.

| id | status | round | open findings | parent | head | worktree | agent | review | checks | fixture | user-path | next |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {id} | todo | 0 | | | | | | | | | | |

## Waves

| wave | parent | stories | integrated_at | program_head |
|---|---|---|---|---|
| 1 | {sha} | {ids} | | |

## Recorded, not fixed

| when | story or gate | kind (nit / out-of-scope) | finding | follow-up |
|---|---|---|---|---|

## Stops

Class: contract, permission, no-progress, budget, infrastructure.

| when | class | on | next human action |
|---|---|---|---|
