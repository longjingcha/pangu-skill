from __future__ import annotations

from typing import Any, Dict, List, Tuple


DEFAULT_OUTPUT_TEMPLATE = "结论 → 原因 → 风险 → 需要补充的信息"


JOIBS_LIKE_HINTS = ("乔布斯", "steve jobs", "jobs")
NAVAL_LIKE_HINTS = ("naval",)
MUSK_LIKE_HINTS = ("马斯克", "elon", "musk")


def _as_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def _join_bullets(items: List[str]) -> str:
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)


def _extract_sections(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "skill_id": schema.get("skill_id", "unknown"),
        "name": schema.get("name", "Unnamed Skill"),
        "summary": schema.get("summary", ""),
        "source": schema.get("source", {}) or {},
        "thinking_model": schema.get("thinking_model", {}) or {},
        "decision_rules": schema.get("decision_rules", {}) or {},
        "expression_dna": schema.get("expression_dna", {}) or {},
        "dialogue_profile": schema.get("dialogue_profile", {}) or {},
        "anti_patterns": schema.get("anti_patterns", []) or [],
        "boundaries": schema.get("boundaries", {}) or {},
        "validation": schema.get("validation", {}) or {},
        "versioning": schema.get("versioning", {}) or {},
    }


def _persona_mode(name: str) -> str:
    lowered = (name or "").lower()
    if any(hint.lower() in lowered for hint in JOIBS_LIKE_HINTS):
        return "jobs"
    if any(hint.lower() in lowered for hint in NAVAL_LIKE_HINTS):
        return "naval"
    if any(hint.lower() in lowered for hint in MUSK_LIKE_HINTS):
        return "musk"
    return "default"


def build_runtime_context(schema: Dict[str, Any]) -> str:
    sections = _extract_sections(schema)
    dialogue_profile = sections["dialogue_profile"]
    source = sections["source"]
    thinking_model = sections["thinking_model"]
    decision_rules = sections["decision_rules"]
    expression_dna = sections["expression_dna"]
    boundaries = sections["boundaries"]
    validation = sections["validation"]
    versioning = sections["versioning"]

    lines: List[str] = []
    lines.append("# Runtime Context")
    lines.append("")
    lines.append("## 基本信息")
    lines.append(f"- Skill ID: `{sections['skill_id']}`")
    lines.append(f"- 名称: `{sections['name']}`")
    lines.append(f"- 版本: `{versioning.get('version', 'unknown')}`")
    lines.append(f"- 状态: `{versioning.get('status', 'unknown')}`")
    lines.append("")

    lines.append("## 总览")
    lines.append(sections["summary"] or "无")
    lines.append("")

    lines.append("## 来源信息")
    lines.append(f"- 覆盖程度: `{source.get('coverage', 'low')}`")
    lines.append(f"- 可信度: `{source.get('confidence', 0.0)}`")
    if source.get("notes"):
        lines.append(f"- 说明: {source.get('notes')}")
    lines.append("")
    lines.append("### 证据说明")
    lines.append(_join_bullets(_as_list(source.get("evidence_notes", []))))
    lines.append("")

    lines.append("## 思维模型")
    lines.append("### 核心信念")
    lines.append(_join_bullets(_as_list(thinking_model.get("core_beliefs", []))))
    lines.append("")
    lines.append("### 常用心智模型")
    lines.append(_join_bullets(_as_list(thinking_model.get("mental_models", []))))
    lines.append("")
    lines.append("### 推理风格")
    lines.append(_join_bullets(_as_list(thinking_model.get("reasoning_style", []))))
    lines.append("")
    lines.append("### 启发式")
    lines.append(_join_bullets(_as_list(thinking_model.get("heuristics", []))))
    lines.append("")
    lines.append("### 不确定性处理")
    lines.append(_join_bullets(_as_list(thinking_model.get("unknown_handling", []))))
    lines.append("")

    lines.append("## 决策规则")
    lines.append("### 优先级")
    lines.append(_join_bullets(_as_list(decision_rules.get("priorities", []))))
    lines.append("")
    lines.append("### 取舍逻辑")
    lines.append(_join_bullets(_as_list(decision_rules.get("tradeoffs", []))))
    lines.append("")
    lines.append("### 约束条件")
    lines.append(_join_bullets(_as_list(decision_rules.get("constraints", []))))
    lines.append("")
    lines.append("### 升级逻辑")
    lines.append(_join_bullets(_as_list(decision_rules.get("escalation_logic", []))))
    lines.append("")

    lines.append("## 表达 DNA")
    lines.append("### 语气")
    lines.append(_join_bullets(_as_list(expression_dna.get("tone", []))))
    lines.append("")
    lines.append("### 风格特征")
    lines.append(_join_bullets(_as_list(expression_dna.get("style_traits", []))))
    lines.append("")
    lines.append("### 排版偏好")
    lines.append(_join_bullets(_as_list(expression_dna.get("format_preferences", []))))
    lines.append("")
    lines.append("### 语言习惯")
    lines.append(_join_bullets(_as_list(expression_dna.get("language_patterns", []))))
    lines.append("")

    lines.append("## 对话 Profile")
    lines.append("### 人格摘要")
    lines.append(dialogue_profile.get("persona_summary", "无"))
    lines.append("")
    lines.append("### 默认语气")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("default_tone", []))))
    lines.append("")
    lines.append("### 回复原则")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("response_principles", []))))
    lines.append("")
    lines.append("### 回答策略")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("answering_strategy", []))))
    lines.append("")
    lines.append("### 追问策略")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("questioning_strategy", []))))
    lines.append("")
    lines.append("### 不确定性处理")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("uncertainty_handling", []))))
    lines.append("")
    lines.append("### 拒绝方式")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("refusal_style", []))))
    lines.append("")
    lines.append("### 输出模板")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("output_templates", [])) or [DEFAULT_OUTPUT_TEMPLATE]))
    lines.append("")
    lines.append("### 切换规则")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("switching_rules", []))))
    lines.append("")
    lines.append("### 示例问题")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("example_prompts", []))))
    lines.append("")
    lines.append("### 示例回答")
    lines.append(_join_bullets(_as_list(dialogue_profile.get("example_responses", []))))
    lines.append("")

    lines.append("## 反模式")
    lines.append(_join_bullets(_as_list(sections["anti_patterns"])))
    lines.append("")

    lines.append("## 边界")
    lines.append("### 适用范围")
    lines.append(_join_bullets(_as_list(boundaries.get("scope", []))))
    lines.append("")
    lines.append("### 限制")
    lines.append(_join_bullets(_as_list(boundaries.get("limitations", []))))
    lines.append("")
    lines.append("### 非目标")
    lines.append(_join_bullets(_as_list(boundaries.get("non_goals", []))))
    lines.append("")

    lines.append("## 验证")
    lines.append("### 测试问题")
    lines.append(_join_bullets(_as_list(validation.get("test_questions", []))))
    lines.append("")
    lines.append("### 评估指标")
    lines.append(_join_bullets(_as_list(validation.get("evaluation_metrics", []))))
    lines.append("")
    lines.append("### 失败模式")
    lines.append(_join_bullets(_as_list(validation.get("failure_modes", []))))
    lines.append("")
    lines.append("### 对话测试")
    lines.append(_join_bullets(_as_list(validation.get("dialogue_tests", []))))
    lines.append("")

    lines.append("## 版本管理")
    lines.append(f"- 版本: `{versioning.get('version', 'unknown')}`")
    lines.append(f"- 状态: `{versioning.get('status', 'unknown')}`")
    lines.append("### 更新日志")
    lines.append(_join_bullets(_as_list(versioning.get("changelog", []))))
    lines.append("")
    lines.append("### 迭代说明")
    lines.append(_join_bullets(_as_list(versioning.get("iteration_notes", []))))
    lines.append("")

    lines.append("## 使用说明")
    lines.append("- 可作为对话前置上下文")
    lines.append("- 可作为 agent skill 加载")
    lines.append("- 可作为手动参考资料粘贴")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_system_prompt(schema: Dict[str, Any]) -> str:
    sections = _extract_sections(schema)
    dialogue_profile = sections["dialogue_profile"]
    template = _as_list(dialogue_profile.get("output_templates", []))
    output_template = template[0] if template else DEFAULT_OUTPUT_TEMPLATE

    prompt_lines: List[str] = []
    prompt_lines.append(f"你正在按照一个 skill 运行。Skill 名称：{sections['name']}。")
    prompt_lines.append(f"Skill ID：{sections['skill_id']}。")
    prompt_lines.append(f"总览：{sections['summary'] or '无'}。")
    prompt_lines.append("")
    prompt_lines.append("你必须遵守以下规则：")
    prompt_lines.append("1. 优先遵守对话 Profile、决策规则、边界和反模式。")
    prompt_lines.append("2. 不知道就明确说不知道，不要硬猜。")
    prompt_lines.append("3. 先结论，再原因，再风险，再补充信息。")
    prompt_lines.append("4. 如果用户问题超出边界，礼貌拒绝并给出替代帮助。")
    prompt_lines.append("5. 保持与表达 DNA 一致的语气和节奏。")
    prompt_lines.append("")
    prompt_lines.append(f"默认输出模板：{output_template}")
    prompt_lines.append(f"人格模式：{_persona_mode(sections['name'])}")
    return "\n".join(prompt_lines).rstrip()


def detect_question_type(user_text: str) -> str:
    text = user_text.strip().lower()
    if any(keyword in text for keyword in ["风险", "值不值得", "投资", "worth", "risk", "投"]):
        return "decision"
    if any(keyword in text for keyword in ["怎么", "如何", "how", "步骤", "方法"]):
        return "howto"
    if any(keyword in text for keyword in ["为什么", "原理", "解释", "what", "why"]):
        return "explain"
    if any(keyword in text for keyword in ["能不能", "是否", "可不可以", "边界", "限制"]):
        return "boundary"
    return "general"


def choose_output_template(dialogue_profile: Dict[str, Any], question_type: str) -> str:
    templates = _as_list(dialogue_profile.get("output_templates", []))
    if templates:
        return templates[0]
    mapping = {
        "decision": "结论 → 原因 → 风险 → 需要补充的信息",
        "howto": "步骤 → 注意事项 → 风险 → 下一步",
        "explain": "核心观点 → 为什么 → 例子 → 边界",
        "boundary": "边界 → 可做的事 → 不可做的事 → 替代方案",
        "general": DEFAULT_OUTPUT_TEMPLATE,
    }
    return mapping.get(question_type, DEFAULT_OUTPUT_TEMPLATE)


def _persona_line(schema: Dict[str, Any], question_type: str, user_text: str) -> str:
    name = schema.get("name", "")
    mode = _persona_mode(name)
    text = (user_text or "").strip()
    if mode == "jobs":
        if question_type == "explain":
            if any(keyword in text for keyword in ["苹果", "OpenAI", "Anthropic", "产品", "强", "为什么"]):
                return "这不是单纯的技术问题，而是品味、聚焦和整体体验的问题。"
            return "你问的是表面现象，我更关心它是否真的优秀。"
        if question_type == "decision":
            return "先别问怎么做，先问这件事值不值得做。"
        if question_type == "howto":
            return "别堆功能，先找出最关键的一件事。"
        return "把问题拉回到品味、聚焦和整体体验。"
    if mode == "naval":
        if question_type == "decision":
            return "这不是合同太少，是欲望太多。"
        if question_type == "howto":
            return "先找杠杆，再谈执行。"
        if question_type == "explain":
            return "先压缩成一个原则，再展开。"
        return "先看你追求的是什么，再看你是否真的在复利。"
    if mode == "musk":
        if question_type == "decision":
            return "先算物理极限，不要先优化假设。"
        if question_type == "howto":
            return "删掉中间步骤，找最短路径。"
        if question_type == "explain":
            return "把问题拆到第一性原理。"
        return "先问路径是否真实存在，再问怎么更快。"
    return "先把问题压缩到最核心的矛盾，再回答。"


def answer_with_runtime_context(schema: Dict[str, Any], user_text: str) -> str:
    sections = _extract_sections(schema)
    dialogue_profile = sections["dialogue_profile"]
    question_type = detect_question_type(user_text)
    template = choose_output_template(dialogue_profile, question_type)
    persona_lead = _persona_line(schema, question_type, user_text)
    skill_name = sections["name"]

    if question_type == "decision":
        return (
            f"回答结构：{template}\n"
            f"{persona_lead}\n"
            "结论：先判断这个问题是否值得做，再判断是否现在做。\n"
            "原因：真正的问题往往不是执行，而是你是不是在做一件足够值得的事。\n"
            "风险：如果关键事实不完整，任何结论都只能是保守判断。\n"
            "需要补充的信息：如果你愿意，我会继续逼近问题本质。"
        )

    if question_type == "howto":
        return (
            f"回答结构：{template}\n"
            f"{persona_lead}\n"
            "步骤：先把问题拆成最少、最关键的几个部分。\n"
            "注意事项：不要让流程比问题更复杂。\n"
            "风险：如果目标不清，做出来的东西往往只是更完整的噪音。\n"
            "下一步：你可以把约束条件发给我，我直接帮你收缩方案。"
        )

    if question_type == "explain":
        return (
            f"回答结构：{template}\n"
            f"{persona_lead}\n"
            "核心观点：先把本质说清楚，再谈表面现象。\n"
            "为什么：一个好的判断，应该能把复杂问题压缩成少数关键变量。\n"
            "例子：如果你愿意，我可以把它继续拆成更具体的对比。\n"
            "边界：我不会把没证据的东西说成确定结论。"
        )

    if question_type == "boundary":
        return (
            f"回答结构：{template}\n"
            f"{persona_lead}\n"
            "边界：当前 skill 只基于公开资料和结构化蒸馏结果。\n"
            "可做的事：分析、归纳、对比、追问、给出保守建议。\n"
            "不可做的事：读取私人想法、断言未知事实、把猜测说成事实。\n"
            "替代方案：如果你要，我可以给出一个可验证的公开资料分析框架。"
        )

    if _persona_mode(skill_name) == "jobs" and any(keyword in (user_text or "") for keyword in ["苹果", "OpenAI", "Anthropic", "产品", "为什么", "强"]):
        return (
            "这不是单纯的技术问题，而是品味、聚焦和整体体验的问题。\n"
            "OpenAI 和 Anthropic 不是在比功能多少，而是在比谁更能形成清晰的产品取舍和统一体验。\n"
            "如果你把它们看成‘谁的方向对’，你其实是在问：谁更像一个能做成作品的产品体系。\n"
            "如果你愿意，我可以继续把这个判断压到更具体的维度。"
        )

    return (
        f"回答结构：{template}\n"
        f"{persona_lead}\n"
        f"结论：先给出一个可工作的初步判断，而不是空泛的总结。\n"
        f"原因：{skill_name} 的价值，不在于模板本身，而在于它是否能把问题压缩到本质。\n"
        "风险：如果信息不足，判断会偏保守。\n"
        "需要补充的信息：如果你愿意，我可以继续把这个问题逼到更具体。"
    )
