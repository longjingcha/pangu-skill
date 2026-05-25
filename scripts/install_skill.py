from __future__ import annotations

import argparse
from pathlib import Path

from scripts._bootstrap import SRC  # noqa: F401

from pangu_skill.installer import install_skill_package

SUPPORTED_TARGETS = ["cursor", "codex", "claude-code", "openclaw", "hermes", "gemini-cli", "opencode", "workbuddy", "codebuddy"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install pangu-skill to a target runtime")
    parser.add_argument("--target", default=None, help="Target runtime, e.g. cursor/codex/claude-code")
    parser.add_argument("--source", default=".", help="Source project directory")
    parser.add_argument("--dry-run", action="store_true", help="Show install destination without copying files")
    parser.add_argument("--list-targets", action="store_true", help="List supported target runtimes")
    return parser.parse_args()


def _print_supported_targets() -> None:
    print("Supported targets:")
    for target in SUPPORTED_TARGETS:
        print(f"- {target}")


def main() -> int:
    args = parse_args()

    if args.list_targets:
        _print_supported_targets()
        return 0

    if not args.target:
        print("Missing --target. Use --list-targets to see supported runtimes.")
        return 1

    source_dir = Path(args.source).resolve()
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return 1

    if args.target not in SUPPORTED_TARGETS:
        print(f"Unsupported target: {args.target}")
        print("Use --list-targets to see supported runtimes.")
        return 1

    try:
        destination = install_skill_package(target=args.target, source_dir=str(source_dir), dry_run=args.dry_run)
    except ValueError as exc:
        print(str(exc))
        return 1

    if args.dry_run:
        print(f"Would install to: {destination}")
        return 0

    print(f"Installed pangu-skill to {destination}")
    print("")
    print("Next steps:")
    print("1. Open your agent runtime")
    print("2. Ask it to load the installed skill")
    print("3. Start distilling and chatting")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
