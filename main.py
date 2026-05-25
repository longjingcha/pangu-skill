from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from src.pangu_skill.distill_config import DistillConfig
from src.pangu_skill.exporter import (
    distill_skill_schema,
    load_skill_schema,
    save_skill_markdown,
    save_skill_schema,
    validate_skill_schema,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pangu skill schema utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export", help="Export YAML schema to SKILL.md")
    export_parser.add_argument("--schema", default="skill_schema.yaml", help="Path to the input YAML schema file")
    export_parser.add_argument("--output", default="generated/SKILL.md", help="Path to the output markdown file")

    validate_parser = subparsers.add_parser("validate", help="Validate a YAML schema")
    validate_parser.add_argument("--schema", default="skill_schema.yaml", help="Path to the YAML schema file")

    distill_parser = subparsers.add_parser("distill", help="Distill raw materials into a first-pass skill schema")
    distill_parser.add_argument("--input", nargs="+", required=True, help="Raw material text files")
    distill_parser.add_argument("--schema-output", default="generated/distilled_skill.yaml", help="Output YAML schema path")
    distill_parser.add_argument("--markdown-output", default="generated/SKILL.md", help="Output SKILL.md path")
    distill_parser.add_argument("--name", default="Generated Skill", help="Name for the distilled skill")
    distill_parser.add_argument("--skill-id", default="pangu.generated.001", help="Skill ID for the distilled skill")
    distill_parser.add_argument("--config", default="distill_config.yaml", help="Path to distillation config YAML")

    return parser.parse_args()


def cmd_export(schema_path: str, output_path: str) -> int:
    schema = load_skill_schema(schema_path)
    errors = validate_skill_schema(schema)
    if errors:
        print("Schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    output = save_skill_markdown(schema, output_path)
    print(f"Exported skill markdown to {output}")
    return 0


def cmd_validate(schema_path: str) -> int:
    schema = load_skill_schema(schema_path)
    errors = validate_skill_schema(schema)
    if errors:
        print("Schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Schema validation passed.")
    return 0


def cmd_distill(input_files: List[str], schema_output: str, markdown_output: str, name: str, skill_id: str, config_path: str) -> int:
    materials = []
    for item in input_files:
        path = Path(item)
        if not path.exists():
            print(f"Missing input file: {path}")
            return 1
        materials.append(path.read_text(encoding="utf-8"))

    config = DistillConfig.load(config_path)
    schema = distill_skill_schema(materials, skill_id=skill_id, name=name, config=config)
    errors = validate_skill_schema(schema)
    if errors:
        print("Generated schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    schema_path = save_skill_schema(schema, schema_output)
    markdown_path = save_skill_markdown(schema, markdown_output)
    print(f"Distilled schema saved to {schema_path}")
    print(f"Exported skill markdown to {markdown_path}")
    return 0


def main() -> int:
    args = parse_args()

    if args.command == "export":
        return cmd_export(args.schema, args.output)
    if args.command == "validate":
        return cmd_validate(args.schema)
    if args.command == "distill":
        return cmd_distill(args.input, args.schema_output, args.markdown_output, args.name, args.skill_id, args.config)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
