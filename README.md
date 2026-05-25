# pangu-skill

[![hero](assets/hero.gif)](assets/hero.gif)

> 你想蒸馏的下一个人，何必只是同事。

`pangu-skill` 把公开资料蒸馏成可对话、可验证、可迭代的 `skill`。

它不是语气模仿器，
而是一个 **公开人物认知框架蒸馏器 + 对话验证器**。

它提取的不是“他说了什么”，
而是：

- 怎么想
- 怎么判断
- 怎么追问
- 怎么重构问题
- 什么不做
- 边界在哪

---

## 它到底在做什么

输入一个名字，`pangu-skill` 帮你把公开资料整理成一个能运行的 skill；
你再用这个 skill 去对话，看看它到底像不像。

不是复读语录，
而是提取认知操作系统。

---

## 安装

`pangu-skill` 基于开放的 Agent Skills 协议，可在 skills-compatible 的 AI agent runtime 中运行。

### 一行命令（推荐）

告诉你的 agent：

> 帮我安装这个 skill：https://github.com/your-org/pangu-skill

或者直接下载仓库后安装：

```bash
git clone https://github.com/your-org/pangu-skill
cd pangu-skill
python scripts/install_skill.py --target cursor
```

### 通用安装器

```bash
npx skills add your-org/pangu-skill
```

### 手动安装

```bash
python scripts/install_skill.py --list-targets
python scripts/install_skill.py --target cursor --source .
```

### 作为参考资料使用

即使 runtime 不支持自动加载，你也可以直接把 `SKILL.md` 粘贴进对话。

---

## 效果示例

你希望它回答得像这样：

- 先质疑问题前提
- 再把问题重构成更本质的版本
- 再给出清晰判断
- 最后压缩成一句锋利的话

### 乔布斯示例

> OpenAI 和 Anthropic 谁的方向是对的？

理想回答不是中性分析，而是：

- 质疑“方向对”这个前提
- 把问题改写成“品味与聚焦的竞赛”
- 用“作品”而不是“公司”来判断
- 给出锋利但有层次的结论

---

## 工作原理

输入一个名字后，`pangu-skill` 做四件事：

1. **六路并行采集**
   - YouTube / B站 / 抖音字幕
   - 维基百科
   - 公开网页
   - 公开访谈稿
   - 批评者视角
   - 时间线与决策记录

2. **三重验证提炼**
   - 一个观点要跨多个来源反复出现
   - 能推断新问题下的立场
   - 不是所有聪明人都会有的独特判断

3. **构建 Skill**
   - 3-7 个心智模型
   - 5-10 条决策启发式
   - 表达 DNA
   - 价值观与反模式
   - 诚实边界

4. **质量验证**
   - 用 3 个公开回答过的问题测试一致性
   - 再用 1 个没讨论过的问题测试不确定性
   - 不像就回去修正蒸馏

完整方法论在 `references/extraction-framework.md`。

---

## 快速开始

### 自动蒸馏

```bash
python -m pangu_skill --say "帮我蒸馏一个乔布斯 skill" --auto
```

### 手动蒸馏

```bash
python -m pangu_skill distill --query "乔布斯" --input-dir research/merged
```

### 进入对话

```bash
python -m pangu_skill chat --schema generated/distilled_skill.yaml
```

### 质量检查

```bash
python -m pangu_skill quality --schema generated/distilled_skill.yaml
```

---

## 最小但足够强

当前版本只保留最关键的能力：

- `signature_questions`
- `signature_reframes`
- `signature_responses`
- `decision_style`
- 角色风格触发器
- 少量高质量样例
- 对话反哺修正

先跑通，再变强。

---

## 研究资料来源

### 视频平台
- YouTube
- B站
- 抖音

用字幕采集：

```bash
bash scripts/download_subtitles.sh
```

### 文本资料
- 维基百科
- 公开网页
- 公开访谈稿

维基百科抓取：

```bash
python scripts/fetch_wiki.py --query "Steve Jobs" --lang en
```

合并研究材料：

```bash
python scripts/merge_research.py
```

---

## 目录结构

```text
pangu-skill/
├── assets/
│   └── hero.gif
├── scripts/
├── src/pangu_skill/
├── examples/
├── research/
└── generated/
```

---

## 诚实边界

- 只能蒸馏公开资料
- 不能读取私人想法
- 不能把猜测说成事实
- 不能把风格模仿当成真实还原

它的任务是逼近，不是伪装。

---

## 和 nuwa-skill 的不同

`nuwa-skill` 很强的地方在于：

- 它把“怎么想”讲清楚了
- 它把“怎么验证”也讲清楚了
- 它让示例对话直接展示结果

`pangu-skill` 现在做的，也是这件事：

> 把公开资料蒸馏成思维框架，再用对话把它逼近到像。

---

## 一句话总结

`pangu-skill` 让你把一个人的公开思维框架蒸馏成 skill，
再用对话把它修正得越来越像。
