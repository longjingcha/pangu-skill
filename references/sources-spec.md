# `references/sources/` 资源组织规范

> 让原始材料、字幕、转写与元信息在盘古流程中可追溯、可复用、可校验。

---

## 1. 目标

`references/sources/` 只保存可追溯的原始材料与派生材料。它是盘古协议提炼的输入层，不承担解释任务。

**目标**
- 保留来源链路
- 区分原始材料与派生材料
- 为人物协议、领域协议与开天判断提供稳定输入
- 方便后续复核、补抓、重提炼

---

## 2. 目录约定

```text
references/
└── sources/
    ├── books/         # PDF、epub、扫描件、书摘
    ├── transcripts/   # 字幕转写后的纯文本
    ├── subtitles/     # 原始字幕文件（srt/vtt）
    ├── metadata/      # 下载与转写元信息（json）
    ├── articles/      # 网页文章、博客、newsletter
    ├── media/         # 音视频原文件或索引
    └── notes/         # 用户整理的辅助笔记
```

**基本原则**
- 原始材料与派生材料分层存放
- 一个来源尽量保留“原件 + 派生件 + 元信息”三件套
- 文件命名要稳定、可读、可追溯

---

## 3. 文件命名规范

### 3.1 通用规则
- 使用小写字母、数字、短横线
- 避免空格、中文、过长文件名
- 保留来源标识、日期或视频 ID 时，优先用短尾标记

### 3.2 推荐命名

| 类型 | 命名示例 |
|------|----------|
| 原始字幕 | `video-title.zh-Hans.srt` |
| 自动字幕 | `video-title.auto.en.vtt` |
| 转写文本 | `video-title.transcript.txt` |
| 下载元信息 | `video-title.subtitles.meta.json` |
| 转写元信息 | `video-title.transcript.meta.json` |
| 文章 | `source-name.2026-05-26.md` |

### 3.3 盘古流程优先命名
- 字幕文件优先保留语言与模式信息
- 转写文件优先保留 `transcript` 标记
- 元信息文件优先保留 `meta` 标记

---

## 4. 字幕 → 转写 → 元信息 的链路

### 4.1 下载阶段
由 `scripts/download_subtitles.sh` 负责：
- 下载字幕
- 优先人工字幕，其次自动字幕
- 输出字幕文件路径
- 同步写出字幕元信息（`.meta.json`）

### 4.2 转写阶段
由 `scripts/srt_to_transcript.py` 负责：
- 清洗字幕内容
- 输出纯文本 transcript
- 同步写出转写元信息（`.meta.json`）

### 4.3 推荐链路
```text
video URL
  → subtitles/*.srt|.vtt
  → subtitles/*.meta.json
  → transcripts/*.txt
  → transcripts/*.meta.json
  → references/research/0X-xxx.md
```

**要求**
- 不跳过字幕元信息
- 不跳过转写元信息
- 若字幕缺失，需在调研记录中说明
- 若转写质量差，需在诚实边界中说明

---

## 5. 元信息字段约定

### 5.1 字幕元信息
至少包含：
- `source_url`
- `subtitle_path`
- `download_mode`
- `language_priority`
- `subtitle_format`
- `downloaded_at`

### 5.2 转写元信息
至少包含：
- `source_path`
- `transcript_path`
- `source_type`
- `generated_at`
- `char_count`
- `paragraph_count`
- `line_count`

### 5.3 可扩展字段
可按需增加：
- `language`
- `video_title`
- `video_id`
- `author`
- `confidence`
- `remarks`

---

## 6. 与提炼流程的对应

| 资源类型 | 进入哪一步 | 作用 |
|----------|------------|------|
| 字幕文件 | 采集 | 原始语料 |
| 转写文件 | 提炼前 | 干净文本输入 |
| 元信息 | 采集/校验 | 来源追溯与质量判断 |
| 用户整理笔记 | 采集补充 | 二手参考与上下文 |

**规则**
- 采集层不解释
- 提炼层不猜测来源
- 验证层必须能回看来源链路

---

## 7. 质量要求

### 必须满足
- [ ] 同一来源尽量保留原始件
- [ ] 同一来源尽量保留派生件
- [ ] 同一来源尽量保留元信息
- [ ] 目录命名清晰、稳定、可追溯
- [ ] 不把临时文件当成正式材料

### 建议满足
- [ ] 让 transcript 与 subtitle 文件一一对应
- [ ] 让 meta 文件与派生文件同名
- [ ] 让 research 文件能回溯到 source 文件

---

## 8. 与盘古协议的关系

`references/sources/` 是盘古协议提炼的输入层。

它服务于：
- 人物协议提炼
- 领域协议提炼
- 开天判断
- 质量自检

如果输入层不完整，后续协议就要降低置信度；如果输入层可追溯，盘古就能更稳地判断哪些内容该保留、哪些内容该重写。

---

> 本规范的核心不是“文件放哪儿”，而是“盘古如何在任何一次提炼中都能回到原始证据”。
