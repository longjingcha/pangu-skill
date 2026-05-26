#!/usr/bin/env python3
"""
自动检查生成的SKILL.md是否通过Phase 4质量标准。

此版本同时支持：
- 人物协议检查
- 领域协议检查
- 开天信号检查

用法:
    python3 quality_check.py <SKILL.md路径>

示例:
    python3 quality_check.py .claude/skills/elon-musk-perspective/SKILL.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable, List, Tuple


def extract_section(content: str, heading_keywords: Tuple[str, ...]) -> str:
    """按标题关键字提取 section 内容。"""
    pattern = r"(?ms)^##\s+.*?(?:" + "|".join(map(re.escape, heading_keywords)) + r").*?\n(.*?)(?=\n##\s+|\Z)"
    m = re.search(pattern, content)
    return m.group(1) if m else ""



def count_bullets(text: str) -> int:
    return len(re.findall(r"^[-*]\s+", text, re.MULTILINE))



def check_person_models(content: str) -> Tuple[bool, str]:
    """检查人物协议模型数量（3-7个）"""
    section = extract_section(content, ("核心模型", "核心心智模型", "Models", "Mental Models"))
    if not section:
        return False, "❌ 未找到人物协议模型section"

    models = len(re.findall(r"^###\s+(?:模型|Model)\s*\d", section, re.MULTILINE))
    if models == 0:
        models = len(re.findall(r"^###\s+", section, re.MULTILINE))

    passed = 3 <= models <= 7
    return passed, f"{models}个模型 {'✅' if passed else '❌ (应为3-7个)'}"



def check_person_rules(content: str) -> Tuple[bool, str]:
    """检查人物协议规则数量（5-10条）"""
    section = extract_section(content, ("规则", "决策启发式", "Rules"))
    if not section:
        return False, "❌ 未找到人物协议规则section"

    rules = count_bullets(section)
    passed = 5 <= rules <= 10
    return passed, f"{rules}条规则 {'✅' if passed else '❌ (应为5-10条)'}"



def check_expression_rules(content: str) -> Tuple[bool, str]:
    """检查表达规则辨识度"""
    section = extract_section(content, ("表达规则", "表达DNA", "Expression Rules", "Expression DNA"))
    if not section:
        return False, "❌ 未找到表达规则section"

    markers = len(re.findall(r"句式|词汇|语气|幽默|节奏|确定性|引用|口癖|禁忌", section))
    passed = markers >= 3
    return passed, f"表达规则特征: {markers}项 {'✅' if passed else '❌ (应≥3项)'}"



def check_person_boundary(content: str) -> Tuple[bool, str]:
    """检查人物协议诚实边界"""
    section = extract_section(content, ("诚实边界", "Boundary"))
    if not section:
        return False, "❌ 未找到诚实边界section"

    items = count_bullets(section)
    passed = items >= 3
    return passed, f"人物边界: {items}条 {'✅' if passed else '❌ (应≥3条)'}"



def check_person_tension(content: str) -> Tuple[bool, str]:
    """检查人物协议内在张力"""
    section = extract_section(content, ("价值观与反模式", "智识谱系", "张力", "Tension"))
    if not section:
        return False, "❌ 未找到人物张力section"

    tension_markers = len(re.findall(r"张力|矛盾|一方面.*另一方面|既.*又", section))
    passed = tension_markers >= 2
    return passed, f"人物张力: {tension_markers}处 {'✅' if passed else '❌ (应≥2处)'}"



def check_domain_scope(content: str) -> Tuple[bool, str]:
    """检查领域协议边界是否明确"""
    hits = len(re.findall(r"\bscope\b|领域边界|子域", content, re.IGNORECASE))
    passed = hits >= 1
    return passed, f"领域边界信号: {hits}项 {'✅' if passed else '❌'}"



def check_domain_structure(content: str) -> Tuple[bool, str]:
    """检查领域协议结构是否完整"""
    needed = ["core_map", "criteria", "path", "pitfalls", "counterexamples", "failure_modes", "decision_actions"]
    hits = sum(1 for term in needed if re.search(rf"\b{re.escape(term)}\b", content))
    passed = hits >= 5
    return passed, f"领域结构字段: {hits}/{len(needed)} {'✅' if passed else '❌ (应≥5项)'}"



def check_domain_schools(content: str) -> Tuple[bool, str]:
    """检查领域协议是否保留流派分歧"""
    section = extract_section(content, ("流派分歧", "Schools", "分歧"))
    if not section:
        return False, "❌ 未找到流派分歧section"

    markers = len(re.findall(r"共识|分歧|流派|场景", section))
    passed = markers >= 2
    return passed, f"流派分歧信号: {markers}项 {'✅' if passed else '❌ (应≥2项)'}"



def check_domain_action(content: str) -> Tuple[bool, str]:
    """检查领域协议是否能落到动作"""
    section = extract_section(content, ("实战路径", "判断层", "行动层", "decision_actions"))
    if not section:
        return False, "❌ 未找到行动/路径section"

    markers = len(re.findall(r"先做什么|不要先做什么|路径|步骤|检查点|动作|行动", section))
    passed = markers >= 3
    return passed, f"行动信号: {markers}项 {'✅' if passed else '❌ (应≥3项)'}"



def check_opening_signal(content: str) -> Tuple[bool, str]:
    """检查是否有开天能力相关信号"""
    section = extract_section(content, ("开天判断", "开天能力", "问题重写", "重构问题"))
    if not section:
        return False, "❌ 未找到开天相关section"

    markers = len(re.findall(r"重写|重构|伪前提|伪问题|边界不清|表面症状|开天", section))
    passed = markers >= 2
    return passed, f"开天信号: {markers}项 {'✅' if passed else '❌ (应≥2项)'}"



def check_primary_sources(content: str) -> Tuple[bool, str]:
    """检查一手来源占比"""
    source_section = extract_section(content, ("附录：调研来源", "Sources", "来源"))
    if not source_section:
        return True, "未找到来源section（跳过检查）"

    primary = len(re.findall(r"一手|primary|原始|本人著作", source_section, re.IGNORECASE))
    secondary = len(re.findall(r"二手|secondary|转述|评论", source_section, re.IGNORECASE))
    total = primary + secondary
    if total == 0:
        return True, "未标记来源类型（跳过检查）"

    ratio = primary / total
    passed = ratio > 0.5
    return passed, f"一手来源占比: {primary}/{total} ({ratio:.0%}) {'✅' if passed else '❌ (应>50%)'}"



def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python3 quality_check.py <SKILL.md路径>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"❌ 文件不存在: {skill_path}")
        sys.exit(1)

    content = skill_path.read_text(encoding="utf-8")

    checks: List[Tuple[str, Callable[[str], Tuple[bool, str]]]] = [
        ("人物模型", check_person_models),
        ("人物规则", check_person_rules),
        ("表达规则", check_expression_rules),
        ("人物边界", check_person_boundary),
        ("人物张力", check_person_tension),
        ("领域边界", check_domain_scope),
        ("领域结构", check_domain_structure),
        ("流派分歧", check_domain_schools),
        ("领域动作", check_domain_action),
        ("开天信号", check_opening_signal),
        ("一手来源占比", check_primary_sources),
    ]

    print(f"质量检查: {skill_path.name}")
    print("=" * 50)

    passed_count = 0
    total = len(checks)

    for name, check_fn in checks:
        passed, detail = check_fn(content)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:<12} {status}  {detail}")
        if passed:
            passed_count += 1

    print("=" * 50)
    print(f"结果: {passed_count}/{total} 通过")

    if passed_count == total:
        print("🎉 全部通过，可以交付")
    elif passed_count >= total - 2:
        print("⚠️ 基本通过，建议修复不通过项后交付")
    else:
        print("❌ 多项不通过，建议回到Phase 2/3迭代")

    sys.exit(0 if passed_count == total else 1)


if __name__ == '__main__':
    main()
