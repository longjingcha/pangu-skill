from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import re
import yaml

from .distill_config import DistillConfig


DEFAULT_TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "SKILL.md"
DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "skill_schema.yaml"

REQUIRED_TOP_LEVEL_FIELDS: Sequence[str] = (
    "skill_id",
    "name",
    "summary",
    "source",
    "thinking_model",
    "decision_rules",
    "expression_dna",
    "anti_patterns",
    "boundaries",
    "validation",
    "versioning",
)


def load_skill_schema(path: str | Path = DEFAULT_SCHEMA_PATH) -> Dict[str, Any]:
    schema_path = Path(path)
    with schema_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("Skill schema must be a mapping/dictionary")
    return data


def validate_skill_schema(schema: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(schema, dict):
        return ["Schema must be a dictionary"]
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in schema:
            errors.append(f"Missing required top-level field: {field}")
    for field in ("source", "thinking_model", "decision_rules", "expression_dna", "boundaries", "validation", "versioning"):
        if field in schema and not isinstance(schema.get(field), dict):
            errors.append(f"Field '{field}' must be a dictionary")
    return errors


def _bullet_list(items: Iterable[Any]) -> str:
    values = list(items or [])
    if not values:
        return "- None"
    return "\n".join(f"- {item}" for item in values)


def _tokenize(text: str, config: DistillConfig) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_\-]{%d,}" % (config.min_token_length - 1), text.lower())
    stopwords = set(config.stopwords)
    return [word for word in words if word not in stopwords]


def _extract_summary(sentences: List[str], config: DistillConfig) -> str:
    if not sentences:
        return "Auto-generated skill distilled from provided materials."
    index = min(max(config.summary_sentence_index, 0), len(sentences) - 1)
    return sentences[index]


def _split_sentences(text: str) -> List[str]:
    return [segment.strip() for segment in re.split(r"[\n\.\!\?]+", text) if segment.strip()]


def _collect_evidence(materials: Sequence[str], config: DistillConfig) -> Tuple[Counter, Dict[str, List[int]], List[str]]:
    combined_text = "\n".join(materials)
    tokens = _tokenize(combined_text, config)
    counts = Counter(tokens)
    sentence_bank = []
    for material in materials:
        sentence_bank.extend(_split_sentences(material))

    evidence_map: Dict[str, List[int]] = defaultdict(list)
    for idx, sentence in enumerate(sentence_bank):
        sentence_tokens = set(_tokenize(sentence, config))
        for token in sentence_tokens:
            if token in counts:
                evidence_map[token].append(idx)
    return counts, evidence_map, sentence_bank


def distill_skill_schema(
    materials: Sequence[str],
    skill_id: str = "pangu.generated.001",
    name: str = "Generated Skill",
    config: DistillConfig | None = None,
) -> Dict[str, Any]:
    config = config or DistillConfig.load()
    combined_text = "\n".join(materials)
    counts, evidence_map, sentence_bank = _collect_evidence(materials, config)
    top_terms = [term for term, _ in counts.most_common(config.top_k_terms)]
    short_summary = _extract_summary(_split_sentences(combined_text), config)

    theme_phrases = top_terms[: min(5, len(top_terms))]
    recurring_evidence = [term for term in top_terms if counts[term] >= config.coverage_threshold]

    coverage = "low"
    if len(recurring_evidence) >= 5:
        coverage = "high"
    elif len(recurring_evidence) >= 3:
        coverage = "medium"

    confidence = config.confidence_low
    if coverage == "medium":
        confidence = config.confidence_medium
    elif coverage == "high":
        confidence = config.confidence_high

    evidence_items = []
    for term in theme_phrases:
        locations = evidence_map.get(term, [])
        supporting_sentences = []
        for idx in locations[:3]:
            if 0 <= idx < len(sentence_bank):
                supporting_sentences.append(sentence_bank[idx])
        evidence_items.append({
            "claim": f"Theme around '{term}' appears repeatedly",
            "support": supporting_sentences,
            "source_count": len(locations),
            "confidence": round(min(0.95, 0.45 + 0.08 * len(locations)), 2),
        })

    conflicts = []
    high_freq_terms = [term for term in top_terms if counts[term] >= max(2, config.coverage_threshold - 1)]
    if {"clarity", "clear"}.issubset(set(counts)) and {"speed", "fast", "rapid"}.intersection(counts):
        conflicts.append({
            "topic": "clarity_vs_speed",
            "description": "Materials emphasize both clarity and speed; treat as a tradeoff rather than a single priority.",
            "evidence": [
                "Evidence shows repeated mentions of clarity-oriented language.",
                "Evidence also shows repeated mentions of speed/iteration-oriented language.",
            ],
            "resolution": "Model as a context-dependent tradeoff: clarity for high-stakes tasks, speed for exploration.",
        })
    elif len(high_freq_terms) >= 2:
        conflicts.append({
            "topic": "competing_themes",
            "description": "Multiple high-frequency themes compete for primacy.",
            "evidence": [f"Recurring terms include: {', '.join(high_freq_terms[:4])}."] ,
            "resolution": "Keep the model conservative until more source material clarifies priority order.",
        })

    core_beliefs = ["Begin with explicit evidence before inferring a stable pattern."]
    heuristics = ["When evidence is sparse, keep the first-pass model conservative."]
    reasoning_style = ["Starts from observable evidence and then abstracts toward patterns."]
    decision_constraints = ["Do not invent unsupported claims from insufficient evidence."]
    anti_patterns = ["Avoid treating the first draft as final truth."]
    boundary_notes = ["This is a first-pass distillation and should be refined with more materials."]

    if theme_phrases:
        core_beliefs.insert(0, f"Repeated themes center on: {', '.join(theme_phrases[:5])}.")
        heuristics.insert(0, f"Prioritize recurring themes such as: {', '.join(theme_phrases[:3])}.")

    if any(word in counts for word in ("clarity", "clear")):
        reasoning_style.append("Prefers clarity and explicit structure.")
    if any(word in counts for word in ("speed", "fast", "rapid")):
        reasoning_style.append("Values rapid iteration and short feedback loops.")
    if any(word in counts for word in ("quality", "correct", "accuracy")):
        decision_constraints.append("Avoid tradeoffs that sacrifice correctness without explicit rationale.")
    if any(word in counts for word in ("boundary", "limit", "scope")):
        boundary_notes.append("Materials explicitly discuss scope or limitation boundaries.")
    if any(word in counts for word in ("avoid", "not", "never")):
        anti_patterns.append("Avoid overgeneralization and unsupported leaps.")

    if not any(word in counts for word in ("clarity", "clear", "structured")):
        reasoning_style.append("Uses structure to compensate for ambiguous inputs.")

    schema: Dict[str, Any] = {
        "skill_id": skill_id,
        "name": name,
        "summary": short_summary,
        "source": {
            "sources": list(materials),
            "coverage": coverage,
            "confidence": round(confidence, 2),
            "notes": "Auto-distilled from raw materials with configurable heuristics.",
        },
        "thinking_model": {
            "core_beliefs": core_beliefs,
            "mental_models": [
                "Evidence-first abstraction",
                f"Recurring themes: {', '.join(theme_phrases[:5])}" if theme_phrases else "Recurring themes unavailable",
            ],
            "reasoning_style": reasoning_style,
            "heuristics": heuristics,
            "unknown_handling": ["State uncertainty explicitly.", "Request more evidence when the signal is weak."],
        },
        "decision_rules": {
            "priorities": ["Evidence before inference", "Structure before polish"],
            "tradeoffs": ["Prefer conservative claims on a first pass"],
            "constraints": decision_constraints,
            "escalation_logic": ["Ask for more source material if the pattern is ambiguous."],
        },
        "expression_dna": {
            "tone": ["clear", "direct"],
            "style_traits": ["structured", "concise"],
            "format_preferences": ["bullets first", "conclusion first"],
            "language_patterns": ["uses explicit caveats when confidence is low"],
        },
        "anti_patterns": anti_patterns,
        "boundaries": {
            "scope": ["First-pass distillation from provided materials"],
            "limitations": ["Cannot infer facts not present in the source"],
            "non_goals": ["Not a final expert model", "Not a roleplay generator"],
        },
        "validation": {
            "test_questions": [
                "What patterns recur across the provided materials?",
                "Where is the evidence weak or contradictory?",
                "Which conclusions are most defensible in a first pass?",
            ],
            "evaluation_metrics": ["consistency", "boundary_awareness", "distinctiveness"],
            "failure_modes": ["becomes generic", "overfits a single source", "claims certainty without evidence"],
            "evidence": evidence_items,
            "conflicts": conflicts,
        },
        "versioning": {
            "version": "v1.2.0",
            "status": "draft",
            "changelog": ["Added evidence structure, conflict detection, and multi-material comparison."],
            "iteration_notes": ["Promote recurring themes only when supported by multiple sources."],
        },
    }
    return schema


def save_skill_schema(schema: Dict[str, Any], output_path: str | Path) -> Path:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(schema, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return target


def build_skill_markdown(schema: Dict[str, Any]) -> str:
    source = schema.get("source", {}) or {}
    thinking_model = schema.get("thinking_model", {}) or {}
    decision_rules = schema.get("decision_rules", {}) or {}
    expression_dna = schema.get("expression_dna", {}) or {}
    boundaries = schema.get("boundaries", {}) or {}
    validation = schema.get("validation", {}) or {}
    versioning = schema.get("versioning", {}) or {}

    lines: List[str] = []
    lines.append(f"# {schema.get('name', '').strip() or 'Unnamed Skill'}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(schema.get("summary", "").strip() or "No summary provided.")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"- Skill ID: `{schema.get('skill_id', '').strip() or 'unknown'}`")
    lines.append(f"- Coverage: `{source.get('coverage', 'low')}`")
    lines.append(f"- Confidence: `{source.get('confidence', 0.0)}`")
    notes = source.get("notes", "")
    if notes:
        lines.append(f"- Notes: {notes}")
    lines.append("")
    lines.append("### Materials")
    lines.append(_bullet_list(source.get("sources", [])))
    lines.append("")

    section_map = [
        ("Thinking Model", [
            ("Core Beliefs", thinking_model.get("core_beliefs", [])),
            ("Mental Models", thinking_model.get("mental_models", [])),
            ("Reasoning Style", thinking_model.get("reasoning_style", [])),
            ("Heuristics", thinking_model.get("heuristics", [])),
            ("Unknown Handling", thinking_model.get("unknown_handling", [])),
        ]),
        ("Decision Rules", [
            ("Priorities", decision_rules.get("priorities", [])),
            ("Tradeoffs", decision_rules.get("tradeoffs", [])),
            ("Constraints", decision_rules.get("constraints", [])),
            ("Escalation Logic", decision_rules.get("escalation_logic", [])),
        ]),
        ("Expression DNA", [
            ("Tone", expression_dna.get("tone", [])),
            ("Style Traits", expression_dna.get("style_traits", [])),
            ("Format Preferences", expression_dna.get("format_preferences", [])),
            ("Language Patterns", expression_dna.get("language_patterns", [])),
        ]),
    ]

    for heading, subsections in section_map:
        lines.append(f"## {heading}")
        lines.append("")
        for subsection, items in subsections:
            lines.append(f"### {subsection}")
            lines.append(_bullet_list(items))
            lines.append("")

    lines.append("## Anti-patterns")
    lines.append("")
    lines.append(_bullet_list(schema.get("anti_patterns", [])))
    lines.append("")

    lines.append("## Boundaries")
    lines.append("")
    lines.append("### Scope")
    lines.append(_bullet_list(boundaries.get("scope", [])))
    lines.append("")
    lines.append("### Limitations")
    lines.append(_bullet_list(boundaries.get("limitations", [])))
    lines.append("")
    lines.append("### Non-goals")
    lines.append(_bullet_list(boundaries.get("non_goals", [])))
    lines.append("")

    lines.append("## Validation")
    lines.append("")
    lines.append("### Test Questions")
    lines.append(_bullet_list(validation.get("test_questions", [])))
    lines.append("")
    lines.append("### Evaluation Metrics")
    lines.append(_bullet_list(validation.get("evaluation_metrics", [])))
    lines.append("")
    lines.append("### Failure Modes")
    lines.append(_bullet_list(validation.get("failure_modes", [])))
    lines.append("")
    lines.append("### Evidence")
    evidence = validation.get("evidence", []) or []
    if evidence:
        for item in evidence:
            lines.append(f"- Claim: {item.get('claim', '')}")
            lines.append(f"  - Support count: {item.get('source_count', 0)}")
            lines.append(f"  - Confidence: {item.get('confidence', 0.0)}")
            for support in item.get("support", []):
                lines.append(f"  - Support: {support}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("### Conflicts")
    conflicts = validation.get("conflicts", []) or []
    if conflicts:
        for item in conflicts:
            lines.append(f"- Topic: {item.get('topic', '')}")
            lines.append(f"  - Description: {item.get('description', '')}")
            for evidence_line in item.get("evidence", []):
                lines.append(f"  - Evidence: {evidence_line}")
            lines.append(f"  - Resolution: {item.get('resolution', '')}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Versioning")
    lines.append("")
    lines.append(f"- Version: `{versioning.get('version', 'v1.0.0')}`")
    lines.append(f"- Status: `{versioning.get('status', 'draft')}`")
    lines.append("")
    lines.append("### Changelog")
    lines.append(_bullet_list(versioning.get("changelog", [])))
    lines.append("")
    lines.append("### Iteration Notes")
    lines.append(_bullet_list(versioning.get("iteration_notes", [])))
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def save_skill_markdown(schema: Dict[str, Any], output_path: str | Path) -> Path:
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_skill_markdown(schema), encoding="utf-8")
    return target
