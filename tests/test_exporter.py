import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.pangu_skill.distill_config import DistillConfig
from src.pangu_skill.exporter import (
    distill_skill_schema,
    save_skill_markdown,
    save_skill_schema,
    validate_skill_schema,
)


class ExporterTests(unittest.TestCase):
    def setUp(self):
        self.materials = [
            "Clear structure is better than vague inspiration. The system should prefer evidence-first reasoning, explicit boundaries, and short feedback loops.",
            "Speed matters during exploration, but clarity and correctness matter for high-stakes decisions.",
        ]
        self.config = DistillConfig(
            min_token_length=3,
            top_k_terms=8,
            summary_sentence_index=0,
            coverage_threshold=2,
            confidence_low=0.4,
            confidence_medium=0.6,
            stopwords=["than", "should", "during"],
        )

    def test_distill_skill_schema_includes_evidence_and_conflicts(self):
        schema = distill_skill_schema(self.materials, skill_id="test.skill.001", name="Test Skill", config=self.config)

        self.assertEqual(schema["skill_id"], "test.skill.001")
        self.assertEqual(schema["name"], "Test Skill")
        self.assertIn("source", schema)
        self.assertIn("validation", schema)
        self.assertIn("evidence", schema["validation"])
        self.assertIn("conflicts", schema["validation"])
        self.assertGreaterEqual(len(schema["validation"]["evidence"]), 1)
        self.assertGreaterEqual(len(schema["validation"]["conflicts"]), 1)

    def test_validate_skill_schema_passes_for_generated_schema(self):
        schema = distill_skill_schema(self.materials, config=self.config)
        errors = validate_skill_schema(schema)
        self.assertEqual(errors, [])

    def test_save_outputs(self):
        schema = distill_skill_schema(self.materials, config=self.config)
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            schema_path = save_skill_schema(schema, tmp_path / "skill.yaml")
            markdown_path = save_skill_markdown(schema, tmp_path / "SKILL.md")

            self.assertTrue(schema_path.exists())
            self.assertTrue(markdown_path.exists())
            self.assertIn("#", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
