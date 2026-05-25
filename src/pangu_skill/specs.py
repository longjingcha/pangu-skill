from __future__ import annotations

from typing import Dict, List


EXTRACTION_FOCUS: List[str] = [
    "expression_dna",
    "thinking_model",
    "decision_rules",
    "anti_patterns",
    "boundaries",
    "evidence",
    "conflicts",
    "dialogue_profile",
]

SKILL_TEMPLATE_SECTIONS: List[str] = [
    "基本信息",
    "总览",
    "来源信息",
    "思维模型",
    "决策规则",
    "表达 DNA",
    "对话 Profile",
    "反模式",
    "边界",
    "验证",
    "版本管理",
    "使用说明",
]

QUALITY_CHECK_ITEMS: List[str] = [
    "has_basic_fields",
    "has_summary",
    "has_sources",
    "has_thinking_model",
    "has_decision_rules",
    "has_expression_dna",
    "has_dialogue_profile",
    "has_boundaries",
    "has_validation",
    "has_versioning",
    "has_evidence",
    "has_conflicts",
]


def get_extraction_focus() -> List[str]:
    return list(EXTRACTION_FOCUS)


def get_skill_template_sections() -> List[str]:
    return list(SKILL_TEMPLATE_SECTIONS)


def get_quality_check_items() -> List[str]:
    return list(QUALITY_CHECK_ITEMS)


def default_quality_thresholds() -> Dict[str, float]:
    return {
        "min_confidence": 0.35,
        "preferred_confidence": 0.65,
        "high_confidence": 0.8,
    }
