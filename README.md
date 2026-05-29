<div align="center">

# 盘古.skill

<p align="center">
  <img src="assets/hero.gif" alt="pangu-skill Hero Animation" />
  <br/>
  <sub>动画由本地 render_hero制作</sub>
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


</div>

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
> 构建一个特朗普的协议
> 造一个张小龙的视角Skill
> 帮我做一个罗永浩的Skill
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

盘古已构建了 18 位人物 + 1 个主题协议。每个都是独立的、可直接安装使用的 Skill，全部基于 Agent Skills 协议，可在 Claude Code / Codex / Cursor / OpenClaw / Hermes 等 runtime 通用。

但盘古真正提供的，不只是列表，而是一套可以持续演化的认知生产线：输入问题、重写问题、提炼结构、验证边界、再输出判断。

### 科技与半导体领域（8位）

| 人物 | 领域 | 独立仓库 | 一键安装（跨 runtime） |
| --- | --- | --- | --- |
| **🔥 埃隆·马斯克（Elon Musk）** | 特斯拉 / SpaceX / 工程边界 / 第一性原理 | [elon-musk-skill](https://github.com/longjingcha/elon-musk-skill) | `npx skills add longjingcha/elon-musk-skill` |
| **🔥 蒂姆·库克（Tim Cook）** | 苹果 / 供应链 / 运营纪律 / 长期稳健增长 | [tim-cook-skill](https://github.com/longjingcha/tim-cook-skill) | `npx skills add longjingcha/tim-cook-skill` |
| **黄仁勋（Jensen Huang）** | 英伟达 / 算力基础设施 / 平台战略 | [jensen-huang-skill](https://github.com/longjingcha/jensen-huang-skill) | `npx skills add longjingcha/jensen-huang-skill` |
| **克里斯蒂亚诺·阿蒙（Cristiano Amon）** | 高通 / 通信平台 / 芯片生态 / 终端连接 | [cristiano-amon-skill](https://github.com/longjingcha/cristiano-amon-skill) | `npx skills add longjingcha/cristiano-amon-skill` |
| **桑杰·梅赫罗特拉（Sanjay Mehrotra）** | 美光科技 / 存储基础设施 / 规模化制造 | [sanjay-mehrotra-skill](https://github.com/longjingcha/sanjay-mehrotra-skill) | `npx skills add longjingcha/sanjay-mehrotra-skill` |
| **雅各布·泰森（Jacob Thaysen）** | 因美纳 / 基因测序 / 科学工具平台 | [jacob-thaysen-skill](https://github.com/longjingcha/jacob-thaysen-skill) | `npx skills add longjingcha/jacob-thaysen-skill` |
| **吉姆·安德森（Jim Anderson）** | Coherent / 光学与光子技术 / 高端光电基础设施 | [jim-anderson-skill](https://github.com/longjingcha/jim-anderson-skill) | `npx skills add longjingcha/jim-anderson-skill` |
| **迪娜·鲍威尔·麦考密克（Dina Powell McCormick）** | Meta / 全球事务 / 政商桥梁 | [dina-powell-mccormick-skill](https://github.com/longjingcha/dina-powell-mccormick-skill) | `npx skills add longjingcha/dina-powell-mccormick-skill` |

### 金融与支付网络（6位）

| 人物 | 领域 | 独立仓库 | 一键安装（跨 runtime） |
| --- | --- | --- | --- |
| **🔥 拉里·芬克（Larry Fink）** | BlackRock / 长期资本配置 / 受托责任 | [larry-fink-skill](https://github.com/longjingcha/larry-fink-skill) | `npx skills add longjingcha/larry-fink-skill` |
| **苏世民（Stephen Schwarzman）** | Blackstone / 另类资产 / 平台化扩张 | [stephen-schwarzman-skill](https://github.com/longjingcha/stephen-schwarzman-skill) | `npx skills add longjingcha/stephen-schwarzman-skill` |
| **苏德巍（David Solomon）** | Goldman Sachs / 市场周期 / 机构客户 | [david-solomon-skill](https://github.com/longjingcha/david-solomon-skill) | `npx skills add longjingcha/david-solomon-skill` |
| **简·弗雷泽（Jane Fraser）** | Citigroup / 全球网络 / 组织重构 | [jane-fraser-skill](https://github.com/longjingcha/jane-fraser-skill) | `npx skills add longjingcha/jane-fraser-skill` |
| **迈克尔·米巴赫（Michael Miebach）** | Mastercard / 支付平台 / 信任安全 | [michael-miebach-skill](https://github.com/longjingcha/michael-miebach-skill) | `npx skills add longjingcha/michael-miebach-skill` |
| **瑞安·麦克纳尼（Ryan McInerney）** | Visa / 全球支付网络 / 跨境交易 | [ryan-mcinerney-skill](https://github.com/longjingcha/ryan-mcinerney-skill) | `npx skills add longjingcha/ryan-mcinerney-skill` |

### 工业航空与制造业（2位）

| 人物 | 领域 | 独立仓库 | 一键安装（跨 runtime） |
| --- | --- | --- | --- |
| **🔥 凯利·奥特伯格（Kelly Ortberg）** | Boeing / 航空制造 / 质量治理 / 供应链恢复 | [kelly-ortberg-skill](https://github.com/longjingcha/kelly-ortberg-skill) | `npx skills add longjingcha/kelly-ortberg-skill` |
| **拉里·卡尔普（Larry Culp）** | GE Aerospace / 运营修复 / 现金流纪律 | [larry-culp-skill](https://github.com/longjingcha/larry-culp-skill) | `npx skills add longjingcha/larry-culp-skill` |

### 传统农业领域（1位）

| 人物 | 领域 | 独立仓库 | 一键安装（跨 runtime） |
| --- | --- | --- | --- |
| **🔥 布莱恩·赛克斯（Brian Sikes）** | Cargill / 供应链韧性 / 粮食安全 / 全球农业基础设施 | [brian-sikes-skill](https://github.com/longjingcha/brian-sikes-skill) | `npx skills add longjingcha/brian-sikes-skill` |

### 政商与交易叙事（1位）

| 人物 | 领域 | 独立仓库 | 一键安装（跨 runtime） |
| --- | --- | --- | --- |
| **🔥 唐纳德·特朗普（Donald Trump）** | 注意力 / 交易叙事 / 冲突管理 / 联盟重组 | [donald-trump-skill](https://github.com/longjingcha/donald-trump-skill) | `npx skills add longjingcha/donald-trump-skill` |

### 主题Skill


| 主题      | 领域            | 独立仓库                                                            | 一键安装（跨 runtime）                             |
| ------- | ------------- | --------------------------------------------------------------- | ------------------------------------------- |
| **小红书协议** | 小红书运营全栈 | [xiaohongshu-ops-skill](https://github.com/longjingcha/xiaohongshu-ops-skill) | `npx skills add longjingcha/xiaohongshu-ops-skill` |


人物协议抽取一个人的思维方式；主题协议抽取一个领域的方法论。每个仓库都包含完整的调研数据和效果示例对话。

想处理不在列表里的人或主题？安装盘古，说「构建一个 XXX 协议」就行。

你也可以直接安装现成的人物协议，比如张雪峰：`npx skills add longjingcha/zhangxuefeng-skill`

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
├── README.md                     # 中文介绍与安装说明
├── README_EN.md                  # English version
├── references/                   # 提炼方法论与模板
│   ├── pangu-extraction-framework.md
│   └── pangu-skill-template.md
└── examples/                     # 已构建/正在构建的示例协议
    ├── tech-and-semi/            # 科技与半导体人物协议
    ├── finance-and-payments/     # 金融与支付网络协议
    ├── industrial-and-manufacturing/ # 工业、航空与制造协议
    ├── agriculture/              # 传统农业与供应链协议
    ├── politics-and-narrative/   # 政商与交易叙事协议
    └── topic-protocols/          # 主题协议
```


调研过程全透明。每个example都包含完整的调研文件，你可以看到信息怎么被收集、筛选、变成心智模型。乔布斯的示例还附带了一段完整的实战对话记录（聊AI硬件、OpenAI vs Anthropic、Apple破局），展示Skill在多轮深度对话中的表现。

---

## 背后的故事

盘古不是在重复女娲，而是在把“人”和“问题”都推进到可调用协议的层面。

[同事.skill](https://github.com/titanwings/colleague-skill) 最近在GitHub爆火——把离职同事构建成 AI Skill，几天破5000星。它证明了一件事：把一个人做成可调用对象是完全可行的。

[女娲.skill](https://github.com/alchaincyf/nuwa-skill)的贡献，是把人物思维框架做成可用镜子；

[盘古.skill](https://github.com/longjingcha/pangu-skill)的推进，是在此基础上把人物、领域和问题本身一起协议化。

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

[盘古.skill](https://github.com/longjingcha/pangu-skill)负责把认知框架、领域判断和问题重构一起做成协议。

**盘古（Pangu）**，中国神话里开天辟地的巨人。这里的泥土是公开信息，造出来的不是人，是一套能不断开天的协议系统。

---

## 统一词表 / Glossary

为了和 `nuwa-skill` 保持术语区分，同时让盘古的表达更稳定，仓库里统一采用下面这组词：

| 旧说法 | 盘古推荐说法 | 用途 |
|------|-------------|------|
| 蒸馏 | 协议生产 / 协议提炼 | 描述整套构建流程 |
| 心智模型 | 模型 / 认知结构 | 描述人的稳定思考方式 |
| 决策启发式 | 规则 | 描述可执行的判断动作 |
| 表达DNA | 表达规则 | 描述语气、句式、节奏与口癖 |
| 造人 / 造Skill | 构建协议 / 构建 Skill | 描述最终产物生成 |
| 角色扮演 | 协议输出 / 认知输出 | 避免把盘古写成纯模仿器 |
| 调研 | 资料采集 / 多源采集 | 描述原始信息输入 |
| 提炼 | 结构化提炼 | 描述从材料到协议的转化 |
| 质量验证 | 审计 / 验收 | 描述交付前检查 |
| 开天 | 问题重写 / 问题校正 | 描述先判断题是否成立 |

### 调研来源

本仓库的协议生产主要依赖 6 个调研文件，均位于 `references/research/`：

- `pangu-writings.md`：著作、长文与系统表达
- `pangu-dialogues.md`：深度采访、对谈与即兴回答
- `pangu-expression.md`：表达风格、句式与口癖
- `pangu-commentary.md`：他者视角、批评与争议
- `pangu-decisions.md`：重大决策、转折与行为分析
- `pangu-timeline.md`：完整人生时间线与最新动态

这 6 个文件不是为了“蒸馏一个人”的固定流程，而是为了给盘古的协议工坊提供稳定输入：人物协议看模型、规则、表达与边界；领域协议看结构、判断、路径与失效条件；开天能力则判断问题本身是否需要先重写。

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

