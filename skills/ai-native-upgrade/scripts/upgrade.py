#!/usr/bin/env python3
"""Refresh protocol files from pack templates using the consumer's .ai-native.yml.

Preserves project-owned settings, adapter notes, and companion instructions.
Does not rewrite ticket trees or INDEX current/phase/ticket.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
INIT = HERE.parents[2] / "ai-native-init" / "scripts" / "init.py"


def load_init():
    if not INIT.is_file():
        sys.exit(f"ai-native-init not next to this skill ({INIT}). Install the full catalog.")
    spec = importlib.util.spec_from_file_location("ai_native_init", INIT)
    if spec is None or spec.loader is None:
        sys.exit(f"cannot load {INIT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path("."))
    args = parser.parse_args()
    module = load_init()
    raise SystemExit(module.upgrade_target(args.target.resolve()))


if __name__ == "__main__":
    main()
