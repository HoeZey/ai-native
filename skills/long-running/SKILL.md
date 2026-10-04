---
name: long-running
description: >-
  Coordinate an approved multi-story program in one chat: plan a frozen
  manifest, keep a visible scoreboard and timestamped log, run nested
  implement/review/integrate waves on a dedicated program branch, and stop
  with an explicit next action. Use when the user says /long-running,
  long-running plan, long-running run, overnight, unattended, many stories,
  PROGRAM-PLAN, or BUILD-PROGRAM.
disable-model-invocation: true
---

# Long-running

Coordinator for many already-sliced stories. Not another planning system.
Grill, PRD, and issues stay the 10x contract.

Two invocations:

- /long-running plan — PROGRAM-PLAN. Fill the manifest from
  manifest-template.md and write it to .runs/<run-id>/manifest.md. Stop.
  Do not branch, worktree, or launch.
- /long-running run <manifest-path> — BUILD-PROGRAM. Fresh Agent-mode chat.
  The path is .runs/<run-id>/manifest.md inside the repository. Execute
  only that file.

Solo implement/review behavior stays unchanged. Under BUILD-PROGRAM, fresh
subagents provide isolation inside the coordinator chat.

## References

- [manifest-template.md](manifest-template.md)
- [scoreboard-template.md](scoreboard-template.md)
- [prompts.md](prompts.md)

## Run directory

```text
.runs/<run-id>/
  manifest.md
  scoreboard.md
  events.log
  field-guide.md
  summary.txt
```

Keep .runs local through an existing ignore rule or Git exclude. Do not edit a
tracked ignore file without approval.

scoreboard.md is authoritative state. events.log is audit history.
Conversation memory is neither.

## Manifest

PROGRAM-PLAN fills the template and writes .runs/<run-id>/manifest.md. It
records repo root; pinned delivery base; program branch; local or external
PRD/issue references and blockers; story/integration/smoke checks; protected
resources; allowed writes; model/concurrency preference; stop/completion/promotion
rules. It does not branch, worktree, or launch.

That file is the manifest. BUILD-PROGRAM takes its path, records its SHA-256
at preflight, and executes only that file. It does not read ~/.cursor/plans/.
It does not write or follow a second execution plan. A later change to the
manifest stops execution until the user accepts the changed file. Execution
never edits it.

## Preflight

Before the first Task:

1. Verify root, pinned base SHA, the manifest file's SHA-256, an acyclic
   blocker graph, and contract references. The manifest path must be inside
   the repository.
2. Record dirty user-checkout files without changing them.
3. Read repository worktree setup and Cursor worktree limits.
4. Record protected resources, permissions, and allowed writes.
5. Create the program branch and worktree without switching the user checkout.
6. Copy the scoreboard template, list every story, append preflight to log.

Mismatch stops before launch.

## Wave loop

A wave is dependency-ready stories up to manifest concurrency.

1. Claim stories; freeze Scope and acceptance criteria.
2. Create story branches/worktrees from the same immutable program head.
3. Launch one implementer per story using prompts.md.
4. Require focused checks and committed head SHA.
5. If production composition changed, require a test through the real factory
   or handler before review. Inner-adapter tests alone do not pass this gate.
6. Launch read-only Standards and Spec reviewers directly, in parallel,
   against the same base/head. Keep axes separate.
7. Allow one remediation and one fresh second review. A second block stops
   that story.
8. Launch one integrator for accepted stories in the wave; resume the same
   integrator for later waves. Squash onto the program branch using repository
   commit rules.
9. Run integration checks and required isolated user-path smoke before
   unlocking dependants.

After all waves, run a fresh two-axis review over delivery-base...program-head
against all manifest contracts.

After every subagent, continue or show:

```text
RUNNING | WAITING_PERMISSION | STOPPED
on: <story or gate>
next: <specific action>
```

Subagent completion alone never ends the coordinator chat.

## Nested roles

Read implement, tdd, and code-review as nested roles. Do not rewrite TDD or
the two-axis split.

- Implementer: one story, no redesign, focused checks, commit, return
  SHA/checks/risks. No review or new-chat handoff.
- Axis reviewer: one axis, under 400 words, findings only, no patch or
  implicit publish.
- Remediation: only blocking findings from the last review.
- Integrator: accepted wave SHAs, frozen contracts, current program head.

## State and recovery

Keep every planned story visible in scoreboard.md. Per row: id, status,
parent/head SHA, worktree, agent reference, review result, checks,
fixture-green, user-path-green, next.

Append one ISO-8601 line to events.log for preflight, claims, starts/ends,
reviews, remediation, gates, integration, smoke, permissions, compaction,
stops, and completion.

field-guide.md holds 1–3 line run-specific surprises. Inject it into later
prompts. It is not a cross-run lessons file.

After compaction or a new run chat, read manifest.md, scoreboard.md, Git,
field-guide.md, and recent events.log lines. Reconcile active rows and agent
references before launching. Do not infer state from transcript memory.

## Gates

- PRD/issue is the contract. No redesign.
- Parallelism only from blocked-by; story branches never merge each other.
- Focused checks per story; full checks at integration and completion.
- Standards and Spec stay separate.
- Record fixture-green and user-path-green separately. Do not describe
  required skipped user-path work as complete.
- Smoke uses isolated manifest-approved resources.
- No undeclared write, push, promotion, process termination, or worktree
  deletion.
- Complete only when every manifest story is accounted for, full checks and
  final program review pass, and user-path state is explicit.

## Stop classes

- Gate — second blocking review, failed required check, contract conflict.
- Permission — WAITING_PERMISSION; name the exact approval needed.
- Infrastructure — retry once with documented safe correction, else STOPPED.
- Compaction — recover from artifacts and continue; not a stop.
- User return — continue unless the user pauses or redirects.

Every terminal stop updates scoreboard, events.log, and summary.txt, then
names the next human action. summary.txt records elapsed time, event/story/
review/remediation counts, checks, user-path state, program head, and exact
stop or next action.

## Hard nos

- No launch without a manifest file inside the repository.
- No read of ~/.cursor/plans/ during BUILD-PROGRAM.
- No second execution plan. The manifest is the only run contract.
- No user-checkout switch.
- No undeclared external or live mutation.
- No push or promotion unless explicitly authorized. Feature-decision promotion and tracker transitions need that authorization named in the manifest. Program completion is not merge evidence for a feature.
- No silent stop after subagent completion.
- No COMPLETE while manifest work remains.
- No run-state or integration helper in v1. Add automation only after logs
  prove a recurring failure.
