import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.pangu_skill import cli


class CliTests(unittest.TestCase):
    def test_distill_command_runs_end_to_end(self):
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_path = tmp_path / "input.txt"
            input_path.write_text(
                "Clear structure is better than vague inspiration. Evidence first, then polish.",
                encoding="utf-8",
            )
            schema_output = tmp_path / "distilled.yaml"
            markdown_output = tmp_path / "distilled.md"

            with patch(
                "sys.argv",
                [
                    "pangu-skill",
                    "distill",
                    "--input",
                    str(input_path),
                    "--schema-output",
                    str(schema_output),
                    "--markdown-output",
                    str(markdown_output),
                    "--name",
                    "CLI Skill",
                    "--skill-id",
                    "cli.skill.001",
                ],
            ):
                exit_code = cli.main()

            self.assertEqual(exit_code, 0)
            self.assertTrue(schema_output.exists())
            self.assertTrue(markdown_output.exists())

    def test_validate_command_runs(self):
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            schema_path = tmp_path / "schema.yaml"
            schema_path.write_text(
                """
skill_id: "test.skill"
name: "Test Skill"
summary: "A test skill"
source:
  sources: ["a"]
  coverage: "low"
  confidence: 0.4
  notes: ""
thinking_model:
  core_beliefs: ["evidence first"]
  mental_models: ["first principles"]
  reasoning_style: ["structured"]
  heuristics: ["be conservative"]
  unknown_handling: ["state uncertainty"]
decision_rules:
  priorities: ["evidence"]
  tradeoffs: ["clarity over speed"]
  constraints: ["no invention"]
  escalation_logic: ["ask for more context"]
expression_dna:
  tone: ["clear"]
  style_traits: ["concise"]
  format_preferences: ["bullets"]
  language_patterns: ["explicit caveats"]
anti_patterns: ["overgeneralize"]
boundaries:
  scope: ["testing"]
  limitations: ["no private facts"]
  non_goals: ["roleplay"]
validation:
  test_questions: ["test?"]
  evaluation_metrics: ["consistency"]
  failure_modes: ["generic"]
versioning:
  version: "v1.0.0"
  status: "draft"
  changelog: ["initial"]
  iteration_notes: ["notes"]
""",
                encoding="utf-8",
            )

            with patch("sys.argv", ["pangu-skill", "validate", "--schema", str(schema_path)]):
                exit_code = cli.main()

            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
