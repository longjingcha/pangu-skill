from __future__ import annotations

import shutil
from pathlib import Path
from typing import Dict


def _skill_dir_for_target(target: str) -> Path:
    home = Path.home()
    target = target.lower().strip()

    mapping: Dict[str, Path] = {
        "claude-code": home / ".claude" / "skills" / "pangu-skill",
        "codex": home / ".codex" / "skills" / "pangu-skill",
        "cursor": home / ".cursor" / "skills" / "pangu-skill",
        "openclaw": home / ".openclaw" / "workspace" / "skills" / "pangu-skill",
        "pycharm": home / ".pangu-skill" / "skills" / "pangu-skill",
        "hermes": home / ".hermes" / "skills" / "pangu-skill",
    }

    if target not in mapping:
        raise ValueError(f"Unsupported target runtime: {target}")
    return mapping[target]


def install_skill_package(target: str, source_dir: str | Path = ".", dry_run: bool = False) -> Path:
    src = Path(source_dir).resolve()
    dest = _skill_dir_for_target(target)

    files_to_copy = [
        "README.md",
        "SKILL.md",
        "skill_schema.yaml",
        "distill_config.yaml",
        "RELEASE.md",
    ]

    if dry_run:
        return dest

    dest.mkdir(parents=True, exist_ok=True)
    for filename in files_to_copy:
        candidate = src / filename
        if candidate.exists() and candidate.is_file():
            shutil.copy2(candidate, dest / filename)

    return dest
