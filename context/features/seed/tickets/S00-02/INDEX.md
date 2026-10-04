---
key: S00-02
type: story
sprint: S00
status: todo
blocked_by: [S00-01]
blocks: []
create:
  - pyproject.toml / uv.lock for catalog dev tools
---

## current

- Init/upgrade scripts are stdlib-only (`pathlib`, `json`, `argparse`). CI runs `python3` compile + `scripts/check-skills.py`.
- No `pyproject.toml`, no Ruff, no pytest yet.

## ac

- Catalog repo uses **uv** for *dev/CI* Python (Ruff, pytest, later optional PyYAML for templates)
- `pyproject.toml` + `uv.lock`; CI uses `astral-sh/setup-uv` + `uv run`
- `requires-python` documents 3.12
- `init.py` / `upgrade.py` still run as `python3` with the stdlib — they never import from the lockfile

## out_of_scope

- Requiring uv (or any third-party import) on consumer machines after `npx skills add`
- Changing `/ai-native-init` to `uv run`

## notes

- GitHub Issues are not the tracker here. This dir is the ticket.
- `done` is merge to `main`, then `ship-ticket`. Implement sets `in_review`.
