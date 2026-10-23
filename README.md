# AI-native

Private catalog of 10x process skills, plus **init/upgrade** for a `context/` (or `docs/`) working-memory layer.

## Install

```bash
npx skills add git@github.com:HoeZey/ai-native.git -g
```

That installs into `~/.agents/skills/<skill-name>` and asks which skills to include. `-g -y` installs the whole catalog with no prompts. Add `#vX.Y.Z` to the git URL to pin a release (`v1.1.0` is the current tag).

One skill:

```bash
npx skills add git@github.com:HoeZey/ai-native.git --skill implement -g -y
```

In a consumer repo:

```bash
/ai-native-init
# default --root context  (pass --root docs if the contract should live in docs/)
```

That writes INDEX + a feature ticket dir, a thin alwaysApply rule that **names** `/10x-engineer` then `/10x-<slug>`, graft MCP, `.cursorignore`. It does not copy this catalog into the project. Default layout is `features`. Default `--packs engineering` does not seed `sprint-planning/`. Pass `--packs planning` or `--packs all` when the schedule should be seeded. Pass `--layout sprints` for the older shape. `sprints`, `epics`, and `flat` stay available.

`/ai-native-upgrade` refreshes pack-owned protocol files and the generated adapter region from `context/.ai-native.yml` (or `docs/.ai-native.yml`). It keeps project settings, the adapter's project region, and `<slug>-project.mdc`. It does not rewrite ticket trees or INDEX `current`.

`npx skills update -g` refreshes `~/.agents/skills`. A same-named skill under `~/.cursor/skills` or a consumer repo's `.cursor/skills/` is the copy that runs.

## Working memory

This catalog dogfoods its own stack. Tickets, board, and INDEX live under [`context/`](context/). **Do not use GitHub Issues for ticket AC.**

## Layout

- `skills/` — what `npx skills add` installs
- Init templates live under `skills/ai-native-init/templates/` so they ship with the skill
- `context/` — committed working memory (features, sprint-planning, board, INDEX)
- `REFERENCES.md` — human credits (Matt / BONDage). Not loaded as a skill.

## Versioning

`main` is the release branch. Feature branches from `main`. Merging conventional commits to `main` opens a **release-please** PR that updates `CHANGELOG.md` and the version; merging *that* PR tags `vX.Y.Z`.

## Default branch of *this* repo

`main`. Consumers choose their own `--default-branch` (Quota uses `develop`).
