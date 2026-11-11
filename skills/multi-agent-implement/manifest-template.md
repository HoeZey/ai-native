# Manifest template

During /multi-agent-implement plan, fill this template and write it to
.runs/<run-id>/manifest.md. Do not branch, worktree, or launch.

/multi-agent-implement run takes that path. It records the file's SHA-256 at
preflight and executes only that file. It does not read ~/.cursor/plans/.
Execution never edits the manifest.

Replace every {slot}.

## Identity

- run-id: {date}-{slug}
- repository root: {absolute path}
- created: {ISO-8601}

## Git

- delivery-base branch: {branch}
- delivery-base SHA (full 40): {sha}
- program branch: {branch}
- stable branch: {branch or none}
- worktree layout: {repository rule or path pattern}

## Board

References may be local paths, provider keys, or URLs.

| id | title | issue reference | PRD reference | blocked_by |
|---|---|---|---|---|
| {id} | {title} | {reference} | {reference} | {ids or empty} |

## Checks

| story | focused commands | production factory/handler if touched |
|---|---|---|
| {id} | {commands} | {symbol/path or none} |

- full integration commands: {commands}
- required user-path smoke: {path and method, or none}
- isolated smoke resources: {ports/data paths the agent may use}

## Protected and allowed

- user checkout: {absolute path}
- protected processes / ports / data: {or none}
- allowed local writes: {exact paths/actions}
- allowed external writes: {exact actions or none}
- allowed live mutations: {exact actions or none}
- follow-up issues for out-of-scope findings: {allowed path/provider, or no}
- push: no unless the user later says yes
- delivery/stable promotion: no unless the user later says yes

## Agent

- model preference: {or default}
- max parallel implementers: {number}
- max parallel reviewers: {number}
- review round budget per story: {number, default 6}

## Fix forward and completion

- triage every failed check, finding, smoke failure, and conflict per
  SKILL.md Triage;
- fix every fixable item, including check failures already on the base, and
  in-scope majors and minors; record nits;
- park a story only for a human-only class: contract, permission, no
  progress (same finding after 2 remediations, or no blocking drop for 2
  rounds), budget, or infrastructure after 2 safe retries;
- a parked story does not stop other runnable stories;
- smoke exercises every acceptance path the isolated resources allow; each
  unexercised path has a stated reason;
- complete only when every manifest story is integrated, full checks pass,
  final program review is green, no fixable item is open, and user-path
  state is explicit;
- one integrator invocation per accepted wave, resuming the same integrator
  after its first launch and as program fixer;
- never merge story branches into each other.

## Notes

{anything the coordinator must not infer}
