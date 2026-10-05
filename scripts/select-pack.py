#!/usr/bin/env python3
"""Print the skills for an engineering, planning, or all preset.

Does not call `npx skills --pack` (that flag is not a real installer option).
A bare `npx skills add <repo>` installs every directory under skills/.
That command is not a preset. Presets are the explicit lists.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "skills" / "ai-native-init" / "scripts"))

from profile import (  # noqa: E402
    classify_profile,
    normalize_packs,
    skills_for,
    skills_only_in,
    switch_packs,
)

REPO = "git@github.com:HoeZey/ai-native.git"


def find_pack(target: Path) -> Path:
    for name in ("context", "docs"):
        path = target / name / ".ai-native.yml"
        if path.is_file():
            return path
    sys.exit("no context/.ai-native.yml or docs/.ai-native.yml — run /ai-native-init first")


def install_command(skills: list[str], repo: str) -> str:
    flags = " ".join(f"--skill {name}" for name in skills)
    return f"npx skills add {repo} {flags}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("engineering", "planning", "all"))
    parser.add_argument("--add", action="append", default=[])
    parser.add_argument("--remove", action="append", default=[])
    parser.add_argument("--target", type=Path)
    parser.add_argument("--repo", default=REPO)
    args = parser.parse_args()
    if not args.preset and not args.add and not args.remove:
        sys.exit("pass --preset and/or --add/--remove")
    if (args.add or args.remove) and args.target is None:
        sys.exit("--add and --remove need --target so the selection is saved")

    print(
        "Bare `npx skills add` is not a preset. It installs every directory under skills/. "
        "Presets are the explicit lists."
    )
    print("This command does not delete skills. User-owned skills stay put.")

    if args.target is None:
        packs = normalize_packs([args.preset])
        skills = skills_for(packs)
        print(f"packs: {', '.join(packs)}")
        print(install_command(skills, args.repo))
        return

    path = find_pack(args.target.resolve())
    data = json.loads(path.read_text())
    issues = classify_profile(data)
    if issues:
        sys.exit("incompatible profile:\n" + "\n".join(issues))
    current = data.get("packs")
    if not isinstance(current, list) or not current:
        if not args.preset or args.add or args.remove:
            sys.exit("profile has no packs list; pass --preset to set one")
        current = [args.preset]
    try:
        if args.add or args.remove:
            updated = switch_packs(current, add=args.add, remove=args.remove)
        else:
            updated = normalize_packs([args.preset])
    except ValueError as exc:
        sys.exit(str(exc))

    added = [name for name in skills_for(updated) if name not in set(skills_for(current))]
    dropped = skills_only_in(current, updated)
    data["packs"] = updated
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"packs: {', '.join(updated)}")
    if added:
        print("install:")
        print(install_command(added, args.repo))
    elif not dropped:
        print(install_command(skills_for(updated), args.repo))
    if dropped:
        print("no longer required by the selected packs (not deleted):")
        print(", ".join(dropped))


if __name__ == "__main__":
    main()
