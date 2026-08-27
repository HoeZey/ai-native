# AI-native

Private catalog: **10x process skills**, **scrum-master**, **ship-ticket**, plus **init/upgrade** for a `context/` (or `docs/`) working-memory layer.

Not on skills.sh. Install with git auth:

```bash
npx skills add git@github.com:HoeZey/ai-native.git
npx skills update -g
```

Pin a release tag when one exists: `npx skills add git@github.com:HoeZey/ai-native.git#v0.1.0`

In a consumer repo:

```bash
/ai-native-init
# default --root context  (pass --root docs if the contract should live in docs/)
```

That writes INDEX + ticket dirs, a thin alwaysApply rule that **names** `/10x-engineer` then `/10x-<slug>`, graft MCP, `.cursorignore`. It does not copy this catalog into the project.

`/ai-native-upgrade` refreshes protocol files from `context/.ai-native.yml` (or `docs/.ai-native.yml`). Never tickets or INDEX `current`.

## Layout

- `skills/` — what `npx skills add` installs
- Init templates live under `skills/ai-native-init/templates/` so they ship with the skill
- `REFERENCES.md` — human credits (Matt / BONDage). Not loaded as a skill.

## Versioning

`main` is the release branch. Feature branches from `main`. Merging conventional commits to `main` opens a **release-please** PR that updates `CHANGELOG.md` and the version; merging *that* PR tags `vX.Y.Z`.

## Default branch of *this* repo

`main`. Consumers choose their own `--default-branch` (Quota uses `develop`).
