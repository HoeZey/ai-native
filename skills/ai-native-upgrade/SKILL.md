---
name: ai-native-upgrade
description: >-
  Refresh AI-native protocol files (alwaysApply rule, graft.mdc, .cursorignore,
  TOOLS.md) from pack templates using context/.ai-native.yml or docs/.ai-native.yml.
  Use when the user says /ai-native-upgrade or "sync the ai-native protocol".
  Never tickets, board cards, or INDEX current.
disable-model-invocation: true
---

# AI-native upgrade

Protocol files only. Instance data stays put.

## Do

1. Confirm the consumer repo root.
2. Run:

```bash
python3 scripts/upgrade.py --target <repo-root>
```

This skill's `scripts/upgrade.py` calls the sibling `ai-native-init` templates. Both skills must be installed from the same catalog.

3. Show stdout. The script refreshes pack-owned protocol and the generated adapter region. It keeps `.ai-native.yml` keys (including ones it does not recognize), the adapter's project region, and `<slug>-project.mdc`. An incompatible value is written to `{root}/upgrade-review.md` and the profile is left as it was.
4. Do not rewrite ticket trees, `board.md` cards, or INDEX `current` / `phase` / `ticket`.
5. Stop. Catalog version itself is `npx skills update -g`, via `scripts/select-pack.py` so the saved packs are what get installed. A bare `npx skills add` is not the `all` preset.
