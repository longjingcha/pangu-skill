#!/usr/bin/env python3
"""
合并6个Agent的调研结果，生成Phase 1.5调研Review检查点的摘要表格。

它不仅统计来源数量、一手/二手占比和关键发现，还会额外提示：
- 人物协议是否存在明显缺口
- 领域协议是否存在明显缺口
- 是否出现需要“开天”的信号（原问题需要重构）
- 是否应优先走人物协议、领域协议，或先重写问题

用法:
    python3 merge_research.py <skill目录路径>

示例:
    python3 merge_research.py .claude/skills/elon-musk-perspective

输出: 打印markdown格式的摘要表格到stdout
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

AGENTS = {
    "01-writings": "著作",
    "02-conversations": "对话",
    "03-expression-dna": "表达",
    "04-external-views": "他者",
    "05-decisions": "决策",
    "06-timeline": "时间线",
}

PERSON_PROTOCOL_TERMS = [
    "模型",
    "规则",
    "表达规则",
    "边界",
    "张力",
    "诚实边界",
]

DOMAIN_PROTOCOL_TERMS = [
    "scope",
    "core_map",
    "criteria",
    "path",
    "pitfalls",
    "counterexamples",
    "failure_modes",
    "schools",
    "progression",
    "decision_actions",
]

OPENING_TERMS = [
    "重写问题",
    "开天",
    "伪问题",
    "伪前提",
    "边界不清",
    "表面症状",
    "问题本身",
]


def count_sources(content: str) -> Dict[str, int]:
    """统计来源数量和一手/二手占比"""
    urls = re.findall(r"https?://[^\s\)]+", content)
    primary_markers = len(re.findall(r"一手|primary|本人|原文|原始|直接引用", content, re.IGNORECASE))
    secondary_markers = len(re.findall(r"二手|secondary|转述|总结|评论|分析", content, re.IGNORECASE))
    return {
        "url_count": len(urls),
        "unique_urls": len(set(urls)),
        "primary_markers": primary_markers,
        "secondary_markers": secondary_markers,
    }


def extract_key_findings(content: str, max_items: int = 3) -> List[str]:
    """提取关键发现：优先标题，其次加粗项，最后前几行摘要"""
    headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
    if headings:
        return headings[:max_items]

    bolds = re.findall(r"\*\*(.+?)\*\*", content)
    if bolds:
        return bolds[:max_items]

    lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")]
    return [l[:50] + "..." if len(l) > 50 else l for l in lines[:max_items]]


def section_text(content: str, heading_keywords: Tuple[str, ...]) -> str:
    """按标题关键字提取 section 内容。"""
    pattern = r"(?ms)^##\s+.*?(?:" + "|".join(map(re.escape, heading_keywords)) + r").*?\n(.*?)(?=\n##\s+|\Z)"
    m = re.search(pattern, content)
    return m.group(1) if m else ""


def has_terms(content: str, terms: List[str]) -> int:
    """统计一组术语出现次数。"""
    total = 0
    for term in terms:
        total += len(re.findall(re.escape(term), content, re.IGNORECASE))
    return total


def detect_person_protocol_gap(files: Dict[str, str]) -> List[str]:
    """检测人物协议可能缺失的信号。"""
    combined = "\n".join(files.values())
    signals = []

    model_count = len(re.findall(r"(?:模型|心智模型|model)\d*", combined, re.IGNORECASE))
    rule_count = len(re.findall(r"(?:规则|决策启发式|heuristic)\d*", combined, re.IGNORECASE))
    expression_count = len(re.findall(r"(?:表达规则|表达DNA|expression)\d*", combined, re.IGNORECASE))
    boundary_count = len(re.findall(r"(?:诚实边界|局限|边界|boundary)\d*", combined, re.IGNORECASE))

    if model_count < 3:
        signals.append("人物协议模型偏少")
    if rule_count < 5:
        signals.append("人物协议规则偏少")
    if expression_count < 3:
        signals.append("表达规则信号偏少")
    if boundary_count < 3:
        signals.append("边界/局限标注偏少")

    return signals



def detect_domain_protocol_gap(files: Dict[str, str]) -> List[str]:
    """检测领域协议可能缺失的信号。"""
    combined = "\n".join(files.values())
    signals = []

    scope = has_terms(combined, ["scope", "边界"])
    core_map = has_terms(combined, ["core_map", "结构", "框架"])
    criteria = has_terms(combined, ["criteria", "标准", "判断"])
    path = has_terms(combined, ["path", "路径", "路线图"])
    failure = has_terms(combined, ["failure_modes", "失效", "不适用"])
    schools = has_terms(combined, ["schools", "流派", "分歧"])
    actions = has_terms(combined, ["decision_actions", "动作", "行动"])

    if scope < 1:
        signals.append("领域边界不够明确")
    if core_map < 2:
        signals.append("领域结构图偏弱")
    if criteria < 2:
        signals.append("判断标准偏弱")
    if path < 2:
        signals.append("实战路径偏弱")
    if failure < 1:
        signals.append("失效条件偏弱")
    if schools < 1:
        signals.append("流派分歧信号偏弱")
    if actions < 1:
        signals.append("可执行动作不足")

    return signals



def detect_opening_signals(files: Dict[str, str]) -> List[str]:
    """检测是否存在开天/重写问题信号。"""
    combined = "\n".join(files.values())
    matches = []
    for term in OPENING_TERMS:
        if term in combined:
            matches.append(term)
    return matches[:8]



def infer_route(person_gap: List[str], domain_gap: List[str], opening_hits: List[str]) -> str:
    """推断接下来应该走哪条路线。"""
    if opening_hits and len(opening_hits) >= 2:
        return "优先重写问题（开天信号明显）"
    if person_gap and not domain_gap:
        return "优先补人物协议"
    if domain_gap and not person_gap:
        return "优先补领域协议"
    if person_gap and domain_gap:
        return "人物协议与领域协议都需要补强"
    return "当前协议结构基本齐备"


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python3 merge_research.py <skill目录路径>")
        sys.exit(1)

    skill_dir = Path(sys.argv[1])
    research_dir = skill_dir / "references" / "research"

    if not research_dir.exists():
        print(f"❌ 目录不存在: {research_dir}")
        sys.exit(1)

    files: Dict[str, str] = {}
    rows: List[str] = []
    total_sources = 0
    total_primary = 0
    total_secondary = 0
    missing: List[str] = []

    for key, label in AGENTS.items():
        md_file = research_dir / f"{key}.md"
        if not md_file.exists():
            missing.append(label)
            rows.append(f"│ {label:<12} │ {'❌ 缺失':<8} │ {'—':<24} │")
            continue

        content = md_file.read_text(encoding="utf-8")
        files[key] = content
        stats = count_sources(content)
        findings = extract_key_findings(content)

        total_sources += stats["unique_urls"]
        total_primary += stats["primary_markers"]
        total_secondary += stats["secondary_markers"]

        findings_str = ", ".join(findings) if findings else "—"
        if len(findings_str) > 40:
            findings_str = findings_str[:37] + "..."

        rows.append(f"│ {label:<12} │ {stats['unique_urls']:<8} │ {findings_str:<24} │")

    contradictions = find_contradictions(files)
    person_gap = detect_person_protocol_gap(files)
    domain_gap = detect_domain_protocol_gap(files)
    opening_hits = detect_opening_signals(files)
    route = infer_route(person_gap, domain_gap, opening_hits)

    print("┌──────────────┬──────────┬──────────────────────────┐")
    print("│ Agent        │ 来源数量  │ 关键发现                  │")
    print("├──────────────┼──────────┼──────────────────────────┤")
    for row in rows:
        print(row)
    print("├──────────────┼──────────┼──────────────────────────┤")

    primary_ratio = f"{total_primary}/{total_primary + total_secondary}" if (total_primary + total_secondary) > 0 else "未标记"
    print(f"│ 总来源数      │ {total_sources:<8} │ 一手占比: {primary_ratio:<15} │")

    if contradictions:
        print(f"│ 矛盾点        │ {len(contradictions)}处      │ {contradictions[0][:24]:<24} │")
    else:
        print(f"│ 矛盾点        │ 0处      │ {'—':<24} │")

    if missing:
        print(f"│ 信息不足维度   │ {len(missing)}个      │ {', '.join(missing):<24} │")
    else:
        print(f"│ 信息不足维度   │ 无       │ {'—':<24} │")

    print("└──────────────┴──────────┴──────────────────────────┘")

    print("\n┌──────────────────────────┬────────────────────────────────────────────┐")
    print("│ 协议信号                  │ 诊断                                         │")
    print("├──────────────────────────┼────────────────────────────────────────────┤")
    print(f"│ 人物协议缺口              │ {', '.join(person_gap) if person_gap else '未发现明显缺口':<42} │")
    print(f"│ 领域协议缺口              │ {', '.join(domain_gap) if domain_gap else '未发现明显缺口':<42} │")
    print(f"│ 开天信号                  │ {', '.join(opening_hits) if opening_hits else '未发现明显信号':<42} │")
    print(f"│ 建议路线                  │ {route:<42} │")
    print("└──────────────────────────┴────────────────────────────────────────────┘")

    if total_sources < 10:
        print("\n⚠️ 总来源数 <10，建议降低期望或补充调研")
    if missing:
        print(f"\n⚠️ 缺失维度: {', '.join(missing)}，建议补充或在诚实边界中标注")
    if person_gap or domain_gap:
        print("\n⚠️ 协议不平衡：建议优先补强缺口部分，再进入 Phase 2/3")
    if opening_hits and len(opening_hits) >= 2:
        print("\n⚠️ 开天信号明显：建议先重写问题，再继续协议构建")


if __name__ == "__main__":
    main()
