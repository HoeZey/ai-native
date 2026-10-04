#!/usr/bin/env python3
"""Temporary-repo checks for pack selection, init, and upgrade preservation."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "ai-native-init" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import profile  # noqa: E402

INIT = SCRIPTS / "init.py"
UPGRADE = ROOT / "skills" / "ai-native-upgrade" / "scripts" / "upgrade.py"
SELECT = ROOT / "scripts" / "select-pack.py"


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def git_repo(path: Path) -> None:
    path.mkdir(parents=True)
    result = run(["git", "init"], cwd=path)
    if result.returncode != 0:
        raise SystemExit(result.stderr)


def init(path: Path, *args: str) -> None:
    result = run([sys.executable, str(INIT), "--target", str(path), "--slug", "demo", *args])
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_membership() -> None:
    for packs in (["engineering"], ["planning"], ["all"], ["engineering", "planning"]):
        skills = profile.skills_for(packs)
        assert "scrum-master" not in skills
    engineering = set(profile.skills_for(["engineering"]))
    planning = set(profile.skills_for(["planning"]))
    assert "sprint-planning" not in engineering
    assert "implement" in engineering
    assert "sprint-planning" in planning
    assert "implement" not in planning
    assert set(profile.skills_for(["all"])) == engineering | planning
    assert profile.switch_packs(["engineering"], add=["planning"]) == ["engineering", "planning"]
    assert profile.switch_packs(["all"], remove=["planning"]) == ["engineering"]
    assert profile.switch_packs(["all"], add=["planning"]) == ["all"]
    dropped = profile.skills_only_in(["engineering", "planning"], ["engineering"])
    assert "sprint-planning" in dropped
    assert "ship-ticket" not in dropped
    assert "implement" not in dropped


def test_select_command() -> None:
    result = run([sys.executable, str(SELECT), "--preset", "all"])
    assert result.returncode == 0, result.stderr
    assert "--skill scrum-master" not in result.stdout
    assert "not the `all` preset" in result.stdout or "not a preset" in result.stdout
    assert "--skill sprint-planning" in result.stdout
    assert "--skill implement" in result.stdout
    assert "--pack" not in result.stdout


def test_engineering_and_planning_init(tmp: Path) -> None:
    eng = tmp / "eng"
    git_repo(eng)
    init(eng, "--packs", "engineering")
    assert not (eng / "context" / "sprint-planning").exists()
    assert (eng / "context" / "features" / "seed" / "tickets" / "S00-01" / "INDEX.md").is_file()
    pack = read_json(eng / "context" / ".ai-native.yml")
    assert pack["packs"] == ["engineering"]
    assert pack["decision_policy"] == "preliminary_until_feature_merge"
    assert "notes_from_the_future" not in pack
    adapter = (eng / ".cursor" / "skills" / "10x-demo" / "SKILL.md").read_text()
    rule = (eng / ".cursor" / "rules" / "demo-ai-native-engineering.mdc").read_text()
    assert "WIP 1" not in adapter and "scrum-master" not in adapter
    assert "WIP 1" not in rule and "scrum-master" not in rule
    assert "<!-- ai-native:project:begin -->" in adapter
    assert (eng / ".cursor" / "rules" / "demo-project.mdc").is_file()

    planned = tmp / "planned"
    git_repo(planned)
    init(planned, "--packs", "all")
    people = (planned / "context" / "sprint-planning" / "S00" / "people.md").read_text()
    assert "Solo" not in people
    assert (planned / "context" / "sprint-planning" / "README.md").is_file()

    legacy = tmp / "legacy"
    git_repo(legacy)
    init(legacy, "--layout", "sprints", "--packs", "engineering")
    assert (legacy / "context" / "planning" / "sprints" / "S00" / "INDEX.md").is_file()
    assert (legacy / "context" / "planning" / "tickets" / "S00-01" / "INDEX.md").is_file()
    assert not (legacy / "context" / "features").exists()
    assert not (legacy / "context" / "sprint-planning").exists()

    jira = tmp / "jira"
    git_repo(jira)
    init(jira, "--board", "jira", "--packs", "engineering")
    tracker = read_json(jira / "context" / ".ai-native.yml")["tracker"]
    assert tracker["kind"] == "jira"
    assert tracker["project"] == ""
    assert not (jira / "context" / "planning" / "board.md").exists()


def test_upgrade_roundtrip(tmp: Path) -> None:
    repo = tmp / "upgrade"
    git_repo(repo)
    init(repo, "--packs", "engineering")
    root = repo / "context"
    pack_path = root / ".ai-native.yml"
    pack = read_json(pack_path)
    pack["decision_policy"] = "locked_on_record"
    pack["quota_note"] = "keep-me"
    pack["tracker"] = {"kind": "markdown", "capabilities": []}
    del pack["github_repo"]
    pack_path.write_text(json.dumps(pack, indent=2) + "\n")
    tools = root / "TOOLS.md"
    tools.write_text(tools.read_text() + "\nTOOLING-KEEP\n")
    index = root / "features" / "seed" / "INDEX.md"
    index.write_text(index.read_text().replace("ticket: S00-01", "ticket: S00-KEEP"))
    (root / "features" / "seed" / "UNTOUCHED.txt").write_text("stay\n")
    companion = repo / ".cursor" / "rules" / "demo-project.mdc"
    companion.write_text(companion.read_text() + "\nCOMPANION-KEEP\n")
    adapter_path = repo / ".cursor" / "skills" / "10x-demo" / "SKILL.md"
    adapter = adapter_path.read_text()
    adapter = adapter.replace("Invent a WIP limit", "STALE-GENERATED")
    adapter = adapter.replace(
        "<!-- ai-native:project:begin -->\n<!-- ai-native:project:end -->",
        "<!-- ai-native:project:begin -->\nKEEP-PROJECT\n<!-- ai-native:project:end -->",
    )
    adapter_path.write_text(adapter)

    result = run([sys.executable, str(UPGRADE), "--target", str(repo)])
    assert result.returncode == 0, result.stdout + result.stderr
    saved = read_json(pack_path)
    assert saved["decision_policy"] == "locked_on_record"
    assert saved["quota_note"] == "keep-me"
    assert saved["tracker"]["kind"] == "markdown"
    assert saved["packs"] == ["engineering"]
    assert "TOOLING-KEEP" in tools.read_text()
    assert "ticket: S00-KEEP" in index.read_text()
    assert (root / "features" / "seed" / "UNTOUCHED.txt").read_text() == "stay\n"
    assert not (root / "sprint-planning").exists()
    refreshed = adapter_path.read_text()
    assert "STALE-GENERATED" not in refreshed
    assert "Invent a WIP limit" in refreshed
    assert "KEEP-PROJECT" in refreshed
    assert "COMPANION-KEEP" in companion.read_text()
    assert not (root / "upgrade-review.md").exists()

    result = run([sys.executable, str(UPGRADE), "--target", str(repo)])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "KEEP-PROJECT" in adapter_path.read_text()
    assert read_json(pack_path)["quota_note"] == "keep-me"
    assert "ticket: S00-KEEP" in index.read_text()


def test_incompatible_and_unmarked_adapter(tmp: Path) -> None:
    bad = tmp / "bad"
    git_repo(bad)
    init(bad, "--packs", "engineering")
    pack_path = bad / "context" / ".ai-native.yml"
    pack = read_json(pack_path)
    pack["layout"] = "custom"
    pack_path.write_text(json.dumps(pack, indent=2) + "\n")
    before = pack_path.read_text()
    result = run([sys.executable, str(UPGRADE), "--target", str(bad)])
    assert result.returncode == 2
    assert pack_path.read_text() == before
    assert "custom" in (bad / "context" / "upgrade-review.md").read_text()
    assert (bad / "context" / "features" / "seed" / "tickets" / "S00-01" / "INDEX.md").is_file()

    unmarked = tmp / "unmarked"
    git_repo(unmarked)
    init(unmarked, "--packs", "engineering")
    adapter = unmarked / ".cursor" / "skills" / "10x-demo" / "SKILL.md"
    adapter.write_text("# project rewrote the whole adapter\n")
    result = run([sys.executable, str(UPGRADE), "--target", str(unmarked)])
    assert result.returncode == 2
    assert adapter.read_text() == "# project rewrote the whole adapter\n"
    assert "project region" in (unmarked / "context" / "upgrade-review.md").read_text()


def test_pack_switch(tmp: Path) -> None:
    repo = tmp / "switch"
    git_repo(repo)
    init(repo, "--packs", "engineering")
    private = repo / ".cursor" / "skills" / "my-private" / "SKILL.md"
    private.parent.mkdir(parents=True)
    private.write_text("---\nname: my-private\n---\n")
    added = run([sys.executable, str(SELECT), "--target", str(repo), "--add", "planning"])
    assert added.returncode == 0, added.stdout + added.stderr
    assert read_json(repo / "context" / ".ai-native.yml")["packs"] == ["engineering", "planning"]
    assert "all" not in read_json(repo / "context" / ".ai-native.yml")["packs"]
    removed = run([sys.executable, str(SELECT), "--target", str(repo), "--remove", "planning"])
    assert removed.returncode == 0, removed.stdout + removed.stderr
    assert read_json(repo / "context" / ".ai-native.yml")["packs"] == ["engineering"]
    assert "sprint-planning" in removed.stdout
    assert "not deleted" in removed.stdout
    assert "implement" not in removed.stdout.split("no longer required", 1)[-1]
    assert private.is_file()


def main() -> None:
    test_membership()
    test_select_command()
    tmp = ROOT / ".tmp-consumer-tests"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    try:
        test_engineering_and_planning_init(tmp)
        test_upgrade_roundtrip(tmp)
        test_incompatible_and_unmarked_adapter(tmp)
        test_pack_switch(tmp)
    finally:
        shutil.rmtree(tmp)
    print("ok")


if __name__ == "__main__":
    main()
