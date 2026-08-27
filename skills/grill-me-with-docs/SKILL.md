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
- **ADRs** — `{root}/decisions/`, `docs/adrs/`, or `docs/adr/` (`root` from `context/` or `docs/` INDEX).

If neither exists, ask once: *"No CONTEXT.md or ADRs found — scaffold as we go, or run plain `grill-me`?"*

## Workflow

1. Read `CONTEXT.md` and the ADR index before the first question. Use the project's terms.
2. Run the `grill-me` loop (see that skill). Challenge terms that conflict with the glossary immediately.
3. **Update `CONTEXT.md` inline** when a term resolves — one-line definition + example. Show the diff before writing. Do not batch until the end. Do not put implementation in the glossary.
4. **Propose an ADR** only when **all three** are true:
   - hard to reverse
   - surprising without context
   - the result of a real trade-off
   ```
   {root}/decisions/NNN-short-title.md
   ── Status · Context · Decision · Consequences
   ```
5. Close with the same decisions log as `grill-me`, plus `CONTEXT.md` additions and ADRs created.

Skip the ADR if any of the three is missing. Most sessions add glossary lines and few or no ADRs.
