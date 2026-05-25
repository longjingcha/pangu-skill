from __future__ import annotations

import argparse
from pathlib import Path

from scripts._bootstrap import SRC  # noqa: F401

from pangu_skill.installer import install_skill_package


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the skill package to a target runtime")
    parser.add_argument("--target", required=True, help="Target runtime, e.g. cursor/codex/claude-code")
    parser.add_argument("--source", default=".", help="Source project directory")
    parser.add_argument("--dry-run", action="store_true", help="Show install destination without copying files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        destination = install_skill_package(target=args.target, source_dir=args.source, dry_run=args.dry_run)
    except ValueError as exc:
        print(str(exc))
        return 1

    if args.dry_run:
        print(f"Would install to: {destination}")
        return 0

    print(f"Installed skill package to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
