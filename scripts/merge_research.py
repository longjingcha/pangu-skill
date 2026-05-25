from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge research materials into a single corpus")
    parser.add_argument("--input-dir", default="research/raw", help="Input research directory containing subtitles/wiki/web pages")
    parser.add_argument("--output-dir", default="research/merged", help="Output directory for merged materials")
    parser.add_argument("--output-name", default="merged_research.txt", help="Merged text filename")
    return parser.parse_args()


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def collect_files(root: Path, suffixes: List[str]) -> List[Path]:
    files: List[Path] = []
    for suffix in suffixes:
        files.extend(sorted(root.rglob(f"*{suffix}")))
    return sorted(set(files))


def load_json_as_text(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    if isinstance(data, dict):
        parts = []
        for key in ["title", "url", "content", "text", "summary", "lang"]:
            value = data.get(key)
            if value:
                parts.append(f"{key.upper()}: {value}")
        if not parts:
            parts.append(json.dumps(data, ensure_ascii=False, indent=2))
        return "\n".join(parts)

    if isinstance(data, list):
        return "\n".join(json.dumps(item, ensure_ascii=False, indent=2) for item in data)

    return str(data)


def collect_materials(input_dir: Path) -> List[Tuple[str, str]]:
    materials: List[Tuple[str, str]] = []

    for path in collect_files(input_dir, [".txt", ".md"]):
        content = read_text_file(path).strip()
        if content:
            materials.append((str(path), content))

    for path in collect_files(input_dir, [".json"]):
        content = load_json_as_text(path).strip()
        if content:
            materials.append((str(path), content))

    return materials


def merge_materials(materials: List[Tuple[str, str]]) -> str:
    blocks: List[str] = []
    blocks.append("# Merged Research Corpus")
    blocks.append("")

    for idx, (source_path, content) in enumerate(materials, start=1):
        blocks.append(f"## Source {idx}")
        blocks.append(f"- Path: `{source_path}`")
        blocks.append("")
        blocks.append(content)
        blocks.append("")
        blocks.append("---")
        blocks.append("")

    return "\n".join(blocks).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return 1

    materials = collect_materials(input_dir)
    if not materials:
        print(f"No research materials found in: {input_dir}")
        return 1

    merged_text = merge_materials(materials)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / args.output_name
    output_path.write_text(merged_text, encoding="utf-8")

    manifest_path = output_dir / "manifest.json"
    manifest = {
        "input_dir": str(input_dir),
        "output_file": str(output_path),
        "source_count": len(materials),
        "sources": [source for source, _ in materials],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Merged {len(materials)} research sources")
    print(f"Saved merged corpus to: {output_path}")
    print(f"Saved manifest to: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
