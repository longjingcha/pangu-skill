from __future__ import annotations

import argparse
from pathlib import Path

from scripts._bootstrap import SRC  # noqa: F401

from pangu_skill.exporter import load_skill_schema, save_prompt_pack
from pangu_skill.intent import detect_intent, normalize_subject
from pangu_skill.runtime import answer_with_runtime_context, build_runtime_context


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chat with a distilled skill")
    parser.add_argument("--schema", required=False, default="generated/distilled_skill.yaml", help="Input YAML skill schema")
    parser.add_argument("--mode", default="repl", choices=["repl", "print", "preview"], help="Chat mode")
    parser.add_argument("--prompt-pack", default=None, help="Optional prompt pack output path")
    parser.add_argument("--input", default=None, help="Optional initial user input")
    parser.add_argument("--say", default=None, help="Natural language chat request")
    parser.add_argument("--schema-dir", default=None, help="Optional directory containing a distilled skill schema")
    return parser.parse_args()


def _resolve_schema_path(args: argparse.Namespace) -> str:
    if args.schema_dir:
        candidate = Path(args.schema_dir) / "distilled_skill.yaml"
        if candidate.exists():
            return str(candidate)
    return args.schema


def main() -> int:
    args = parse_args()

    if args.say:
        intent = detect_intent(args.say)
        if intent.intent == "chat":
            subject = normalize_subject(intent.subject)
            print(f"[natural] 我将使用 {subject} skill 进入对话")
            print("[natural] 请加载对应 skill 的 schema，再运行 chat。")
            return 0
        print("[natural] 当前只支持对话意图。你可以说：用乔布斯 skill 帮我分析这个产品")
        return 1

    schema_path = _resolve_schema_path(args)
    if not schema_path:
        print("Missing --schema")
        return 1

    schema = load_skill_schema(schema_path)
    context = build_runtime_context(schema)

    if args.prompt_pack:
        save_prompt_pack(schema, args.prompt_pack)

    if args.mode == "print":
        print(context)
        return 0

    if args.mode == "preview":
        print(f"Loaded skill: {schema.get('name', 'Unknown')}")
        print(f"Version: {schema.get('versioning', {}).get('version', 'unknown')}")
        print("")
        print(context[:2000])
        return 0

    print(f"Loaded skill: {schema.get('name', 'Unknown')}")
    print("Type /exit to quit.")
    print("")

    if args.input:
        print(f"skill> {args.input}")
        print("")
        print(answer_with_runtime_context(schema, args.input))
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
