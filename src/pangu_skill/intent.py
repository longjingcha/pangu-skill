from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class IntentResult:
    intent: str
    subject: Optional[str] = None
    skill_path: Optional[str] = None
    user_text: Optional[str] = None
    materials: Optional[List[str]] = None


DISTILL_PATTERNS = [
    r"蒸馏(.+?)skill",
    r"生成(.+?)skill",
    r"做一个(.+?)skill",
    r"造一个(.+?)skill",
]

CHAT_PATTERNS = [
    r"用(.+?)skill.*?(分析|回答|判断|帮我|看看)",
    r"切换到(.+?)",
    r"用(.+?)视角",
]


COMMON_PREFIXES = [
    "一个",
    "一位",
    "一名",
    "这个",
    "那个",
    "帮我蒸馏",
    "帮我生成",
    "帮我做一个",
    "帮我做个",
    "蒸馏一个",
    "蒸馏",
    "生成一个",
    "生成",
    "做一个",
    "做个",
    "造一个",
    "造个",
]


def clean_subject(subject: Optional[str]) -> str:
    if not subject:
        return ""
    text = subject.strip()
    changed = True
    while changed:
        changed = False
        for prefix in COMMON_PREFIXES:
            if text.startswith(prefix):
                text = text[len(prefix):].strip(" 、，。:：\t\n\r")
                changed = True
    text = re.sub(r"\s+", " ", text)
    return text.strip(" 、，。:：\t\n\r")


def detect_intent(text: str) -> IntentResult:
    raw = (text or "").strip()
    lowered = raw.lower()

    for pattern in DISTILL_PATTERNS:
        m = re.search(pattern, raw)
        if m:
            subject = clean_subject(m.group(1))
            return IntentResult(intent="distill", subject=subject, user_text=raw)

    for pattern in CHAT_PATTERNS:
        m = re.search(pattern, raw)
        if m:
            subject = clean_subject(m.group(1))
            return IntentResult(intent="chat", subject=subject, user_text=raw)

    if any(keyword in lowered for keyword in ["蒸馏", "生成", "做一个", "造一个"]):
        return IntentResult(intent="distill", user_text=raw)
    if any(keyword in lowered for keyword in ["回答", "分析", "判断", "解释", "看看", "用", "切换到"]):
        return IntentResult(intent="chat", user_text=raw)

    return IntentResult(intent="unknown", user_text=raw)


def normalize_subject(subject: Optional[str]) -> str:
    if not subject:
        return "Generated Skill"
    s = clean_subject(subject)
    s = re.sub(r"\s+", " ", s)
    return s if s else "Generated Skill"


def infer_skill_slug(subject: Optional[str]) -> str:
    if not subject:
        return "pangu.generated.001"
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", clean_subject(subject).strip().lower())
    slug = slug.strip("-") or "generated"
    return f"pangu.{slug}.001"


def collect_materials(paths: List[str]) -> List[str]:
    materials: List[str] = []
    for item in paths:
        path = Path(item)
        if path.exists() and path.is_file():
            materials.append(path.read_text(encoding="utf-8"))
    return materials
