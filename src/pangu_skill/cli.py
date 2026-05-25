from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from .distill_config import DistillConfig
from .exporter import (
    distill_skill_schema,
    load_skill_schema,
    save_prompt_pack,
    save_skill_markdown,
    save_skill_schema,
    validate_skill_schema,
)
from .intent import detect_intent, infer_skill_slug, normalize_subject
from .pipeline import distill_from_query, quality_report_for_schema
from .installer import install_skill_package
from .quality import quality_check_file
from .runtime import answer_with_runtime_context, build_runtime_context


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pangu skill utilities")
    parser.add_argument("--say", default=None, help="Natural language command for distill/chat routing")
    parser.add_argument("--auto", action="store_true", help="Run the one-sentence auto pipeline")

    subparsers = parser.add_subparsers(dest="command")

    export_parser = subparsers.add_parser("export", help="Export YAML schema to SKILL.md")
    export_parser.add_argument("--schema", default="skill_schema.yaml", help="Input YAML schema file")
    export_parser.add_argument("--output", default="generated/SKILL.md", help="Output markdown file")

    validate_parser = subparsers.add_parser("validate", help="Validate a YAML schema")
    validate_parser.add_argument("--schema", default="skill_schema.yaml", help="YAML schema file")

    distill_parser = subparsers.add_parser("distill", help="Distill raw materials into a skill schema")
    distill_parser.add_argument("--input", nargs="*", default=[], help="Raw material text files")
    distill_parser.add_argument("--input-dir", default=None, help="Directory containing research materials")
    distill_parser.add_argument("--schema-output", default="generated/distilled_skill.yaml", help="Output YAML schema path")
    distill_parser.add_argument("--markdown-output", default="generated/SKILL.md", help="Output SKILL.md path")
    distill_parser.add_argument("--name", default="Generated Skill", help="Skill name")
    distill_parser.add_argument("--skill-id", default="pangu.generated.001", help="Skill ID")
    distill_parser.add_argument("--config", default="distill_config.yaml", help="Distillation config YAML")
    distill_parser.add_argument("--query", default=None, help="Topic/person name to derive name and skill id")

    chat_parser = subparsers.add_parser("chat", help="Load a skill schema and chat with it")
    chat_parser.add_argument("--schema", default="generated/distilled_skill.yaml", help="YAML skill schema file")
    chat_parser.add_argument("--prompt-pack", default=None, help="Optional prompt pack output path")
    chat_parser.add_argument("--mode", default="repl", choices=["repl", "print", "preview"], help="Chat mode")
    chat_parser.add_argument("--input", default=None, help="Optional initial user input")
    chat_parser.add_argument("--schema-dir", default=None, help="Directory containing distilled_skill.yaml")

    install_parser = subparsers.add_parser("install", help="Install the skill package to a target runtime")
    install_parser.add_argument("--target", required=True, help="Target runtime")
    install_parser.add_argument("--source", default=".", help="Source project directory")
    install_parser.add_argument("--dry-run", action="store_true", help="Show install destination without copying files")

    quality_parser = subparsers.add_parser("quality", help="Run quality checks for a skill schema")
    quality_parser.add_argument("--schema", default="generated/distilled_skill.yaml", help="YAML skill schema file")
    quality_parser.add_argument("--report", default="generated/quality_report.md", help="Path to the quality report")

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


def _collect_inputs(input_files: List[str], input_dir: str | None) -> List[str]:
    files = list(input_files)
    if input_dir:
        root = Path(input_dir)
        if root.exists():
            for suffix in ["*.txt", "*.md", "*.json"]:
                files.extend(str(p) for p in sorted(root.rglob(suffix)))
    return files


def cmd_distill(input_files: List[str], input_dir: str | None, schema_output: str, markdown_output: str, name: str, skill_id: str, config_path: str, query: str | None) -> int:
    if query:
        subject = normalize_subject(query)
        name = f"{subject} Skill"
        skill_id = infer_skill_slug(subject)
        print(f"[query] topic: {subject}")
        print(f"[query] name: {name}")
        print(f"[query] skill_id: {skill_id}")

    input_paths = _collect_inputs(input_files, input_dir)
    if not input_paths:
        print("No input materials provided.")
        return 1

    materials = []
    for item in input_paths:
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


def _resolve_schema_path(schema_path: str, schema_dir: str | None) -> str:
    if schema_dir:
        candidate = Path(schema_dir) / "distilled_skill.yaml"
        if candidate.exists():
            return str(candidate)
    return schema_path


def run_repl(schema: dict, initial_input: str | None) -> int:
    print(f"Loaded skill: {schema.get('name', 'Unknown')}")
    print("Type /exit to quit.")
    print("")

    if initial_input:
        print(f"skill> {initial_input}")
        print("")
        response = answer_with_runtime_context(schema, initial_input)
        print(response)
        print("")

    while True:
        try:
            user_text = input("skill> ").strip()
        except KeyboardInterrupt:
            print("\nBye.")
            return 0

        if user_text in {"/exit", "/quit"}:
            print("Bye.")
            return 0

        if not user_text:
            continue

        response = answer_with_runtime_context(schema, user_text)
        print("")
        print(response)
        print("")


def cmd_chat(schema_path: str, schema_dir: str | None, prompt_pack_output: str | None, mode: str, initial_input: str | None) -> int:
    schema_path = _resolve_schema_path(schema_path, schema_dir)
    schema = load_skill_schema(schema_path)
    errors = validate_skill_schema(schema)
    if errors:
        print("Schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    prompt_text = build_runtime_context(schema)
    if prompt_pack_output:
        save_prompt_pack(schema, prompt_pack_output)

    if mode == "print":
        print(prompt_text)
        return 0

    if mode == "preview":
        print(f"Loaded skill: {schema.get('name', 'Unknown')}")
        print(f"Version: {schema.get('versioning', {}).get('version', 'unknown')}")
        print("")
        print(prompt_text[:2000])
        return 0

    return run_repl(schema, initial_input)


def cmd_install(target: str, source: str, dry_run: bool) -> int:
    try:
        destination = install_skill_package(target=target, source_dir=source, dry_run=dry_run)
    except ValueError as exc:
        print(str(exc))
        return 1

    if dry_run:
        print(f"Would install to: {destination}")
        return 0

    print(f"Installed skill package to {destination}")
    return 0


def cmd_quality(schema_path: str, report_path: str) -> int:
    issues, report = quality_check_file(schema_path, report_path)
    print(report)
    return 1 if issues else 0


def cmd_auto_pipeline(query: str) -> int:
    schema, schema_path, markdown_path, prompt_pack_path = distill_from_query(query)
    report_path = quality_report_for_schema(schema_path)
    print(f"Auto distilled skill: {schema.get('name', 'Unknown')}")
    print(f"Schema: {schema_path}")
    print(f"Markdown: {markdown_path}")
    print(f"Prompt pack: {prompt_pack_path}")
    print(f"Quality report: {report_path}")
    print("")
    print("You can continue with:")
    print(f"python -m pangu_skill chat --schema {schema_path}")
    return 0


def cmd_natural(say: str, auto: bool = False) -> int:
    intent = detect_intent(say)
    if intent.intent == "distill":
        subject = normalize_subject(intent.subject)
        skill_id = infer_skill_slug(subject)
        print(f"[intent] distill -> {subject}")
        print(f"[intent] suggested skill_id -> {skill_id}")
        if auto:
            return cmd_auto_pipeline(subject)
        print("[intent] 准备好公开材料后，运行 distill 命令。");
        return 0
    if intent.intent == "chat":
        subject = normalize_subject(intent.subject)
        print(f"[intent] chat -> {subject}")
        print("[intent] 请先加载对应 skill 的 schema，然后用 chat 命令进入对话。")
        return 0
    print("[intent] 无法识别意图。你可以说：帮我蒸馏一个乔布斯 skill，或者用乔布斯 skill 回答我。")
    return 1


def main() -> int:
    args = parse_args()

    if getattr(args, "say", None):
        return cmd_natural(args.say, getattr(args, "auto", False))

    if not getattr(args, "command", None):
        print("No command provided. Use --say for natural language or a subcommand like distill/chat/quality.")
        return 1

    if args.command == "export":
        return cmd_export(args.schema, args.output)
    if args.command == "validate":
        return cmd_validate(args.schema)
    if args.command == "distill":
        return cmd_distill(args.input, args.input_dir, args.schema_output, args.markdown_output, args.name, args.skill_id, args.config, args.query)
    if args.command == "chat":
        return cmd_chat(args.schema, args.schema_dir, args.prompt_pack, args.mode, args.input)
    if args.command == "install":
        return cmd_install(args.target, args.source, args.dry_run)
    if args.command == "quality":
        return cmd_quality(args.schema, args.report)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
