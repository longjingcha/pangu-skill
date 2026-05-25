# pangu-skill

![hero](assets/hero.gif)

盘古（Pangu）是一个开源的 AI 心智蒸馏平台。它把公开材料、对话、作品和行为中的思维模式，蒸馏成可执行、可验证、可演化的 `skill`。

## 安装

### 方式一：一行命令（推荐）

```bash
pip install -r requirements.txt
```

### 方式二：包入口运行

```bash
python -m pangu_skill --help
```

### 方式三：命令行直接使用

```bash
pangu-skill --help
```

## 使用

### 蒸馏

```bash
pangu-skill distill \
  --input examples/raw_material_1.txt examples/raw_material_2.txt \
  --schema-output generated/distilled_skill.yaml \
  --markdown-output generated/SKILL.md \
  --name "Generated Skill" \
  --skill-id "pangu.generated.001" \
  --config distill_config.yaml
```

### 验证

```bash
pangu-skill validate --schema examples/example_skill.yaml
```

### 导出

```bash
pangu-skill export --schema examples/example_skill.yaml --output generated/SKILL.md
```

### 手动安装

| Runtime | 安装路径 |
| --- | --- |
| Claude Code | `~/.claude/skills/pangu-skill/` |
| Codex CLI | `~/.codex/skills/pangu-skill/` |
| Cursor | `~/.cursor/skills/pangu-skill/` |
| OpenClaw | `~/.openclaw/workspace/skills/pangu-skill/` |
| Hermes Agent | 运行 `tools/install_hermes_skill.py` |
| 其他 runtime | 克隆到对应 runtime 的 `skills/` 目录 |

### 作为参考资料使用

即使 runtime 不支持自动加载，你也可以直接使用以下内容：

- `SKILL.md`
- `skill_schema.yaml`
- `RELEASE.md`

## 最简使用方式

> 给材料，说目标，蒸馏成 skill，然后直接调用。

### 标准口令

- `帮我蒸馏这个对象`
- `帮我生成一个适合 X 场景的 skill`
- `把这个 skill 导出成 SKILL.md`
- `用这个 skill 来处理下面这个问题`

## 核心能力

- 统一 skill schema
- 配置化蒸馏器
- 多材料对比
- 冲突检测
- 结构化 evidence
- Markdown 导出
- CLI 包入口
- 项目可打包发布

## 蒸馏器 v3

- 可配置的分词、停用词和阈值
- 多材料对比与高频主题提取
- 冲突检测
- 结构化 evidence 输出
- 版本化输出

### Validation 新增

- `validation.evidence`
- `validation.conflicts`

## 与 nuwa-skill 的关系

- `nuwa-skill` 更偏向“蒸馏一个对象”
- `pangu-skill` 更偏向“蒸馏思维方法论，并让它持续进化”

## 口号

- 蒸馏思维，生成你的能力系统
- 让认知成为可运行的结构
- 从混沌输入，到秩序输出
