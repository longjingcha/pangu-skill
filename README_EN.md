# Pangu Skill

> Pangu is not copying people. It is turning people, domains, and questions into callable protocols.

[English](README_EN.md) · [中文](README.md)

---

## What this is

`pangu-skill` is a protocol factory for AI skills.

It goes beyond person-to-person imitation and supports three layers:
- `Person Protocol` — extract a public figure’s cognitive structure, decision heuristics, and expression style
- `Domain Protocol` — turn a field or methodology into a structured, executable knowledge protocol
- `Open-the-sky` capability — if the question itself is broken, rewrite the question before answering it

---

## How it differs from `nuwa-skill`

| Dimension | `nuwa-skill` | `pangu-skill` |
|---|---|---|
| Core goal | Distill a person into a runnable Skill | Protocolize people, domains, and the question itself |
| Main axis | Mental models and roleplay | Person protocol + domain protocol + question rewriting |
| Output shape | Person Skill / Topic Skill | Person Protocol / Domain Protocol |
| Key capabilities | Mental models, heuristics, expression DNA | Protocol extraction, domain structuring, open-the-sky routing, protocol auditing |
| Workflow style | Research → distill → build → validate | Route → rewrite → extract → template → audit |
| Resource organization | Research files + skill template | Input spec + extraction framework + templates + audit chain |

### Why Pangu is a better fit for a protocol factory

- It does not only answer “who is this like?” — it first checks whether the question itself is valid.
- It does not stop at people — it turns domain knowledge into a callable protocol.
- It does not only do roleplay — it separates question rewriting, protocol extraction, and quality auditing into distinct steps.
- It does not rely on one template — it ships with two parallel templates: person and domain.

Pangu is the upgrade path when you want more than imitation.

---

## Core workflow

Pangu does four things after you give it a name, topic, or vague need — but unlike `nuwa-skill`, this is not a pure distillation pipeline.

1. **Decide whether to open the sky first** — if the question contains a false premise, unclear boundaries, or a symptom disguised as a goal, rewrite the question before continuing.

2. **Collect sources in parallel** — gather books, podcasts/interviews, social posts, critics’ views, decision records, and a timeline with 6 agents running at the same time.

3. **Extract two kinds of protocols** — not only person protocols, but also domain protocols. Person protocols capture mental models, heuristics, expression rules, values, and honesty boundaries. Domain protocols capture scope, structure, criteria, paths, failure modes, and schools of thought.

4. **Validate and audit the output** — make sure person protocols are coherent without guessing, domain protocols lead to real decisions and actions, and open-the-sky rewriting actually corrected the original question. Then run the auditor before shipping.

Full methodology: `references/pangu-extraction-framework.md`.

---

## Repository structure

```text
pangu-skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── references/
│   ├── pangu-extraction-framework.md
│   ├── pangu-skill-template.md
│   └── pangu-sources-spec.md
└── scripts/
    ├── pangu_subtitle_fetcher.sh
    ├── pangu_transcript_cleaner.py
    ├── pangu_protocol_diagnoser.py
    └── pangu_protocol_auditor.py
```

---

## What Pangu provides

Pangu provides a full protocol production chain, not just a one-off answer.

### 1. Person Protocol
For public figures, founders, creators, and thinkers.

It captures:
- mental models
- decision heuristics
- expression rules
- values and anti-patterns
- honesty boundaries

### 2. Domain Protocol
For fields, methodologies, themes, and frameworks.

It captures:
- scope
- core map
- criteria
- path
- pitfalls and counterexamples
- failure modes
- schools of thought
- decision actions

### 3. Open-the-sky capability
When the question itself is broken, Pangu rewrites it before trying to answer.

### 4. Diagnoser and auditor tools
- `pangu_protocol_diagnoser` finds protocol gaps and open-the-sky signals
- `pangu_protocol_auditor` checks whether the output is ready to ship
- `pangu_subtitle_fetcher` and `pangu_transcript_cleaner` provide the raw source pipeline
- source names are standardized as `pangu-writings.md`, `pangu-dialogues.md`, `pangu-expression.md`, `pangu-commentary.md`, `pangu-decisions.md`, and `pangu-timeline.md`

### 5. End-to-end input pipeline
From subtitles and transcripts to source specs, extraction frameworks, templates, and auditing, Pangu is a system for continuously producing protocols.

---

## Source pipeline

Pangu treats sources as a traceable pipeline:
- subtitle fetcher → raw subtitles + metadata
- transcript cleaner → clean transcript + metadata
- source specification → storage and naming rules
- extraction framework → protocol extraction standard
- templates → final output shape
- protocol diagnoser → gap detection and open-the-sky signals
- protocol auditor → quality checks before release
- research file names are standardized as `pangu-writings.md`, `pangu-dialogues.md`, `pangu-expression.md`, `pangu-commentary.md`, `pangu-decisions.md`, and `pangu-timeline.md`

---

## Current state

This repository is designed to be copied as a standalone protocol system.

If you want to build a new person protocol or domain protocol, install the skill and say:

- “Build a Paul Graham protocol.”
- “Give me a domain protocol for growth.”
- “Open the sky first — this question is probably wrong.”

---

## Links

- Chinese README: `README.md`
- Main skill spec: `SKILL.md`
- Source spec: `references/pangu-sources-spec.md`
- Extraction framework: `references/pangu-extraction-framework.md`
- Skill templates: `references/pangu-skill-template.md`

---

## License

MIT
