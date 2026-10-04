---
name: grill-me-with-docs
description: >-
  Run the grill-me loop while grounding every question in CONTEXT.md and ADRs,
  updating the glossary inline. Use when the user says "grill me with docs",
  "grill-with-docs", or works in a mature codebase with established conventions.
---

# Grill Me (with docs)

Same loop as `grill-me` (one question per turn, ungrillable → `prototype`, design tree), calibrated to the project's language and past decisions.

## Prerequisites

- **`CONTEXT.md`** — glossary only (no implementation, no spec).
- **Decision records** — final history, when it exists, is `{root}/decisions/` (or a legacy `docs/adrs/` / `docs/adr/` folder). In-flight choices are not written there under the pack default. `root` comes from `context/` or `docs/` INDEX.

If neither exists, ask once: *"No CONTEXT.md or ADRs found — scaffold as we go, or run plain `grill-me`?"*

## Workflow

1. Read `CONTEXT.md` and the ADR index before the first question. Use the project's terms.
2. Run the `grill-me` loop (see that skill). Challenge terms that conflict with the glossary immediately.
3. **Update `CONTEXT.md` inline** when a term resolves — one-line definition + example. Show the diff before writing. Do not batch until the end. Do not put implementation in the glossary.
4. **Record a decision** only when **all three** are true:
   - hard to reverse
   - surprising without context
   - the result of a real trade-off
   Read `{root}/.ai-native.yml` `decision_policy` when that file exists.
   - `locked_on_record`: write where the project adapter or companion rule says. Do not rewrite an existing record. Supersede if that project already does; otherwise stop and ask. Do not move records into a new tree.
   - `preliminary_until_feature_merge`, or the key is absent and no project instruction locks the store: on `layout: features`, add or update `features/<feature>/decisions/<id>.md` with status `preliminary`. Do not create an accepted file under `{root}/decisions/`. On `sprints` or `epics`, update that folder's `decisions.md` log. On `flat`, record the choice in the handoff or ticket plan, not as accepted history.
   If you replace a record, update references that cite the old id.
5. Close with the same decisions log as `grill-me`, plus `CONTEXT.md` additions and preliminary records touched. Do not list them as accepted ADRs.

Skip the record if any of the three is missing. Most sessions add glossary lines and few or no decisions.
