# Collect portable skills, selectable packs, and project adaptation

## Status

This file is the plan. `.handoff/collect-portable-skills.md` is an older draft and must not be copied forward.

Resolved in the repair (these win over any older "open" wording below):

- **Packs.** `scripts/select-pack.py` prints `npx skills add <repo> --skill ...` for `engineering`, `planning`, or `all`. There is no `npx skills --pack` flag. `all` is the union of the two presets, not every directory under `skills/`. `scrum-master` is excluded from every preset and its source stays. Selection is the `packs` list in `.ai-native.yml`. `--add planning` stores `engineering,planning` and does not rewrite that to `all`. Removing a pack keeps skills the other pack still needs and does not delete skills outside the catalog.
- **Membership.** Engineering is the build/review route plus init, upgrade, and ship-ticket. Planning adds `sprint-planning` and shares the overlapping skills. `grill-plan` is not in the catalog. Nested ticket directories are still not a schema: parent/child grouping is links.
- **Decision policy.** `decision_policy` in `.ai-native.yml`: `preliminary_until_feature_merge` (pack default for new setups) or `locked_on_record`. Features layout uses `features/<feature>/decisions/<id>.md`. Sprints and epics keep the folder `decisions.md` log. Flat layout does not gain a feature tree. Accepted history is immutable; supersede it. Promotion is explicit and needs positive merge evidence. One ticket close does not promote. Braid's locked store is not edited by this repo.
- **Completion.** `ship-ticket` closes a merged markdown ticket, or updates a local ticket without creating a board when the tracker is external. Tracker writes stay explicit. Sprint accounting labels are not merge evidence.
- **Upgrade.** Pack-owned adapter text sits between generated markers. Project notes sit between project markers and survive upgrade. `<slug>-project.mdc` is created once and not overwritten. Unknown `.ai-native.yml` keys are kept. An unsupported recognized value is reported in `{root}/upgrade-review.md` and the file is not rewritten.

Still open: whether a future consumer wants nested story/subtask directories. Do not add them until that is decided. S00 in this repo stays unshipped.

## Handoff scope and status

The sections below are the settled direction plus the history of the open questions. Where they disagree with **Status**, Status wins.

Bring generic user-wide skill improvements and long-running's four files into this Git-distributed catalog. Offer engineering, planning, and all packs. Separate feature contracts from sprint scheduling, use the Connection Designer team workflow as the planning baseline, and adapt shared workflows through project configuration rather than copied project rules. Preserve legacy layouts and project-owned policies.

Do not fold this work into S00-01: that ticket remains the memory-layer seed. The future migration of this repo's S00 work is described below; it does not ship either seed ticket.

## Distribution and pack selection

**Settled:** keep the private Git distribution and existing update channel documented in [README.md](README.md):

```bash
python3 scripts/select-pack.py --preset engineering
npx skills update -g
```

`npx skills` supports individual `--skill` selections; this does **not** establish a native `--pack` option. `scripts/select-pack.py` is the repository-owned preset entry. It prints `npx skills add <repo> --skill ...` for `engineering`, `planning`, or `all`. Do not document a fabricated `npx skills add --pack ...` command. A bare `npx skills add <repo>` installs every directory under `skills/`, including `scrum-master`, and is not the `all` preset.

One canonical skill source may belong to more than one pack. Ship supporting resources and required workflow dependencies with the selected skills, without installing every pack. Engineering-only consumers must be able to build and review work without sprint planning, planning artifacts, or missing planning skills. Audit routing and dependencies, especially `implement`'s conditional `ship-ticket` handoff and `ai-native-upgrade`'s reliance on init templates. Do not solve missing dependencies by silently selecting `all`.

**Resolved:** see Status. Membership is the lists in `skills/ai-native-init/scripts/profile.py`. `to-issues` and `wayfinder` are in both presets. `ship-ticket`, init, and upgrade are shared support. `sprint-planning` is planning-only. `grill-plan` is not in this catalog. The candidate list below is history, not a second inventory.

- Engineering candidates: `10x-engineer`, `write-a-prd`, `grill-me`, `grill-me-with-docs`, `prototype`, `implement`, `tdd`, `diagnosing-bugs`, `code-review`, `qa`, `research`, `handoff`, and `long-running`.
- Overlap needing a membership decision: `to-issues` (PRD into vertical Jira stories), `wayfinder` (decision tickets), and Connection Designer's `grill-plan` (reviewable plan and question/decision record).
- Shared support candidates: init, upgrade, and completion, including whether and how `ship-ticket` participates.

Presence in a source directory is inventory evidence, not evidence of regular use. The actively used planning baseline is the Connection Designer sprint workflow, not this list alone.

**Exclude `scrum-master` from every distributed pack, including `all`.** It is the user's Quota solo PM; this is not authorization to delete its source. Audit/remove portable requirements and generated references to it, including the `10x-engineer` standup route and adapter WIP guidance. Do not impose solo WIP rules on team workflows. Clarify how selectable installs enforce this exclusion, since an unfiltered catalog install must not accidentally become the new `all` preset.

Cursor uses installed skills rather than `node_modules`. Same-named project-local `.cursor/skills/` copies can shadow global skills. Document the existing update path and shadowing behavior, alongside the eventual preset mechanism.

## Generic skill imports and exclusions

Add [skills/long-running/](skills/long-running/) from the four user-wide files: `SKILL.md`, `manifest-template.md`, `scoreboard-template.md`, and `prompts.md`. Keep them product-agnostic.

Compare `~/.cursor/skills` against the catalog again before applying imports. The original comparison found `handoff`, `qa`, `research`, `to-issues`, and `write-a-prd` identical; leave identical files alone, but audit even unchanged skills for pack dependencies and project assumptions.

- [10x-engineer](skills/10x-engineer/SKILL.md): keep the PROGRAM-PLAN / BUILD-PROGRAM route, the phase-exit paste, and the “commit when green / long-running for many stories” rules. Keep `context/` or `docs/` discovery. The `/scrum-master` standup route is removed. Completion follows the project board and `default_branch`.
- [implement](skills/implement/SKILL.md) and [code-review](skills/code-review/SKILL.md): import generic nested BUILD-PROGRAM clauses. Nested review does not publish unless the frozen manifest explicitly names that authorized write; tracker writes also require an explicit user request. Review remains report-only.
- [tdd](skills/tdd/SKILL.md): import overlapping-test collapse rules.
- Smaller differences in `grill-me`, `grill-me-with-docs`, `diagnosing-bugs`, `prototype`, and `wayfinder`: take generic wording only.
- Preserve [ship-ticket](skills/ship-ticket/SKILL.md)'s `context/` discovery; the user-wide docs-only copy would lose it. Its pack placement and role in generalized completion are open.

Keep these out of generic distributed workflows:

- Guided PR review app behavior, vendored `docs/prds/` assumptions, and `CodeReviewOutcome` publication to `localhost:8765`. Its publisher belongs in that product's local skill/rule.
- Project-specific Connection Designer debugging/tool setup and comment-resolution skills (`debug-azure`, `local-debug`, `cursor-setup`, etc.). `create-jira-ticket` is a qualified exception: its reusable creation, parent association, and sprint-assignment behavior may inform the first Jira adapter after removing project-specific configuration and verifying actual tool capabilities. Do not copy its IDs, assumptions, or tool limitations as universal facts.
- `caveman`, `stacked-prs`, and `resolve-merge-conflicts`, which were not catalog skills; personal rules such as `caveman.mdc`, `ponytail.mdc`, and `commits.mdc`.

Do not blindly import Connection Designer's rules. Extract general behavior into shared skills, leave project conventions in project instructions, and keep personal TickTick behavior separate and optional.

## Planning baseline: Connection Designer's team workflow

**Settled:** the planning pack supports the actively used team workflow, including:

- Feature scope/contracts, preliminary decisions, and progress; ticket breakdown, dependencies, and parent/child grouping.
- Ownership, sprint membership and order, and carry-over. Keep carried work visible without counting it twice or including another sprint's work in current-sprint totals.
- People availability, capacity, estimates, and assigned load. Derive figures from configured units, calendars/availability, and stated assumptions; do not invent capacity or hardcode one team's formulas.
- Review-ready timing separately from sprint-end dates, with project-defined implementation/merge deadlines and time for QA or acceptance.
- Multi-sprint scope/budget scenarios, alternative capacity assumptions, optional scope, and explicit buffers. Expose assumptions and overload rather than hiding them in a single total.

This replaces the old blanket exclusions of Jira fetches, capacity planning, and story-point math. Capacity spreadsheets are not mandatory; the workflow must support the calculations and scenarios regardless of the eventual artifact format. Connection Designer's numbers, staffing, dates, holidays, and buffer policy are examples to generalize, not portable defaults. QA inclusion and status interpretations belong to project settings.

Local notes hold the working plan and may intentionally differ from tracker indicators. Read notes first for planning/status questions. An explicit refresh reads the tracker and reconciles relevant facts into notes; missing local data should be surfaced rather than silently triggering a tracker fetch. Only explicit user requests authorize external creation, edits, comments, or transitions. A local plan change does not automatically synchronize Jira or a personal planner. Optional TickTick integration has its own configuration and authorization; no personal list/task IDs ship in generic assets.

## Tracker adapters

**Settled:** generic user-facing planning workflows load tracker-specific supporting instructions and mappings through project configuration. Ship Jira support first; Linear and other trackers are extension points, not promised implemented support. Prefer a few generic workflows over many tracker-specific user commands.

The Jira configuration must cover instance/project, issue types, fields, statuses, estimates, owners, sprints, and story/subtask mappings. No hardcoded TCD IDs, people, dates, or project names in generic assets. Generalize useful behavior from `create-jira-ticket` rather than distributing its project-bound configuration.

Adapters declare capabilities, such as hierarchy, sprint membership, estimates, and permitted operations. Workflows check these capabilities and explain unsupported operations; do not force a tracker to mimic Jira hierarchy or sprints. Markdown/local tracking remains supported. Tracker-specific supporting instructions are `skills/sprint-planning/jira.md`. The project `tracker` object supplies concrete mappings. Field ownership and conflicts are in `skills/sprint-planning/SKILL.md`: refresh updates tracker-owned facts, keeps local schedules, capacity, and feature decisions unless a change to those is authorized, and does not write to Jira.

## Feature contracts and sprint schedules

**Settled:** durable feature scope, decisions, progress, and ticket contracts belong to features; sprint artifacts describe scheduling, membership/order, ownership/load, and review timing. A feature may span several sprints. Sprint moves must not move or duplicate its contract.

Retain `sprints`, `epics`, and `flat` compatibility. Add a feature-oriented layout for new planning-enabled setups, preserving the original direction that `features` becomes their default. Engineering-only setup need not generate sprint or other planning artifacts. Upgrades must not auto-rewrite consumer trees.

**Resolved for storage that exists today:** features use per-id files; sprints and epics keep a `decisions.md` log; flat does not grow a feature tree. Nested story/subtask directories are still an open question. Parent/child grouping is links and parent keys until that is decided. An area folder is not mandatory. The following is the separation init uses, not a nested-directory schema:

```text
<root>/features/<feature>/       contract, preliminary decisions, progress, ticket context
<root>/decisions/                final accepted/superseded history under default policy
<root>/sprint-planning/          active-sprint reference and per-sprint notes
                                membership/order, schedule/review timing, people/capacity
<root>/planning/board.md         optional Markdown tracking for projects that choose it
```

`<root>` remains project-configured (`context/` or `docs/`). Decide whether a feature `done/` directory is useful; moving a ticket there is not a settled universal closure requirement. Markdown kanban is optional, not mandatory for tracker consumers.

Likely implementation touchpoints after schema review: [init.py](skills/ai-native-init/scripts/init.py), feature layout templates under `skills/ai-native-init/templates/layouts/features/`, the [protocol README template](skills/ai-native-init/templates/protocol/README.md.tmpl), [adapter template](skills/ai-native-init/templates/adapter/SKILL.md.tmpl), [dogfood adapter](.cursor/skills/10x-ai-native/SKILL.md), and completion discovery in `ship-ticket` or its agreed replacement/support role.

## Structured project adaptation and setup

**Settled:** use shared skills + tracker adapter + project-owned profile/settings + companion project instructions. Extend the existing `.ai-native.yml`, `/ai-native-init`, `/ai-native-upgrade`, and `10x-<slug>` adapter mechanisms; do not introduce a competing configuration system.

The structured profile holds paths/layout, tools/build/test commands, tracker mappings, merge/default branch, status/completion mappings, team/planning settings, and decision policy. Companion freeform instructions live in `.cursor/rules/<slug>-project.mdc`. The thin generated rule loads that file, `.ai-native.yml`, and the shared skills. It does not clone workflow prose. Pack-owned adapter text is the generated region; project notes are the project region.

Setup inspects existing rules and configuration, reuses known choices, asks only missing material questions, and produces reviewable configuration. It must distinguish source information from choices requiring the user. Engineering setup need not create planning artifacts. Updates preserve project-owned settings, instructions, and explicit overrides, and surface incompatible overrides rather than overwriting them. Preserve instance data, ticket state, and router current/phase/ticket during upgrades.

Connection Designer's thin rule illustrates the boundary: route through shared 10x, read local feature/ticket context before tracker context, use configured Graft/ADO tooling, write Jira only on explicit requests, report reviews, and mark done after merge to its configured branch. Its tooling and `develop` branch are project values, not generic defaults. **Do not change Braid's existing locked decision policy as part of this work.**

## Feature decision lifecycle

**Settled pack default:** feature decisions are preliminary/editable until the whole feature has merged to the configured merge/default branch. Then promote them to final accepted/superseded history. A single ticket merge does not freeze the entire feature.

- Preliminary records are the working plan. Update or replace them when a choice changes; do not block a correction merely because a preliminary decision ID exists. Keep IDs/references coherent when replacing records.
- Accepted history is immutable by default. Supersede accepted records rather than rewriting them in place.
- If a correction changes already-shipped behavior, it needs code changes as well as documentation, even while the broader feature is still preliminary.
- Projects may explicitly choose a different policy during setup or later. Record the override, have skills honor it, and preserve it on upgrade. Do not reinterpret Braid's locked store using the new pack default.

Update the future protocol, feature templates, `implement`'s “already-decided/do not reopen” wording, and final-history documentation to distinguish corrections from unsolicited redesign. `implement` still follows agreed scope; editable decisions do not authorize inventing a new feature.

**Resolved:** see Status. Features layout uses one file per id. Sprints and epics use the folder log. Promotion is a separate explicit step in `ship-ticket`, and only with the positive evidence listed there. Closing one ticket does not promote.

## Completion across local and tracker workflows

**Settled:** completion must work with Markdown or trackers. Honor project-configured merge branches and status mappings; implementation reaching acceptance criteria or review-ready is not by itself evidence of merge. Tracker reads and writes follow the explicit refresh/write boundaries above. Planning labels such as “done for sprint accounting” must not silently imply feature merge or final decision promotion.

**Resolved:** see Status and `skills/ship-ticket/SKILL.md`. Markdown closes go through `ship-ticket` after merge to `default_branch`. Tracker-only completion updates a local ticket when one exists and does not create a markdown board. Tracker writes stay explicit. Nested BUILD-PROGRAM does not close trackers or promote decisions unless the manifest names that write. Engineering completion does not require `sprint-planning`.

## Future dogfood migration: S00 into feature seed

After the feature schema is agreed, migrate this repo explicitly; consumer upgrades remain non-migrating.

- Move `context/planning/sprints/S00/{INDEX,decisions,progress}.md` into the chosen contract representation under `context/features/seed/`.
- Move `context/planning/tickets/S00-01` and `S00-02` into that feature's chosen ticket structure, preserving ticket identities, contents, dependencies, and state.
- Add `context/sprint-planning/README.md` and S00 membership/order, schedule, and minimal people notes consistent with this repo's actual setup. Do not propagate its solo rules as team defaults.
- Update [context/INDEX.md](context/INDEX.md), [context/.ai-native.yml](context/.ai-native.yml), [context/README.md](context/README.md), the dogfood rule/adapter, board links, and other references to feature `seed` and sprint `S00`. Keep this repo's existing Markdown board choice.
- Remove obsolete `planning/sprints/` and `planning/tickets/` trees only after checking references and preservation.

S00-01 and S00-02 are not shipped by this migration; nothing moves to `done/` or becomes final merely because paths changed. Preserve Q1–Q3 as preliminary feature records, revising Q1's old sprint-layout choice coherently with the agreed feature layout. Do not copy them into `context/decisions/` as accepted history.

## Cursor implementation order and validation

1. Recompare source skills and audit portable assumptions/dependencies. Review candidate pack membership, overlap, and exclusion enforcement.
2. Resolve selector/defaults, profile ownership/loading, tracker capabilities, artifact hierarchy/schema, and completion/promotion questions. Record the choices before implementing their schemas.
3. Import generic changes and long-running; implement the thin Git preset selection and supporting dependencies. Update routing to work for engineering-only consumers.
4. Extend existing init/upgrade/profile/adapter templates and build the first generalized Jira support. Generalize planning behavior without copying project or personal data.
5. Add feature layout and decision-policy handling, with explicit overrides and legacy compatibility. Migrate S00 only as the deliberate dogfood step above.
6. Update README and consumer guidance. After actual implementation, run `python3 scripts/check-skills.py` and appropriate focused checks for pack independence, legacy setup, upgrade preservation, explicit tracker boundaries, and decision policies. Search generic assets for `localhost:8765`, vendored `docs/prds` assumptions, and Braid/Tesseract identifiers; source attribution is distinct from hardcoded runtime behavior.

For this documentation edit, inspect the diff for coherence, stale contradictory requirements, and unsupported promises; do not run implementation code checks. Nothing is committed or published here. Future publishing remains release-please on `main`, followed by the existing Git update path; no second publish channel.

Follow-up outside this repo: after installing the catalog globally, deliberately remove Guided PR review's vendored generic copies so they stop shadowing global skills, retaining its project-local publisher. This plan does not authorize editing that product now.

## Read-only source references

Connection Designer sources resolve under `/Users/joselee/ml6/bbh/braid-connection-designer/`:

- `.cursor/rules/personal/sprint-planning.mdc`: notes-first status, capacity, review timing, parent/child grouping, and personal TickTick behavior to keep separate.
- `context/sprint-planning/README.md`: active-sprint routing and distinct planning/implementation timing.
- `context/sprint-planning/sprint-21-24-bulk-updates/README.md`: multi-sprint scope, ownership, estimates/load, availability, budget scenarios, and buffers.
- `.cursor/rules/personal/braid-ai-native-engineering.mdc`: thin shared-skill routing, local context, configured tools, explicit writes, report-only review, branch/status conventions, and its existing locked policy.
- `.cursor/skills/create-jira-ticket/SKILL.md`: reusable Jira creation/parent/sprint behavior requiring configuration extraction.
- `.agents/skills/grill-plan/SKILL.md`: candidate plan-interview workflow and reviewable plan/decision artifacts; membership and format remain open.

These are evidence to generalize, not files to modify or policy to replace.
