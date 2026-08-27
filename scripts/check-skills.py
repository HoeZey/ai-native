#!/usr/bin/env python3
"""Fail if skills/<dir>/SKILL.md frontmatter name: does not match <dir>."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills"
pat = re.compile(r"^name:\s*(.+)\s*$", re.M)
failed = 0
for skill_md in sorted(ROOT.glob("*/SKILL.md")):
    dirname = skill_md.parent.name
    text = skill_md.read_text()
    m = pat.search(text)
    if not m:
        print(f"FAIL {dirname}: no name: in frontmatter")
        failed += 1
        continue
    name = m.group(1).strip()
    if name != dirname:
        print(f"FAIL {dirname}: name: {name!r} != directory")
        failed += 1
        continue
    print(f"ok {dirname}")
sys.exit(1 if failed else 0)
