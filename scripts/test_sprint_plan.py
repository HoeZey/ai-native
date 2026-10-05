#!/usr/bin/env python3
"""Self-check for skills/sprint-planning/scripts/sprint.py.

Run: uv run --with pyyaml python scripts/test_sprint_plan.py
"""

import datetime
import importlib.util
import pathlib
import sys
import tempfile

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sprint", ROOT / "skills/sprint-planning/scripts/sprint.py")
sprint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sprint)

S1 = """
sprint: Sprint 1
dates: [2026-10-07, 2026-10-20]
merge_by: 2026-10-16
goal: Ship the thing
capacity:
  - {person: Ana, pool: BE, points: 10}
  - {person: Bo, pool: BE, points: 10}
tickets:
  - {key: T-1, title: First, owner: Ana, points: 9, status: To Do, ready: 2026-10-12}
  - {key: T-2, title: Second, owner: Bo, points: 3, status: To Do, ready: 2026-10-09, blocked_by: [T-1]}
  - {key: T-3, title: Late, owner: Bo, points: 1, status: To Do, ready: 2026-10-19, blocked_by: [T-5]}
pull_in:
  - {key: T-4, title: Next, points: 2}
"""

S2 = """
sprint: Sprint 2
dates: [2026-10-21, 2026-11-03]
merge_by: 2026-10-30
goal: Ship the rest
capacity:
  - {person: Ana, pool: BE, points: 10}
tickets:
  - {key: T-1, title: First again, owner: Ana, points: 1, status: To Do}
  - {key: T-5, title: Early, owner: Ana, points: 1, status: To Do, blocked_by: [T-6, T-4]}
"""

S0 = """
sprint: Sprint 0
dates: [2026-10-01, 2026-10-06]
merge_by: 2026-10-02
goal: Earlier
capacity: []
tickets:
  - {key: T-6, title: Done before, owner: Ana, points: 1, status: Done}
"""


def write(root, name, text):
    folder = root / name
    folder.mkdir()
    (folder / "sprint.yaml").write_text(text)


def run(root, *cmd):
    return sprint.main([*cmd, str(root)], today=datetime.date(2026, 10, 5))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        write(root, "s1", S1)
        write(root, "s2", S2)

        s1 = sprint.load(root / "s1/sprint.yaml")
        flags = sprint.check(s1)
        assert any("Ana is over the 80% load limit" in f for f in flags), flags
        assert any("T-2 ready" in f and "blocker T-1" in f for f in flags), flags
        assert any("T-3 ready" in f and "after merge_by" in f for f in flags), flags
        assert not any(f.startswith("Bo ") for f in flags), flags
        assert [t["key"] for t, who in sprint.pull_in_fits(s1)] == ["T-4"]

        s2 = sprint.load(root / "s2/sprint.yaml")
        across = sprint.check_across([s1, s2], datetime.date(2026, 10, 5))
        assert any("T-1 is in Sprint 1 and Sprint 2" in f for f in across), across
        assert any("T-3 (Sprint 1) is blocked by T-5 in later Sprint 2" in f for f in across), across
        assert any("T-5 (Sprint 2) is blocked by T-4, which is only in Sprint 1 pull_in" in f for f in across), across

        write(root, "s0", S0)
        s0 = sprint.load(root / "s0/sprint.yaml")
        assert not any("T-6" in f for f in sprint.check_across([s0, s2], datetime.date(2026, 10, 7))), \
            "ended sprints are skipped"

        assert run(root, "check") == 1, "stale sprint.md and flags must fail"
        assert run(root, "render") == 0
        md = (root / "s1/sprint.md").read_text()
        assert md.startswith(sprint.HEADER) and "| 1 | T-1 | First |" in md, md

        (root / "s1/sprint.yaml").write_text(S1.replace("points: 3,", ""))
        assert run(root, "check") == 2, "missing points must be a schema error"

        (root / "s1/sprint.yaml").write_text(S1 + "stray: yes\n")
        assert run(root / "s1", "check") == 2, "unknown top-level key must be a schema error"
        (root / "s1/sprint.yaml").write_text(S1.replace(
            "{key: T-1, title: First,", "{key: T-1, title: First, stray: yes,",
        ))
        assert run(root / "s1", "check") == 2, "unknown ticket key must be a schema error"
        (root / "s1/sprint.yaml").write_text(S1.replace(
            "{person: Ana, pool: BE, points: 10}", "{person: Ana, pool: BE, points: 10, stray: 1}",
        ))
        assert run(root / "s1", "check") == 2, "unknown capacity key must be a schema error"
    print("ok")


if __name__ == "__main__":
    main()
