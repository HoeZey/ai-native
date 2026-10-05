# Glossary

Ubiquitous language for this repo. Product/process detail lives under [`context/`](context/). Decisions live under [`context/decisions/`](context/decisions/).

**AI-native** — Private skill catalog: engineering, planning, and all presets, plus init/upgrade for a `context/` (or `docs/`) working-memory layer.

**Working memory** — Committed `context/` engineering contract (INDEX, current vs ac, seams, plan.md). Not the board.

**INDEX** — Router file (`phase`, `skill`, `ticket`, `layout`). Repo: `context/INDEX.md`. Feature: `context/features/<feature>/INDEX.md`. Ticket spec: `context/features/<feature>/tickets/<KEY>/INDEX.md`. Honor those; then read that named skill.

**Feature** — Durable contract: INDEX, preliminary decisions, tickets, and `done/` after ship. Not the sprint schedule.

**Sprint planning** — `context/sprint-planning/<sprint>/`. Membership, order, and people. Not the spec.

**Preliminary decision** — `context/features/<feature>/decisions/<id>.md`. Editable until that feature merges. Not a law.

**Final decision** — `context/decisions/`. A preliminary record moves here only after the feature has merged. Supersede; do not rewrite in place.

**plan.md** — Implementer source of truth in the ticket dir (how, inlined decisions, tests). Required before `/implement` on a code slice.

**sprint.yaml** — Source for one sprint: commitment, ranked pull-in, capacity, and dates. The agent edits this file. `sprint.md` next to it is generated and read-only. Not `plan.md`.

**Seam** — Public surface the behavior is observed through. Not every file in the diff.

**current vs ac** — Already true in the tree vs this ticket. Stops agents rebuilding what exists.

**in_review** — Slice implemented, not merged. Implement must not set `done`. `done` only after merge to `main`.

**Catalog Python** — Dev/CI tooling in this repo (uv, Ruff, pytest). Not a runtime for consumer `init.py`.
