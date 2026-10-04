---
name: ai-native-init
description: >-
  Seed the AI-native memory layer (context/ or docs/ INDEX, ticket dirs,
  alwaysApply rule, graft MCP) and generate a 10x-<slug> adapter. Use when
  the user says /ai-native-init, "init ai-native", or "seed working memory".
  Run scripts/init.py; do not invent the tree by hand.
disable-model-invocation: true
---

# AI-native init

Seed working memory into the **current git repo**. Do not copy Quota or Jarvis docs. Do not write INDEX/README from memory — run the script.

## Preconditions

- `/10x-engineer` is installed (this catalog). If missing, from a catalog clone run `python3 scripts/select-pack.py --preset engineering` and use the printed command. A bare `npx skills add` is not the `all` preset.
- Cwd is a git repo. Stop if not.

## Parameters (inspect first)

Read an existing `{root}/.ai-native.yml`, adapter, and `.cursor/rules/<slug>-project.mdc` before asking. Reuse recorded `packs`, `decision_policy`, `tracker`, and branch. Ask only for material choices that are still missing.

| Flag | Default | Notes |
|------|---------|--------|
| `--root` | `context` | `docs` if they already want the contract in `docs/` |
| `--layout` | `features` | `sprints`, `epics`, or `flat` |
| `--clone` | `personal` | `work` gitignores `{root}/` |
| `--default-branch` | `main` | e.g. `develop` |
| `--slug` | (required) | `10x-<slug>` + rule filename |
| `--board` | `markdown` | `jira` skips markdown board files and records a `tracker` object |
| `--packs` | `engineering` | `planning`, `all`, or `engineering,planning`. Sprint notes are seeded only when planning or all is included. Stored as given — `engineering,planning` is not rewritten to `all` |
| `--decision-policy` | `preliminary_until_feature_merge` | `locked_on_record` keeps an existing locked store. Do not set that to change another repo's policy |
| `--tools` | `graft,github` | add `godot` / `atlassian` |
| `--index-keys` | `none` | `scenes` or `alembic` |
| `--github-repo` | empty | `HoeZey/quota` |

## Do

1. Confirm parameters back in one line.
2. Run from this skill directory:

```bash
python3 scripts/init.py --target <repo-root> --slug <slug> [flags]
```

`scripts/init.py` lives next to this `SKILL.md` after `npx skills add` (`~/.cursor/skills/ai-native-init/scripts/init.py`). If you are in the catalog clone, same relative path.

3. Show the script stdout. Do not hand-edit seeded protocol files in the same turn unless the script failed.
4. If graft is on PATH: `graft build` in the target repo.
5. Stop. Next is `/implement S00-01` in a **new** chat, or the human reviews the tree.

## Do not

- Invent `.tscn` filenames or alembic revision ids
- Copy `epics/` into the alwaysApply rule
- Spawn `/implement` as a Task from this chat
- Overwrite an existing INDEX `current` (script skips INDEX if present unless `--force`)
