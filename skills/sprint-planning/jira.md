# Jira support

Use this when `{root}/.ai-native.yml` `tracker.kind` is `jira`. Mappings come from that `tracker` object: `site`, `project`, `issue_types`, `fields`, `statuses`, `hierarchy`, and `capabilities`. If `site` or `project` is empty, ask before any call. Do not invent a project key.

Atlassian MCP is the tool. Reads happen on an explicit refresh. Creates, edits, comments, and transitions happen only when the user asks for that write.

- Map parent/child with `fields.parent` when `hierarchy` is a capability. Otherwise keep the grouping in local notes and say hierarchy is unsupported.
- Map sprint membership only when `sprints` is a capability.
- Map estimates and owners through `fields.estimate` and `fields.owner`. An empty field name means it is not configured; ask, do not guess a custom field.
- Translate tracker statuses through `tracker.statuses`. An unmapped status is unknown: surface it, do not treat it as `done`.

Refresh updates tracker-owned facts listed in `SKILL.md` and writes conflicts. It does not change local schedules, capacity assumptions, or feature decisions unless the user authorizes those changes. It does not write back to Jira.
