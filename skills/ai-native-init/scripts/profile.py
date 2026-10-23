"""Pack membership, profile checks, and adapter region refresh.

`all` is the union of the engineering and planning presets. It is the
explicit lists below, not a scan of every directory under skills/.
"""

from __future__ import annotations

PACK_VERSION = "1.1.0"  # x-release-please-version

ENGINEERING = [
    "10x-engineer",
    "grill-me",
    "grill-me-with-docs",
    "prototype",
    "research",
    "handoff",
    "write-a-prd",
    "wayfinder",
    "to-issues",
    "implement",
    "tdd",
    "diagnosing-bugs",
    "code-review",
    "qa",
    "long-running",
    "ai-native-init",
    "ai-native-upgrade",
    "ship-ticket",
]

PLANNING = [
    "grill-me",
    "grill-me-with-docs",
    "handoff",
    "write-a-prd",
    "wayfinder",
    "to-issues",
    "sprint-planning",
    "ai-native-init",
    "ai-native-upgrade",
    "ship-ticket",
]

KNOWN_PRESETS = ("engineering", "planning", "all")
LAYOUTS = {"features", "sprints", "epics", "flat"}
ROOTS = {"context", "docs"}
CLONES = {"personal", "work"}
BOARDS = {"markdown", "jira"}
INDEX_KEYS = {"none", "scenes", "alembic"}
DECISION_POLICIES = {"preliminary_until_feature_merge", "locked_on_record"}

GEN_BEGIN = "<!-- ai-native:generated:begin -->"
GEN_END = "<!-- ai-native:generated:end -->"
PROJ_BEGIN = "<!-- ai-native:project:begin -->"
PROJ_END = "<!-- ai-native:project:end -->"


def normalize_packs(packs: list[str]) -> list[str]:
    if not packs:
        raise ValueError("packs is empty")
    unknown = [p for p in packs if p not in KNOWN_PRESETS]
    if unknown:
        raise ValueError(f"unknown packs: {', '.join(unknown)}")
    out: list[str] = []
    for name in packs:
        if name not in out:
            out.append(name)
    return out


def _expanded(packs: list[str]) -> list[str]:
    names = set(normalize_packs(packs))
    if "all" in names:
        names = {"engineering", "planning"}
    ordered: list[str] = []
    if "engineering" in names or "all" in set(packs):
        ordered.extend(ENGINEERING)
    if "planning" in names or "all" in set(packs):
        ordered.extend(PLANNING)
    return ordered


def skills_for(packs: list[str]) -> list[str]:
    """Skills to install for this selection. Explicit preset lists, not every directory."""
    seen: set[str] = set()
    out: list[str] = []
    for name in _expanded(packs):
        if name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def wants_planning(packs: list[str]) -> bool:
    names = set(normalize_packs(packs))
    return "all" in names or "planning" in names


def switch_packs(
    current: list[str],
    *,
    add: list[str] | None = None,
    remove: list[str] | None = None,
) -> list[str]:
    """Change selection without collapsing a list into the `all` token."""
    cur = normalize_packs(current)
    removing = set(remove or [])
    adding = list(add or [])
    for name in list(removing) + adding:
        if name not in KNOWN_PRESETS or name == "all":
            raise ValueError(f"add/remove accepts engineering or planning, not {name!r}")
    if "all" in cur and not removing:
        return cur
    if "all" in cur and removing:
        cur = [name for name in ("engineering", "planning") if name not in removing]
    else:
        cur = [name for name in cur if name not in removing]
    for name in adding:
        if name not in cur:
            cur.append(name)
    if not cur:
        raise ValueError("selection would be empty")
    return cur


def skills_only_in(before: list[str], after: list[str]) -> list[str]:
    kept = set(skills_for(after))
    return [name for name in skills_for(before) if name not in kept]


def classify_profile(data: dict) -> list[str]:
    """Incompatible recognized values. Unknown keys are not issues."""
    issues: list[str] = []
    checks = (
        ("root", ROOTS),
        ("layout", LAYOUTS),
        ("clone", CLONES),
        ("board", BOARDS),
        ("index_keys", INDEX_KEYS),
        ("decision_policy", DECISION_POLICIES),
    )
    for key, allowed in checks:
        if key in data and data[key] not in allowed:
            issues.append(f"{key}={data[key]!r} is not supported ({', '.join(sorted(allowed))})")
    if "packs" in data:
        packs = data["packs"]
        if not isinstance(packs, list) or any(not isinstance(p, str) or p not in KNOWN_PRESETS for p in packs):
            issues.append(f"packs={packs!r} is not a list of {', '.join(KNOWN_PRESETS)}")
        elif not packs:
            issues.append("packs is empty")
    if "tools" in data and (
        not isinstance(data["tools"], list) or any(not isinstance(t, str) for t in data["tools"])
    ):
        issues.append("tools must be a list of strings")
    if "tracker" in data and not isinstance(data["tracker"], dict):
        issues.append("tracker must be an object")
    if "slug" in data and not isinstance(data["slug"], str):
        issues.append("slug must be a string")
    if "default_branch" in data and not isinstance(data["default_branch"], str):
        issues.append("default_branch must be a string")
    return issues


def bump_pack_version(data: dict) -> dict:
    out = dict(data)
    out["pack"] = PACK_VERSION
    return out


def default_jira_tracker() -> dict:
    return {
        "kind": "jira",
        "site": "",
        "project": "",
        "capabilities": ["hierarchy", "sprints", "estimates", "owners"],
        "issue_types": {"map": "Epic", "story": "Story", "subtask": "Sub-task"},
        "fields": {"estimate": "", "owner": "assignee", "sprint": "", "parent": "parent"},
        "statuses": {
            "todo": "To Do",
            "doing": "In Progress",
            "in_review": "In Review",
            "done": "Done",
        },
        "hierarchy": "parent-child",
    }


def _between(text: str, begin: str, end: str) -> str | None:
    if text.count(begin) != 1 or text.count(end) != 1:
        return None
    start = text.find(begin)
    stop = text.find(end)
    if stop < start:
        return None
    return text[start + len(begin) : stop]


def merge_adapter(existing: str | None, generated: str) -> tuple[str | None, str | None]:
    """Refresh the pack region. Keep the project region. Return (text, error)."""
    if _between(generated, GEN_BEGIN, GEN_END) is None or _between(generated, PROJ_BEGIN, PROJ_END) is None:
        return None, "generated adapter is missing pack or project markers"
    if existing is None:
        return generated if generated.endswith("\n") else generated + "\n", None
    project = _between(existing, PROJ_BEGIN, PROJ_END)
    if project is None:
        return None, "adapter has no intact project region; left unchanged"
    end = generated.find(GEN_END) + len(GEN_END)
    merged = generated[:end] + f"\n\n{PROJ_BEGIN}{project}{PROJ_END}\n"
    return merged, None
