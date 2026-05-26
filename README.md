

# 盘古.skill

<p align="center">
  <img src="assets/hero.gif" alt="pangu-skill Hero Animation" />
  <br/>
  <sub>动画由 <a href="https://github.com/alchaincyf/huashu-design">huashu-design</a> skill 制作</sub>
</p>  

> *「你想构建的下一个协议，何必是同事、人类」*

[License: MIT](LICENSE)
[Agent Skills](https://agentskills.io)
[skills.sh](https://skills.sh)
[Multi-Runtime](#安装)

  


**盘古不是只处理人物，而是把人物协议、领域协议、判断结构一起开成可调用的工具。**

基于开放的 [Agent Skills 协议](https://agentskills.io)，可在 Claude Code、Codex、Cursor、OpenClaw、Hermes Agent、CodeBuddy、Workbuddy、Gemini CLI、OpenCode 等 50+ 兼容 runtime 中运行。

  


[同事.skill](https://github.com/titanwings/colleague-skill) 证明了“把一个人做成可调用对象”是可行的。  

[女娲.skill](https://github.com/longjingcha/nuwa-skill) 证明了“女娲不复制人。它提取认知操作系统”
盘古要做的更进一步：它不只处理某个人，也能处理一个专业领域的知识协议、路径与规则。  

只需输入一个名字、一个领域，或者一个模糊目标，盘古就会自动完成生成流程，并在必要时触发开天能力。

[看效果](#效果示例) · [安装](#安装) · [盘古提供什么](#盘古提供什么) · [工作原理](#工作原理) · [不想自己构建？试试 Bloome](#不想自己构建试试-bloome)

  


**其他语言 / Other Languages:**

[English](README_EN.md)

  


[Star History Chart](https://star-history.com/#longjingcha/pangu-skill&Date)



---

## 效果示例

```
用户      ❯ 用张小龙的视角帮我想想：我的 App 想加一个‘签到’功能，该不该做？

张小龙     ❯ 如果你的 App 不是高频核心场景，签到 功能大概率不该做。
这个“签到”到底是在帮用户完成什么任务？

如果答案只是：

提升活跃
做留存数据
给运营一个抓手
让产品看起来“有互动”
那它通常不是用户需求，而是团队需求。

```

再来一个专业领域的例子：

```
用户      ❯ 我想系统学“增长”，但市面内容太碎了，怎么入门？

盘古      ❯ 先别背术语。先把增长拆成四个判断问题：
            1. 你到底在优化什么指标？
            2. 哪个环节是最强杠杆？
            3. 哪些增长动作短期有效、长期反噬？
            4. 什么看起来像增长，其实只是噪音？
            
            你不是缺内容，你缺的是一张增长知识地图。
```

这不是角色扮演。乔布斯用的是「聚焦即说不」和「端到端控制」模型，Naval用的是「欲望即合同」，马斯克用的是「渐近极限法」。**它们不是在复读名人语录，而是在用稳定模型帮你分析。**

---

## 安装

盘古基于开放的 [Agent Skills](https://agentskills.io) 协议，可在任何 skills-compatible 的 AI agent runtime 中运行。

### 方式一：一行命令（推荐，跨 runtime）

打开你正在用的 agent（Claude Code、Codex、Cursor、OpenClaw、Hermes、CodeBuddy、Workbuddy、Gemini CLI、OpenCode 等），告诉它：

```
帮我安装这个 skill：https://github.com/longjingcha/pangu-skill
```

或者用通用 CLI 安装器（[vercel-labs/skills](https://github.com/vercel-labs/skills)，支持 55+ runtime）：

```bash
npx skills add longjingcha/pangu-skill
```

它会自动识别你当前的 runtime 并把 skill 放到正确目录。需要指定时加 `-a claude-code` / `-a codex` / `-a cursor` / `-a openclaw` 等参数。

### 方式二：手动安装

展开查看各 runtime 的 skills 目录


| Runtime      | 安装路径                                        |
| ------------ | ------------------------------------------- |
| Claude Code  | `~/.claude/skills/pangu-skill/`             |
| Codex CLI    | `~/.codex/skills/pangu-skill/`              |
| Cursor       | `~/.cursor/skills/pangu-skill/`             |
| OpenClaw     | `~/.openclaw/workspace/skills/pangu-skill/` |
| Hermes Agent | 跑 `tools/install_hermes_skill.py`           |
| 其他 runtime   | clone 到对应 runtime 的 `skills/` 目录            |


```bash
git clone https://github.com/longjingcha/pangu-skill <上面对应的路径>
```



---

### 使用

装好后，告诉 agent：

```
> 构建一个保罗·格雷厄姆协议
> 造一个张小龙的视角Skill
> 帮我做一个段永平的Skill
```

造完之后直接调用：

```
> 用芒格的视角帮我分析这个投资决策
> 用张小龙的视角帮我想想：我的 App 想加一个‘签到’功能，该不该做
```

再来一个专业领域的例子：

```
用户      ❯ 我想系统学习「增长」这门知识，但网上内容太散了

盘古      ❯ 先别急着学。你现在缺的不是内容，是一张增长知识地图。
          我会先把增长拆成 4 层：
          1. 目标函数：增长到底是在优化什么
          2. 系统杠杆：拉新、激活、留存、传播、变现各自怎么起作用
          3. 约束边界：哪些增长手段短期有效、长期会反噬
          4. 反例清单：什么看起来像增长，实际上只是噪音

          你要的不是一堆技巧，而是一套可迁移的判断框架。
```

---

## 盘古到底在做什么

盘古不只是处理人物，而是在抽取“可迁移的判断结构”和“可执行的知识协议”。

它提取六层：


| 层次        | 说明               |
| --------- | ---------------- |
| **怎么说话**  | 表达规则——语气、节奏、用词偏好 |
| **怎么想**   | 模型——稳定认知结构       |
| **怎么判断**  | 规则——可执行判断动作      |
| **怎么拆问题** | 问题分层、边界识别、重写能力   |
| **什么不做**  | 反模式、价值观底线        |
| **知道局限**  | 诚实边界             |


工作习惯可以靠流程文档传递，但让芒格和马斯克面对同一个问题做出不同判断的，是认知框架。盘古提取的是可迁移的认知结构，而不是通用的流程模板；如果原问题本身就是错的，它还会先把问题改对。

### 诚实边界

每个Skill都明确标注做不到什么：

- 抽取不了直觉——框架能提取，灵感不能
- 捕捉不了突变——截止到调研时间的快照
- 公开表达 ≠ 真实想法——只能基于公开信息

**一个不告诉你局限在哪的Skill，不值得信任。一个不敢重写问题的Skill，也不够强。**

---

## 已构建人物

盘古已构建了13位人物 + 1个主题协议。每个都是独立的、可直接安装使用的Skill，全部基于 Agent Skills 协议，可在 Claude Code / Codex / Cursor / OpenClaw / Hermes 等 runtime 通用。

但盘古真正提供的，不只是列表，而是一套可以持续演化的认知生产线：输入问题、重写问题、提炼结构、验证边界、再输出判断。

### 人物Skill


| 人物                 | 领域            | 独立仓库                                                                  | 一键安装（跨 runtime）                                |
| ------------------ | ------------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| 🔥 **Paul Graham** | 创业/写作/产品/人生哲学 | [paul-graham-skill](https://github.com/longjingcha/paul-graham-skill) | `npx skills add longjingcha/paul-graham-skill` |


### 主题Skill


| 主题      | 领域            | 独立仓库                                                            | 一键安装（跨 runtime）                             |
| ------- | ------------- | --------------------------------------------------------------- | ------------------------------------------- |
| **X导师** | X/Twitter运营全栈 | [x-mentor-skill](https://github.com/longjingcha/x-mentor-skill) | `npx skills add longjingcha/x-mentor-skill` |


人物协议抽取一个人的思维方式；主题协议抽取一个领域的方法论。每个仓库都包含完整的调研数据和效果示例对话。

想处理不在列表里的人或主题？安装盘古，说「构建一个XXX协议」就行。

---

## 盘古提供什么

盘古提供的不是单次回答，而是一整套可复用的协议生产链：

### 1. 人物协议

面向具体人物，抽取：

- 心智模型
- 决策启发式
- 表达规则
- 价值观与反模式
- 诚实边界

### 2. 领域协议

面向主题、方法论、学科，抽取：

- 领域边界
- 核心结构
- 判断标准
- 进入路径
- 失效条件
- 流派分歧
- 可执行动作

### 3. 开天能力

当问题本身有伪前提、边界不清或只是表面症状时，先重写问题，再决定是否继续进入人物协议或领域协议。

### 4. 诊断与审计工具

- `pangu_protocol_diagnoser`：发现协议缺口、判断是否要开天
- `pangu_protocol_auditor`：检查交付质量，避免编造式交付
- `pangu_subtitle_fetcher` / `pangu_transcript_cleaner`：提供原始语料链路

### 5. 完整输入链路

从字幕、转写、来源规范，到提炼框架、模板、审计，盘古不是一个单点 Skill，而是一套能持续生产协议的系统。

---

## 工作原理

输入一个名字后，盘古做四件事，但这四件事和 `nuwa-skill` 不是同一套逻辑。

**1. 先判断要不要开天**——如果用户的问题本身有伪前提、边界不清、目标和手段混在一起，先重写问题，再决定是否进入协议构建。

**2. 六路并行采集**——著作、播客/访谈、社交媒体、批评者视角、决策记录、人生时间线，6个Agent同时跑，各自存档。

**3. 双协议提炼**——不只提炼人物，也提炼领域。人物侧抽取心智模型、决策启发式、表达规则、价值观与边界；领域侧抽取边界、结构、判断标准、路径、失效条件与流派分歧。

**4. 质量验证与审计**——人物协议要看是否像且不乱猜，领域协议要看是否能落到判断与行动，开天判断要看是否真的把错题重写对了。最后再用审计工具检查能否交付。

完整方法论在 `references/pangu-extraction-framework.md`。

---

## 仓库结构

```
pangu-skill/
├── SKILL.md                      # 盘古本体
├── references/
│   ├── pangu-extraction-framework.md   # 提炼方法论（想深入了解看这个）
│   └── pangu-skill-template.md         # 生成Skill的模板
└── examples/                          # 正在构建
    ├── steve-jobs-perspective/        # ⭐ 乔布斯（含实战对话记录）
    ├── paul-graham-perspective/       # Paul Graham
```

调研过程全透明。每个example都包含完整的调研文件，你可以看到信息怎么被收集、筛选、变成心智模型。乔布斯的示例还附带了一段完整的实战对话记录（聊AI硬件、OpenAI vs Anthropic、Apple破局），展示Skill在多轮深度对话中的表现。

---

## 背后的故事

盘古不是在重复女娲，而是在把“人”和“问题”都推进到可调用协议的层面。

[同事.skill](https://github.com/titanwings/colleague-skill) 最近在GitHub爆火——把离职同事构建成 AI Skill，几天破5000星。它证明了一件事：把一个人做成可调用对象是完全可行的。

女娲的贡献，是把人物思维框架做成可用镜子；盘古的推进，是在此基础上把人物、领域和问题本身一起协议化。

盘古把两件事放在一起：既能构建人物协议，也能构建领域协议，还能在问题本身不对的时候先开天。前者给你认知风格，后者给你判断协议，而开天能力让系统先判断题对不对。

我之前就一直在做类似的事，但构建的不只是同事，而是芒格、费曼、Naval、马斯克、塔勒布这些协议。今天把方法论开源了。

### 和 `nuwa-skill` 的区别


| 维度   | `nuwa-skill`        | `pangu-skill`            |
| ---- | ------------------- | ------------------------ |
| 核心目标 | 把一个人蒸馏成人物 Skill     | 把人物、领域、问题一起协议化           |
| 主轴   | 人物思维框架与角色扮演         | 人物协议 + 领域协议 + 开天分流       |
| 产物结构 | 人物 Skill / 主题 Skill | 人物协议 / 领域协议              |
| 关键能力 | 心智模型、决策启发式、表达DNA    | 人物协议、领域协议、开天能力、协议审计      |
| 流程风格 | 调研 → 提炼 → 构建 → 验证   | 分流 → 开天 → 提炼 → 模板 → 审计   |
| 资源组织 | 调研文件 + skill模板      | 输入层规范 + 提炼规范 + 模板 + 审计链路 |


### 盘古为什么更适合做“协议工坊”

- 不是只回答“像谁”，而是先判断“问题对不对”
- 不是只做人，而是把领域方法论也做成可调用对象
- 不是只做角色扮演，而是把问题重写、协议提炼、质量审计拆成独立步骤
- 不是只有一个模板，而是人物协议和领域协议双模板并行

[女娲.skill](https://github.com/longjingcha/nuwa-skill) 负责提炼认知框架。

盘古负责把认知框架、领域判断和问题重构一起做成协议。

**盘古（Pangu）**，中国神话里开天辟地的巨人。这里的泥土是公开信息，造出来的不是人，是一套能不断开天的协议系统。

---

## 关于作者

**查老师并不渣** — 一人公司OPC（独立开发者） | 副业赚钱 | AI自动化编程网站 [www.lscript.cn](http://www.lscript.cn)


|        |                                                                             |
| ------ | --------------------------------------------------------------------------- |
| 🌐 官网  | [www.lscript.cn](http://www.lscript.cn)                                     |
| 📺 B站  | [查老师并不渣](https://space.bilibili.com/642180359?spm_id_from=333.337.0.0)      |
| 📕 小红书 | [查老师并不渣](https://www.xiaohongshu.com/user/profile/67698a55000000001802adbc) |
| 💬 公众号 | 微信搜「查哥聊AI」                                                                  |


## 许可证

MIT — 随便用，随便改，随便造。

---



**女娲.skill**  女娲不复制人。它提取认知操作系统。  

**盘古** 抽取了人怎么想。  
  

*你想构建的下一个协议，何必是人类。*

  


MIT License © [查老师并不渣](https://github.com/longjingcha)



---

