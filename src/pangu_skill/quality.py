from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from .exporter import load_skill_schema, validate_skill_schema
from .specs import default_quality_thresholds, get_quality_check_items


def run_quality_check(schema: dict) -> List[str]:
    issues: List[str] = []
    required_items = set(get_quality_check_items())

    structural_errors = validate_skill_schema(schema)
    if structural_errors:
        issues.extend(structural_errors)

    source = schema.get("source", {}) or {}
    validation = schema.get("validation", {}) or {}
    dialogue_profile = schema.get("dialogue_profile", {}) or {}

    if not source.get("sources"):
        issues.append("No sources provided in source.sources")

    confidence = float(source.get("confidence", 0.0) or 0.0)
    thresholds = default_quality_thresholds()
    if confidence < thresholds["min_confidence"]:
        issues.append(f"Confidence too low ({confidence}); expected at least {thresholds['min_confidence']}")

    if not validation.get("evidence"):
        issues.append("validation.evidence is empty")
    if validation.get("conflicts") is None:
        issues.append("validation.conflicts is missing")
    if not dialogue_profile:
        issues.append("dialogue_profile is missing or empty")

    for item in required_items:
        if item == "has_basic_fields":
            if not all(schema.get(k) for k in ["skill_id", "name", "summary"]):
                issues.append("Basic fields are incomplete: skill_id/name/summary")
        elif item == "has_summary" and not schema.get("summary"):
            issues.append("summary is missing")
        elif item == "has_sources" and not source.get("sources"):
            issues.append("sources are missing")
        elif item == "has_thinking_model" and not schema.get("thinking_model"):
            issues.append("thinking_model is missing")
        elif item == "has_decision_rules" and not schema.get("decision_rules"):
            issues.append("decision_rules is missing")
        elif item == "has_expression_dna" and not schema.get("expression_dna"):
            issues.append("expression_dna is missing")
        elif item == "has_dialogue_profile" and not dialogue_profile:
            issues.append("dialogue_profile is missing")
        elif item == "has_boundaries" and not schema.get("boundaries"):
            issues.append("boundaries is missing")
        elif item == "has_validation" and not validation:
            issues.append("validation is missing")
        elif item == "has_versioning" and not schema.get("versioning"):
            issues.append("versioning is missing")
        elif item == "has_evidence" and not validation.get("evidence"):
            issues.append("validation.evidence is missing")
        elif item == "has_conflicts" and validation.get("conflicts") is None:
            issues.append("validation.conflicts is missing")

    return issues


def build_quality_report(schema: dict, issues: List[str]) -> str:
    lines: List[str] = []
    lines.append("# Quality Report")
    lines.append("")
    lines.append(f"- Skill ID: `{schema.get('skill_id', 'unknown')}`")
    lines.append(f"- Name: `{schema.get('name', 'Unnamed Skill')}`")
    lines.append(f"- Status: `{schema.get('versioning', {}).get('status', 'unknown')}`")
    lines.append(f"- Confidence: `{schema.get('source', {}).get('confidence', 0.0)}`")
    lines.append("")
    if not issues:
        lines.append("## Result")
        lines.append("")
        lines.append("- PASS")
        lines.append("- No blocking quality issues found.")
        return "\n".join(lines).rstrip() + "\n"

    lines.append("## Result")
    lines.append("")
    lines.append("- FAIL")
    lines.append("")
    lines.append("## Issues")
    lines.append("")
    for issue in issues:
        lines.append(f"- {issue}")
    return "\n".join(lines).rstrip() + "\n"


def quality_check_file(schema_path: str | Path, report_path: str | Path | None = None) -> Tuple[List[str], str]:
    schema = load_skill_schema(schema_path)
    issues = run_quality_check(schema)
    report = build_quality_report(schema, issues)

    if report_path is not None:
        output = Path(report_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")

    return issues, report
