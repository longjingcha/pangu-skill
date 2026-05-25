# pangu-skill

> 把公开资料蒸馏成一个可对话、可验证、可迭代的 `skill`。

`pangu-skill` 不是语气模仿器，
而是一个 **公开人物认知框架蒸馏器 + 对话验证器**。

它把一个人的：

- 认知框架
- 判断方式
- 追问方式
- 重构问题的方式
- 边界意识

蒸馏成一个可以反复对话、反复修正、逐步逼近的 skill。

---

## 一句话看懂它

**不是复读语录，而是提取“怎么想”。**

你输入一个名字，`pangu-skill` 帮你把公开资料整理成一个能运行的 skill；
你再用这个 skill 去对话，检验它是否真的像这个人。

---

## 它能做什么

- 蒸馏乔布斯 / Naval / 马斯克 / 其他人物的公开思维模式
- 生成可运行的 `skill_schema.yaml`
- 导出 `SKILL.md` 和 `prompt_pack.md`
- 用 skill 对话，验证它是否真的像
- 根据对话结果继续修正蒸馏

---

## 核心闭环

```text
公开资料
→ 蒸馏成 skill
→ 用 skill 对话
→ 发现偏差
→ 修正蒸馏
→ 再对话
```

这就是 `pangu-skill` 的产品核心。

---

## 为什么它有用

因为真正“像”的回答，不在句式，
而在它是否真的进入了那个人的思考方式：

- 这是不是一个值得做的问题？
- 这是不是一个品味问题？
- 这是不是一个取舍问题？
- 这是不是一个杠杆问题？
- 这是不是一个最短路径问题？

`pangu-skill` 蒸馏的就是这些 **思考动作**。

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

## 快速开始

### 1. 自动蒸馏

```bash
python -m pangu_skill --say "帮我蒸馏一个乔布斯 skill" --auto
```

### 2. 手动蒸馏

```bash
python -m pangu_skill distill --query "乔布斯" --input-dir research/merged
```

### 3. 进入对话

```bash
python -m pangu_skill chat --schema generated/distilled_skill.yaml
```

### 4. 质量检查

```bash
python -m pangu_skill quality --schema generated/distilled_skill.yaml
```

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
├── scripts/
├── src/pangu_skill/
├── examples/
├── research/
└── generated/
```

---

## 对话风格目标

你希望它回答得像这样：

- 先质疑问题前提
- 再把问题重构成更本质的版本
- 再给出清晰判断
- 最后用这个人物的方式压缩成一句锋利的话

不是“回答像谁”，
而是“想问题像谁”。

---

## 乔布斯示例目标

例如：

> OpenAI 和 Anthropic 谁的方向是对的？

理想回答不是中性分析，而是：

- 质疑“方向对”这个前提
- 把问题改写成“品味与聚焦的竞赛”
- 用“作品”而不是“公司”来判断
- 给出锋利但有层次的结论

这就是 `pangu-skill` 想逼近的效果。

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
