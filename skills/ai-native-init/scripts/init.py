#!/usr/bin/env python3
"""Seed an AI-native memory layer into a git repo. Do not invent files by hand — run this."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
TEMPLATES = SKILL_DIR / "templates"
PACK_VERSION = "0.1.0"


def slug_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def load_tmpl(name: str) -> str:
    path = TEMPLATES / name
    return path.read_text()


def render(name: str, **kw: str) -> str:
    text = load_tmpl(name)
    for k, v in kw.items():
        text = text.replace("${" + k + "}", v)
    leftover = re.findall(r"\$\{[a-z_]+\}", text)
    if leftover:
        sys.exit(f"unrendered placeholders in {name}: {leftover}")
    return text


def append_unique(path: Path, lines: list[str]) -> None:
    existing = path.read_text() if path.exists() else ""
    blob = existing if existing.endswith("\n") or not existing else existing + "\n"
    for line in lines:
        if line == "":
            if not blob.endswith("\n\n"):
                blob += "\n"
            continue
        if line not in existing.splitlines():
            blob += line + "\n"
    path.write_text(blob)


def merge_graft_mcp(path: Path) -> None:
    data: dict = {}
    if path.exists():
        data = json.loads(path.read_text())
    servers = data.setdefault("mcpServers", {})
    servers.setdefault("graft", {"command": "graft", "args": ["mcp"]})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def write(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else content + "\n")


def tools_yaml(tools: list[str], github_repo: str, default_branch: str) -> str:
    blocks = []
    catalog = {
        "graft": """  - id: graft
    when: file and symbol discovery — before grep or reading a whole file
    how: graft ask / callers / skeleton / map; MCP in .cursor/mcp.json; protocol in .cursor/rules/graft.mdc
    not: ticket AC, PRs""",
        "github": f"""  - id: github
    when: PR status, review, or opening a PR for {github_repo or "this GitHub repo"}
    how: Cursor plugin MCP plugin-github-github; or gh
    base: {default_branch}
    not: ticket AC (INDEX.md + plan.md, not GitHub issues)""",
        "godot": """  - id: godot-ai
    when: scenes, nodes, packed resources, project.godot, play / screenshot
    how: user-godot-ai MCP; protocol in .cursor/rules/godot-ai-tools.mdc if present
    not: ticket AC; skip if session_manage list is empty""",
        "atlassian": """  - id: atlassian
    when: Jira/Confluence the user explicitly asked for
    how: Atlassian MCP; Jira writes only when asked
    not: ticket AC for markdown-board repos; do not open create-jira-ticket unless asked""",
    }
    for t in tools:
        if t not in catalog:
            sys.exit(f"unknown tool {t!r}; expected graft, github, godot, atlassian")
        blocks.append(catalog[t])
    return "---\npurpose: project-tool-glossary\n---\n\n```yaml\ntools:\n" + "\n".join(blocks) + "\n```\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", type=Path, default=Path("."), help="consumer repo root")
    p.add_argument("--root", choices=("context", "docs"), default="context")
    p.add_argument("--layout", choices=("sprints", "epics", "flat"), default="sprints")
    p.add_argument("--clone", choices=("personal", "work"), default="personal")
    p.add_argument("--default-branch", default="main")
    p.add_argument("--slug", required=True, help="repo slug: 10x-<slug> and rule name")
    p.add_argument("--board", choices=("markdown", "jira"), default="markdown")
    p.add_argument("--tools", default="graft,github", help="comma list: graft,github,godot,atlassian")
    p.add_argument("--index-keys", choices=("none", "scenes", "alembic"), default="none")
    p.add_argument("--github-repo", default="", help="e.g. HoeZey/quota")
    p.add_argument("--force", action="store_true", help="overwrite protocol files")
    p.add_argument("--upgrade", action="store_true", help="protocol files only; never tickets/INDEX current")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    target = args.target.resolve()
    if not (target / ".git").exists():
        sys.exit(f"not a git repo: {target}")
    if not TEMPLATES.is_dir():
        sys.exit(f"templates missing next to skill: {TEMPLATES}")

    tools = [t.strip() for t in args.tools.split(",") if t.strip()]
    if "graft" not in tools:
        tools.insert(0, "graft")
    root_name = args.root
    root = target / root_name
    kw = {
        "root": root_name,
        "slug": args.slug,
        "slug_title": slug_title(args.slug),
        "adapter": f"10x-{args.slug}",
        "default_branch": args.default_branch,
        "layout": args.layout,
        "index_keys": args.index_keys,
        "memory_commit": (
            f"`{root_name}/` is committed working memory."
            if args.clone == "personal"
            else f"`{root_name}/` is gitignored working memory; `.cursorignore` re-includes it."
        ),
        "jira_line": (
            f"This repo has no Jira. Product, PM, and engineering contract live under `{root_name}/`."
            if args.board == "markdown"
            else f"Jira is the product tracker. `{root_name}/` is the engineering contract. Point, don't paste Jira bodies."
        ),
    }

    write(target / ".cursor" / "rules" / "graft.mdc", load_tmpl("protocol/graft.mdc"), force=True)
    write(
        target / ".cursor" / "rules" / f"{args.slug}-ai-native-engineering.mdc",
        render("protocol/always-apply.mdc.tmpl", **kw),
        force=args.force or args.upgrade,
    )
    write(
        target / ".cursorignore",
        render("protocol/cursorignore.tmpl", **kw),
        force=args.force or args.upgrade,
    )
    merge_graft_mcp(target / ".cursor" / "mcp.json")

    gi = [
        "",
        "# AI-native (generated graph + session notes)",
        "graft/",
        ".handoff/",
        ".ignore",
    ]
    if args.clone == "work":
        gi += [f"{root_name}/", ".cursorignore"]
    append_unique(target / ".gitignore", gi)

    write(root / "TOOLS.md", tools_yaml(tools, args.github_repo, args.default_branch), force=args.force or args.upgrade)
    write(root / "README.md", render("protocol/README.md.tmpl", **kw), force=args.force or args.upgrade)

    pack = {
        "pack": PACK_VERSION,
        "root": root_name,
        "layout": args.layout,
        "clone": args.clone,
        "default_branch": args.default_branch,
        "slug": args.slug,
        "board": args.board,
        "tools": tools,
        "index_keys": args.index_keys,
    }
    write(root / ".ai-native.yml", json.dumps(pack, indent=2) + "\n", force=True)

    if args.upgrade:
        print(f"upgraded protocol under {root} (pack {PACK_VERSION})")
        return

    if args.layout == "sprints":
        write(root / "INDEX.md", render("layouts/sprints/repo-INDEX.md.tmpl", **kw), force=False)
        sprint = root / "planning" / "sprints" / "S00"
        write(sprint / "INDEX.md", render("layouts/sprints/sprint-INDEX.md.tmpl", **kw), force=False)
        write(sprint / "decisions.md", render("layouts/sprints/decisions.md.tmpl", **kw), force=False)
        write(sprint / "progress.md", render("layouts/sprints/progress.md.tmpl", **kw), force=False)
        current_link = "planning/sprints/S00"
    elif args.layout == "epics":
        write(root / "INDEX.md", render("layouts/epics/repo-INDEX.md.tmpl", **kw), force=False)
        epic = root / "planning" / "epics" / "BOOT"
        write(epic / "INDEX.md", render("layouts/epics/epic-INDEX.md.tmpl", **kw), force=False)
        write(epic / "decisions.md", render("layouts/sprints/decisions.md.tmpl", **kw), force=False)
        write(epic / "progress.md", render("layouts/sprints/progress.md.tmpl", **kw), force=False)
        current_link = "planning/epics/BOOT"
    else:
        write(root / "INDEX.md", render("layouts/flat/repo-INDEX.md.tmpl", **kw), force=False)
        current_link = "planning/tickets"

    ticket = root / "planning" / "tickets" / "S00-01"
    write(ticket / "INDEX.md", render("tickets/S00-01-INDEX.md.tmpl", **kw), force=False)

    if args.board == "markdown":
        write(root / "planning" / "board.md", render("board/board.md.tmpl", **kw), force=False)
        write(root / "planning" / "backlog.md", render("board/backlog.md.tmpl", **kw), force=False)
        write(root / "planning" / "icebox.md", "# Icebox\n\nNot scheduled. Not a board column.\n", force=False)
        write(root / "planning" / "pm-state.md", render("board/pm-state.md.tmpl", **kw), force=False)
        write(root / "planning" / "sprint-log.md", "# Sprint log\n\nPM process notes. Newest first.\n", force=False)
        write(
            root / "CHANGELOG.md",
            "# Changelog\n\n## Unreleased\n\n### Added\n\n### Changed\n\n### Fixed\n",
            force=False,
        )

    write(target / "CONTEXT.md", "# Glossary\n\nUbiquitous language for this repo. Keep this file glossary-only.\n", force=False)
    write(root / "decisions" / "README.md", render("decisions/README.md.tmpl", **kw), force=False)

    adapter_dir = target / ".cursor" / "skills" / f"10x-{args.slug}"
    write(adapter_dir / "SKILL.md", render("adapter/SKILL.md.tmpl", **kw), force=args.force)

    print(f"seeded {root_name}/ (layout={args.layout}, clone={args.clone})")
    print(f"adapter: .cursor/skills/10x-{args.slug}/SKILL.md")
    print(f"next: honor {root_name}/INDEX.md ({current_link})")
    print("run `graft build` once if graft is installed")


if __name__ == "__main__":
    main()
