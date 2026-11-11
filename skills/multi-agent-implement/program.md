# Program mode

Many already-sliced Stories under one frozen manifest. The Story loop,
Triage, Status, Worktree close, and Nested roles in SKILL.md apply unchanged.

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

## Plan

/multi-agent-implement plan fills manifest-template.md and writes
.runs/<run-id>/manifest.md. It records repo root; pinned delivery base;
program branch; local or external PRD/issue references and blockers;
story/integration/smoke checks; protected resources; allowed writes;
model/concurrency preference; review round budget; completion and promotion
rules. It does not branch, worktree, or launch. Stop.

That file is the manifest. /multi-agent-implement run takes its path, records
its SHA-256 at preflight, and executes only that file. It does not read
~/.cursor/plans/. It does not write or follow a second execution plan. A later
change to the manifest stops execution until the user accepts the changed
file. Execution never edits it.

## Preflight

Before the first Task:

1. Verify root, pinned base SHA, the manifest file's SHA-256, an acyclic
   blocker graph, and contract references. The manifest path must be inside
   the repository.
2. Record dirty user-checkout files without changing them.
3. Read repository worktree setup and Cursor worktree limits.
4. Record protected resources, permissions, and allowed writes.
5. Create the program branch and worktree without switching the user checkout.
6. Copy the scoreboard template, list every story, set `program_worktree` to
   that absolute path, and append preflight to the log.

Mismatch stops before launch.

## Wave loop

A wave is dependency-ready Stories up to manifest concurrency.

1. Claim Stories. Create story branches and worktrees from the same immutable
   program head.
2. Run the Story loop for each claimed Story, up to max parallel implementers
   and reviewers.
3. A human-only item parks that Story with its class. Its dependants stay
   unready. The other Stories continue.
4. When every claimed Story is accepted or parked, launch one integrator for
   the accepted Stories. Resume the same integrator for later waves. Squash
   onto the program branch using repository commit rules.
5. Run integration checks and required isolated user-path smoke. Triage each
   failure. Fixable: resume the integrator as program fixer, then rerun the
   checks. A failure already present on the wave parent is fixable. Tag that
   fix `pre-existing` in events.log.
6. When integration is green, unlock dependants. Close each story worktree
   from this wave.
7. If any Story is dependency-ready, claim the next wave (step 1). Otherwise
   run the final program review.

Story branches never merge each other. Parallelism comes only from blocked-by.

## Final program review

Launch fresh Standards and Spec reviewers over delivery-base...program-head
against every manifest contract, plus the required smoke. Triage the results.
Fixable items go to the program fixer. After its checks pass, run both axes
again over the full range. Keep the program worktree until this review is
green or stopped.

Smoke exercises every acceptance path that the isolated resources allow,
including failure paths through fixtures, stubs, or fault injection on
isolated resources. A path left unexercised needs a stated reason: it needs an
undeclared live permission, or the host cannot produce the case. A smoke
failure that breaks an acceptance criterion is fixable: program fixer with a
regression test, then smoke that path again.

## Completion and stops

- COMPLETE only when every manifest Story is integrated, full checks pass, the
  final review is green, no fixable item is open, and user-path state is
  explicit.
- STOPPED only when no runnable work remains and parked Stories, or a
  human-only final-review item, need a decision. Name each question.
- WAITING_PERMISSION for the Permission class. Other Stories continue while
  they can.
- Compaction is not a stop. Recover from artifacts and continue.
- User return: continue unless the user pauses or redirects.

Every terminal state closes each run worktree whose porcelain status is empty,
including the program worktree. Leave any path that still has uncommitted
changes, and name it. summary.txt records elapsed time, event/story/review/
remediation counts, rounds per Story, fixes tagged `pre-existing`, checks,
user-path state, out-of-scope items, program head, worktrees left in place,
and the exact stop or next action.

## State and recovery

Keep every planned Story visible in scoreboard.md. Per row: id, status, round,
open findings, parent/head SHA, worktree, agent reference, review result,
checks, fixture-green, user-path-green, next.

Append one ISO-8601 line to events.log for preflight, claims, starts/ends,
reviews, triage decisions, remediation, fixes, gates, integration, smoke,
worktree removal, permissions, compaction, stops, and completion.

field-guide.md holds 1–3 line run-specific surprises. Inject it into later
prompts. It is not a cross-run lessons file.

After compaction or a new run chat, read manifest.md, scoreboard.md, Git,
field-guide.md, and recent events.log lines. Reconcile active rows and agent
references before launching. Do not infer state from transcript memory. A
worktree cell or `program_worktree` value of `removed` means that checkout is
gone. Add a new worktree only if that Story or the program still needs one.

## Gates

- Focused checks per Story; full checks at integration and completion.
- Smoke uses isolated manifest-approved resources.
- Feature-decision promotion and tracker transitions need that authorization
  named in the manifest.

## Hard nos

- No launch without a manifest file inside the repository.
- No read of ~/.cursor/plans/ during a run.
- No second execution plan. The manifest is the only run contract.
- No COMPLETE while manifest work remains.
