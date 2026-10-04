# Manifest template

During /long-running plan, fill this template and write it to
.runs/<run-id>/manifest.md. Do not branch, worktree, or launch.

/long-running run takes that path. It records the file's SHA-256 at
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
- push: no unless the user later says yes
- delivery/stable promotion: no unless the user later says yes

## Agent

- model preference: {or default}
- max parallel implementers: {number}
- max parallel reviewers: {number}

## Stop and completion

- one remediation and one fresh second review per blocked story;
- stop a story after its second block;
- stop on failed required checks, manifest change, undeclared write, or user
  pause;
- complete only when every manifest story is accounted for, full checks pass,
  final program review passes, and user-path state is explicit;
- one integrator invocation per accepted wave, resuming the same integrator
  after its first launch;
- never merge story branches into each other.

## Notes

{anything the coordinator must not infer}
