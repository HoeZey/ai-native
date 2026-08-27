# References

Human-facing credits. Skills do not include this file; agents should not load it.

## Process skills (10x)

Inspired by [Matt Pocock's skills](https://github.com/mattpocock/skills) (grill, wayfinder, spec, tickets, implement-as-orchestrator) and Theo Depraetere’s [BONDage](https://www.linkedin.com/feed/update/urn:li:activity:7463151557669228546/) write-up.

Local deltas in this catalog:

- `tdd` keeps **Beck** (refactor while green). Later Matt `tdd` is red-green only.
- `10x-engineer` still defaults to **Jira**. Markdown-board / `context/` remaps live in the generated `10x-<slug>` adapter, not in the router.
- `code-review` is report-only (two axes: Standards vs Spec).
- `ship-ticket` closes a markdown board after merge; Jira-only repos skip it.
- `scrum-master` is a solo PM loop (WIP 1, INDEX is not the board).

## Memory layer

Ticket-dir contract (`INDEX.md` spec + `plan.md` implementer SoT), INDEX router with `layout` as a parameter, `.cursorignore` (not ripgrep `.ignore`) for gitignored graft/context trees. Worked through personal repos (Jarvis, Quota) after a Braid-shaped `epics/` pack.

## Graft

Context graph CLI (`graft mcp`, `graft ask`, `graft build`). Protocol file is `graft.mdc` in the init templates.
