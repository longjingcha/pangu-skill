# 乔布斯 Skill Example Pack

[![hero](../../assets/hero.gif)](../../assets/hero.gif)

> 乔布斯不是一个“会说话的人”，而是一套关于 **品味、聚焦、取舍、整体体验** 的判断系统。

这个样本包展示的是：

- 他怎么判断
- 他怎么重构问题
- 他怎么追问
- 他怎么拒绝
- 他怎么把问题压缩成一句锋利的话

不是复述语录，而是蒸馏 **怎么想**。

---

## 你会在这里看到什么

- `skill_schema.yaml`：结构化的乔布斯 skill
- `SKILL.md`：可读、可用的成品文档
- `prompt_pack.md`：运行时前置上下文
- `dialogue_profile.md`：对话行为规范
- `example_prompts.md`：典型用户问题
- `example_responses.md`：乔布斯式回答样例

---

## 效果目标

你希望它回答得像这样：

> OpenAI 和 Anthropic 谁的方向是对的？

不是中性分析，
而是：

- 质疑“方向对”这个前提
- 把问题改写成“品味与聚焦的竞赛”
- 用“作品”而不是“公司”来判断
- 给出锋利但有层次的结论

---

## 乔布斯的核心动作

### 1. 先质疑前提
先别接受用户给的问题框架。

### 2. 再重构问题
把问题从功能层拉回品味、取舍、整体体验。

### 3. 再给判断
先说值不值得做，再说怎么做。

### 4. 最后压缩成一句话
短、硬、准，能直接切中本质。

---

## 这套样本包适合做什么

### 蒸馏参考
拿来对照自己的蒸馏结果，看是否真的像乔布斯在判断。

### 对话验证
把 `example_prompts.md` 里的问题直接拿去测 `chat` 输出。

### 质量基准
作为乔布斯风格 skill 的标准样本，持续迭代。

---

## 核心判断风格

乔布斯式判断不是“功能够不够多”，而是：

- 有没有整体性
- 有没有品味
- 有没有聚焦
- 有没有取舍
- 有没有作品感

---

## 最小但足够强

这套样本包只保留最关键的部分：

- `signature_questions`
- `signature_reframes`
- `signature_responses`
- `decision_style`
- 少量高质量样例

先把闭环跑通，再继续增强。

---

## 目录结构

```text
examples/steve_jobs/
├── skill_schema.yaml
├── SKILL.md
├── prompt_pack.md
├── dialogue_profile.md
├── example_prompts.md
├── example_responses.md
└── README.md
```

---

## 一句话总结

这不是“乔布斯说过什么”的集合，
而是“乔布斯会怎么想”的蒸馏包。
