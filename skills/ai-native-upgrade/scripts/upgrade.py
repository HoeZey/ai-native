#!/usr/bin/env python3
"""Refresh protocol files from pack templates using the consumer's .ai-native.yml."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
INIT = HERE.parents[2] / "ai-native-init" / "scripts" / "init.py"


def find_pack(target: Path) -> Path:
    for name in ("context", "docs"):
        p = target / name / ".ai-native.yml"
        if p.is_file():
            return p
    sys.exit("no context/.ai-native.yml or docs/.ai-native.yml — run /ai-native-init first")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--target", type=Path, default=Path("."))
    args = p.parse_args()
    target = args.target.resolve()
    pack_path = find_pack(target)
    pack = json.loads(pack_path.read_text())
    if not INIT.is_file():
        sys.exit(
            f"ai-native-init not next to this skill ({INIT}). Install the full catalog."
        )
    cmd = [
        sys.executable,
        str(INIT),
        "--target",
        str(target),
        "--upgrade",
        "--slug",
        pack["slug"],
        "--root",
        pack["root"],
        "--layout",
        pack["layout"],
        "--clone",
        pack["clone"],
        "--default-branch",
        pack["default_branch"],
        "--board",
        pack["board"],
        "--tools",
        ",".join(pack["tools"]),
        "--index-keys",
        pack.get("index_keys", "none"),
    ]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
