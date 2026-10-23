# Scoreboard {run-id}

Copy to .runs/<run-id>/scoreboard.md at preflight. This file is authoritative
run state. Keep every planned story visible, including remaining todo rows.

```text
status: PLANNING | RUNNING | WAITING_PERMISSION | STOPPED | COMPLETE
on: {story id, gate, or none}
next: {specific action}
program_branch: {branch}
program_head: {full sha}
program_worktree: {absolute path, or removed}
manifest_sha256: {hash}
delivery_base: {branch}@{full sha}
started: {ISO-8601}
updated: {ISO-8601}
```

## Stories

Status: todo, claimed, implementing, review, remediating, accepted, blocked,
stopped.

| id | status | parent | head | worktree | agent | review | checks | fixture | user-path | next |
|---|---|---|---|---|---|---|---|---|---|---|
| {id} | todo | | | | | | | | | |

## Waves

| wave | parent | stories | integrated_at | program_head |
|---|---|---|---|---|
| 1 | {sha} | {ids} | | |

## Stops

| when | class | on | next human action |
|---|---|---|---|
