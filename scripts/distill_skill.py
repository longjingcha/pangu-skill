from __future__ import annotations

import argparse
from pathlib import Path

from scripts._bootstrap import SRC  # noqa: F401

from pangu_skill.distill_config import DistillConfig
from pangu_skill.exporter import distill_skill_schema, save_skill_markdown, save_skill_schema, validate_skill_schema
from pangu_skill.intent import collect_materials, detect_intent, infer_skill_slug, normalize_subject


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Distill research materials into a skill schema")
    parser.add_argument("--input", nargs="+", required=False, default=[], help="Input material files")
    parser.add_argument("--input-dir", default=None, help="Input directory containing merged research materials")
    parser.add_argument("--schema-output", required=False, default="generated/distilled_skill.yaml", help="Output YAML schema path")
    parser.add_argument("--markdown-output", required=False, default="generated/SKILL.md", help="Output SKILL.md path")
    parser.add_argument("--name", default="Generated Skill", help="Skill name")
    parser.add_argument("--skill-id", default="pangu.generated.001", help="Skill ID")
    parser.add_argument("--config", default="distill_config.yaml", help="Distillation config YAML")
    parser.add_argument("--say", default=None, help="Natural language distill request")
    parser.add_argument("--query", default=None, help="Natural language topic / person name, used to derive name and skill id")
    return parser.parse_args()


def _collect_input_materials(args: argparse.Namespace) -> list[str]:
    paths = list(args.input or [])
    if args.input_dir:
        root = Path(args.input_dir)
        if root.exists():
            for suffix in ["*.txt", "*.md", "*.json"]:
                paths.extend(str(p) for p in sorted(root.rglob(suffix)))
    return paths


def main() -> int:
    args = parse_args()

    if args.say:
        intent = detect_intent(args.say)
        if intent.intent == "distill":
            subject = normalize_subject(intent.subject)
            suggested_id = infer_skill_slug(subject)
            print(f"[natural] distill request detected: {subject}")
            print(f"[natural] suggested skill id: {suggested_id}")
            if not args.query:
                args.query = subject
        else:
            print("[natural] 当前只支持蒸馏意图。你可以说：帮我蒸馏一个乔布斯 skill")
            return 1

    if args.query:
        subject = normalize_subject(args.query)
        args.name = f"{subject} Skill"
        args.skill_id = infer_skill_slug(subject)
        print(f"[query] topic: {subject}")
        print(f"[query] name: {args.name}")
        print(f"[query] skill_id: {args.skill_id}")

    input_paths = _collect_input_materials(args)
    if not input_paths:
        print("No input materials provided. Use --input, --input-dir, or a natural language query that resolves to materials.")
        return 1

    materials = collect_materials(input_paths)
    if not materials:
        print("No readable input material files found.")
        return 1

    config = DistillConfig.load(args.config)
    schema = distill_skill_schema(materials, skill_id=args.skill_id, name=args.name, config=config)

    errors = validate_skill_schema(schema)
    if errors:
        print("Generated schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    schema_path = save_skill_schema(schema, args.schema_output)
    markdown_path = save_skill_markdown(schema, args.markdown_output)

    print(f"Distilled skill schema saved to {schema_path}")
    print(f"Exported skill markdown saved to {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
