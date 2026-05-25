# pangu-skill

盘古（Pangu）是一个开源的 AI 心智蒸馏平台，它通过多源资料采集、结构化提炼与可信度验证，把人物、组织或主题的公开知识转化为可执行、可更新、可导出的心智模型。

## 项目结构

```text
pangu-skill/
├── README.md
├── pyproject.toml
├── requirements.txt
├── SKILL.md
├── skill_schema.yaml
├── distill_config.yaml
├── examples/
│   ├── example_skill.yaml
│   ├── raw_material_1.txt
│   └── raw_material_2.txt
├── tests/
│   └── test_exporter.py
└── src/
    └── pangu_skill/
        ├── __init__.py
        ├── __main__.py
        ├── cli.py
        ├── distill_config.py
        └── exporter.py
```

## 产品定位

盘古不是简单的内容生成器，也不是单纯的人设模仿器。它的目标是把“思维方式”蒸馏成可调用、可验证、可演化的 `skill`，最终形成一套属于自己的认知操作系统。

## 设计目标

- 从公开材料、对话、作品和行为中蒸馏出稳定的思维模式
- 将蒸馏结果组织成统一的 `skill schema`
- 将结构化结果导出为可直接使用的 `SKILL.md`
- 通过验证、反馈与版本化机制持续演化 skill

## 安装与运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 包入口运行

```bash
python -m pangu_skill validate --schema examples/example_skill.yaml
python -m pangu_skill export --schema examples/example_skill.yaml --output generated/SKILL.md
```

### 通过项目命令运行

安装后可直接使用：

```bash
pangu-skill validate --schema examples/example_skill.yaml
pangu-skill export --schema examples/example_skill.yaml --output generated/SKILL.md
```

### 蒸馏原始材料

```bash
pangu-skill distill \
  --input examples/raw_material_1.txt examples/raw_material_2.txt \
  --schema-output generated/distilled_skill.yaml \
  --markdown-output generated/SKILL.md \
  --name "Generated Skill" \
  --skill-id "pangu.generated.001" \
  --config distill_config.yaml
```

## 蒸馏器 v3

当前蒸馏器已经具备：

- 可配置的分词、停用词和阈值
- 多材料对比与高频主题提取
- 冲突检测
- 结构化 evidence 输出
- 版本化输出

### Validation 结构新增

- `validation.evidence`：每个主题的支持材料、来源数和置信度
- `validation.conflicts`：主题冲突、冲突证据和建议解释方式

## 核心理念

### 1. 蒸馏，而不是抄写
盘古输出的不是原文摘要，而是：

- 核心认知
- 决策模式
- 价值偏好
- 风格特征
- 反模式
- 边界条件

### 2. 结构优先，而不是堆材料
盘古强调统一骨架，先有结构，再有表达。这样不同对象蒸馏出的结果才能比较、验证和演化。

### 3. 可验证，而不是只讲故事
一个 skill 如果不能验证，就只是包装。盘古会为每个 skill 提供一致性、区分度、预测力和边界验证。

### 4. 可演化，而不是一次性生成
skill 不是静态文档，而是持续成长的能力体。盘古支持版本管理、反馈迭代和重新蒸馏。

## 统一 Skill Schema v1

盘古建议所有 skill 统一采用以下结构：

```yaml
skill_id: ""
name: ""
summary: ""

source:
  sources: []
  coverage: "low"
  confidence: 0.0
  notes: ""

thinking_model:
  core_beliefs: []
  mental_models: []
  reasoning_style: []
  heuristics: []
  unknown_handling: []

decision_rules:
  priorities: []
  tradeoffs: []
  constraints: []
  escalation_logic: []

expression_dna:
  tone: []
  style_traits: []
  format_preferences: []
  language_patterns: []

anti_patterns: []

boundaries:
  scope: []
  limitations: []
  non_goals: []

validation:
  test_questions: []
  evaluation_metrics: []
  failure_modes: []
  evidence: []
  conflicts: []

versioning:
  version: "v1.0.0"
  status: "draft"
  changelog: []
  iteration_notes: []
```

## 蒸馏工作流 v1

1. 选择蒸馏对象
2. 收集多源材料
3. 提取认知模式
4. 归纳决策规则
5. 组织成统一 schema
6. 验证质量与边界
7. 生成 `SKILL.md`
8. 收集反馈并迭代版本

## 与 nuwa-skill 的关系

盘古可以参考 `nuwa-skill` 的结构思路，但目标更进一步：

- `nuwa-skill` 更偏向“蒸馏一个对象”
- `pangu-skill` 更偏向“蒸馏思维方法论，并让它持续进化”

## 项目下一步建议

- 定义完整的蒸馏工作流
- 定义 `SKILL.md` 输出模板
- 建立验证集与评分标准
- 增加版本管理与回归测试机制

## 口号

- 蒸馏思维，生成你的能力系统
- 让认知成为可运行的结构
- 从混沌输入，到秩序输出
