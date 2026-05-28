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

## Built protocols

Pangu currently ships with 18 person protocols + 1 domain protocol. Each one is a standalone, installable Skill built on the Agent Skills protocol and compatible with runtimes like Claude Code, Codex, Cursor, OpenClaw, and Hermes.

What Pangu really provides is not just a list, but a continuously evolving protocol production line: take a question, rewrite it if needed, extract structure, validate boundaries, and then produce a judgment.

### Technology and semiconductors (8)

| Person | Domain | Repository | One-line install |
| --- | --- | --- | --- |
| **Elon Musk** | Tesla / SpaceX / engineering constraints / first principles | [elon-musk-skill](https://github.com/longjingcha/elon-musk-skill) | `npx skills add longjingcha/elon-musk-skill` |
| **Tim Cook** | Apple / supply chain / operational discipline / durable growth | [tim-cook-skill](https://github.com/longjingcha/tim-cook-skill) | `npx skills add longjingcha/tim-cook-skill` |
| **Jensen Huang** | NVIDIA / compute infrastructure / platform strategy | [jensen-huang-skill](https://github.com/longjingcha/jensen-huang-skill) | `npx skills add longjingcha/jensen-huang-skill` |
| **Cristiano Amon** | Qualcomm / communications platforms / chip ecosystem / device connectivity | [cristiano-amon-skill](https://github.com/longjingcha/cristiano-amon-skill) | `npx skills add longjingcha/cristiano-amon-skill` |
| **Sanjay Mehrotra** | Micron / storage infrastructure / scaled manufacturing | [sanjay-mehrotra-skill](https://github.com/longjingcha/sanjay-mehrotra-skill) | `npx skills add longjingcha/sanjay-mehrotra-skill` |
| **Jacob Thaysen** | Illumina / genome sequencing / scientific tooling platforms | [jacob-thaysen-skill](https://github.com/longjingcha/jacob-thaysen-skill) | `npx skills add longjingcha/jacob-thaysen-skill` |
| **Jim Anderson** | Coherent / optics and photonics / high-end photonics infrastructure | [jim-anderson-skill](https://github.com/longjingcha/jim-anderson-skill) | `npx skills add longjingcha/jim-anderson-skill` |
| **Dina Powell McCormick** | Meta / global affairs / public-private bridge building | [dina-powell-mccormick-skill](https://github.com/longjingcha/dina-powell-mccormick-skill) | `npx skills add longjingcha/dina-powell-mccormick-skill` |

### Finance and payment networks (6)

| Person | Domain | Repository | One-line install |
| --- | --- | --- | --- |
| **Larry Fink** | BlackRock / long-term capital allocation / fiduciary duty | [larry-fink-skill](https://github.com/longjingcha/larry-fink-skill) | `npx skills add longjingcha/larry-fink-skill` |
| **Stephen Schwarzman** | Blackstone / alternative assets / platform expansion | [stephen-schwarzman-skill](https://github.com/longjingcha/stephen-schwarzman-skill) | `npx skills add longjingcha/stephen-schwarzman-skill` |
| **David Solomon** | Goldman Sachs / market cycles / institutional clients | [david-solomon-skill](https://github.com/longjingcha/david-solomon-skill) | `npx skills add longjingcha/david-solomon-skill` |
| **Jane Fraser** | Citigroup / global networks / organizational restructuring | [jane-fraser-skill](https://github.com/longjingcha/jane-fraser-skill) | `npx skills add longjingcha/jane-fraser-skill` |
| **Michael Miebach** | Mastercard / payments platform / trust and security | [michael-miebach-skill](https://github.com/longjingcha/michael-miebach-skill) | `npx skills add longjingcha/michael-miebach-skill` |
| **Ryan McInerney** | Visa / global payments network / cross-border transactions | [ryan-mcinerney-skill](https://github.com/longjingcha/ryan-mcinerney-skill) | `npx skills add longjingcha/ryan-mcinerney-skill` |

### Industrial, aviation, and manufacturing (2)

| Person | Domain | Repository | One-line install |
| --- | --- | --- | --- |
| **Kelly Ortberg** | Boeing / aircraft manufacturing / quality governance / supply-chain recovery | [kelly-ortberg-skill](https://github.com/longjingcha/kelly-ortberg-skill) | `npx skills add longjingcha/kelly-ortberg-skill` |
| **Larry Culp** | GE Aerospace / operational turnaround / cash-flow discipline | [larry-culp-skill](https://github.com/longjingcha/larry-culp-skill) | `npx skills add longjingcha/larry-culp-skill` |

### Agriculture (1)

| Person | Domain | Repository | One-line install |
| --- | --- | --- | --- |
| **Brian Sikes** | Cargill / supply-chain resilience / food security / global agriculture infrastructure | [brian-sikes-skill](https://github.com/longjingcha/brian-sikes-skill) | `npx skills add longjingcha/brian-sikes-skill` |

### Politics and transaction narratives (1)

| Person | Domain | Repository | One-line install |
| --- | --- | --- | --- |
| **Donald Trump** | attention / transaction narrative / conflict management / coalition reshaping | [donald-trump-skill](https://github.com/longjingcha/donald-trump-skill) | `npx skills add longjingcha/donald-trump-skill` |

### Domain protocol

| Topic | Domain | Repository | One-line install |
| --- | --- | --- | --- |
| **X Mentor** | X/Twitter growth operations | [x-mentor-skill](https://github.com/longjingcha/x-mentor-skill) | `npx skills add longjingcha/x-mentor-skill` |

Person protocols extract how a person thinks. Domain protocols extract how a field works. Each repository includes full research notes and example dialogues.

Need a person or domain that is not on the list? Install Pangu and say: “Build an XXX protocol.”

You can also install an existing protocol directly, for example Tim Cook: `npx skills add longjingcha/tim-cook-skill`

---

## What Pangu provides

Pangu provides a full protocol production chain, not just a one-off answer.

### 1. Person protocol
For public figures, founders, creators, and thinkers.

It captures:
- mental models
- decision heuristics
- expression rules
- values and anti-patterns
- honesty boundaries

### 2. Domain protocol
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
