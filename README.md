# AI-native

Private catalog of 10x process skills, plus **init/upgrade** for a `context/` (or `docs/`) working-memory layer. Presets are `engineering`, `planning`, and `all`. `scrum-master` stays in the repo and is not part of any preset.

Not on skills.sh. There is no `npx skills --pack` flag. From a clone of this repo, print the install command for a preset:

```bash
python3 scripts/select-pack.py --preset engineering
python3 scripts/select-pack.py --preset planning
python3 scripts/select-pack.py --preset all
```

Run the printed `npx skills add ... --skill ...` command. It installs that preset through the existing git distribution.

A bare `npx skills add git@github.com:HoeZey/ai-native.git` installs every directory under `skills/`, including `scrum-master`. That is not the `all` preset.

Update an install with `npx skills update -g`. To add or remove a pack in a consumer repo without switching the selection to `all`:

```bash
python3 scripts/select-pack.py --target <repo> --add planning
python3 scripts/select-pack.py --target <repo> --remove planning
```

The script updates `packs` in `.ai-native.yml` and prints skills to install. It does not delete skills. Shared skills that another selected pack still needs stay required. Skills that are not in this catalog are left alone.

Pin a release tag when one exists by adding `#v0.1.0` to the git URL in the printed command.

In a consumer repo:

```bash
/ai-native-init
# default --root context  (pass --root docs if the contract should live in docs/)
```

That writes INDEX + a feature ticket dir, a thin alwaysApply rule that **names** `/10x-engineer` then `/10x-<slug>`, graft MCP, `.cursorignore`. It does not copy this catalog into the project. Default layout is `features`. Default `--packs engineering` does not seed `sprint-planning/`. Pass `--packs planning` or `--packs all` when the schedule should be seeded. Pass `--layout sprints` for the older shape. `sprints`, `epics`, and `flat` stay available.

`/ai-native-upgrade` refreshes pack-owned protocol files and the generated adapter region from `context/.ai-native.yml` (or `docs/.ai-native.yml`). It keeps project settings, the adapter's project region, and `<slug>-project.mdc`. It does not rewrite ticket trees or INDEX `current`.

`npx skills update -g` refreshes `~/.cursor/skills`. A same-named skill under a consumer repo's `.cursor/skills/` shadows the global one, so do not vendor this catalog inside a product repo.

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
