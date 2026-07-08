# Cold Memory Kernel
## Hermes Agent Architecture Repository

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jim-688/cold-memory-kernel?style=social)](https://github.com/jim-688/cold-memory-kernel)
[![GitHub last commit](https://img.shields.io/github/last-commit/jim-688/cold-memory-kernel)](https://github.com/jim-688/cold-memory-kernel)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![中文](https://img.shields.io/badge/docs-%E4%B8%AD%E6%96%87-blue)](README.md)
[![GitHub issues](https://img.shields.io/github/issues/jim-688/cold-memory-kernel)](https://github.com/jim-688/cold-memory-kernel/issues)

---

### What is this?

一个用于 AI Agent 的架构治理与记忆系统设计仓库。
An architecture repository for AI agent memory, governance, and capability design.

### What problems does it solve?

| Problem | Solution |
|---------|----------|
| 🔄 Agent 记忆写了但没用 | Hot→Cold→Config→Runtime 四层架构 |
| 🎯 工具体积膨胀 | Tool Gating + Register≠Expose 分离 |
| ⚡ Provider 选错/超时 | Provider Health Score + 动态路由 |
| 📋 架构决策混乱 | Hypothesis + Observation Week 证据驱动 |
| 🧩 能力扩展困难 | Capability Registry + AP-001 提案 |

### Who is it for?

正在开发 AI Agent / Coding Agent 的开发者。
Built for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

### Quick Demo

```bash
python demo.py
# → Shows current architecture status, hypotheses, and routing logic
```

### Current Status

```
Phase:  Observation Week 1 (Feature Freeze)
Status: Collecting real usage data before architecture decisions
```

---

## 🏗️ Architecture at a Glance

---

## 🏗️ Architecture at a Glance

```
  User Query
       │
       ▼
┌─────────────────────────────────────────────┐
│              Router                          │
│  DeepSeek → Kimi → Xiaomi → 小Q (fallback)  │
└──────┬──────────┬──────────┬────────────────┘
       ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────┐
│ DeepSeek │ │   Kimi   │ │Xiaomi│
│ (Primary)│ │(Analyst) │ │(Long)│
│ tool acc │ │ no tools │ │  1M  │
│   ess    │ │  deep    │ │ ctx  │
└──────────┘ └──────────┘ └──────┘
     ┌──────┐
     │ 小Q  │
     │(Local│
     │  0$) │
     └──────┘

Memory Layers:
  🔥 Hot    (2,200 chars) → Route hints, recent corrections
  ❄️ Cold   (unlimited)   → Structured knowledge, verified facts
  ⚙️ Config (.env)        → API keys, executable truths
  ⏳ Runtime (session)    → Tool outputs, ephemeral state
```

---

## 🎯 Governance Model

| Type | What it means | Example |
|------|--------------|---------|
| **Constraint** 🔒 | Must follow, no debate | Register ≠ Expose separation |
| **Hypothesis** 🔬 | Awaiting evidence | H-004: Tool Gating, H-005: Provider Health Score |
| **Backlog** 📋 | Queued for future | Skill Discovery, Hook System |
| **Proposal** 📐 | Complete design | AP-001: Capability-Driven Architecture |

**Lifecycle:** `Idea → Proposal → Backlog → Hypothesis Review → Hypothesis → Validated ❌✅`

---

## 🧪 Current Hypotheses (H-001 ~ H-005)

| ID | Hypothesis | Status |
|----|-----------|--------|
| H-001 | **Search Policy** — when to search vs. use internal knowledge | `provisional` |
| H-002 | **Safety Policy** — tiered safety response | `provisional` |
| H-003 | **Decision Principles** — meta-principles for agent decisions | `provisional` |
| H-004 | **Tool Gating** — expose tools by task capability, not default | `provisional` |
| H-005 | **Provider Health Score** — dynamic routing by latency/success | `provisional` |

> **Current Phase:** 🔭 Observation Week (Feature Freeze) — collecting real usage data before any architecture decision.

---

## 📁 Repo Structure

```
├── README.md
├── ARCHITECTURE.md              ← Full system design
├── GOVERNANCE.md                ← 5-question governance framework
├── schema.yaml                  ← Memory schema definition
├── observation-checklist.md     ← Observation Week tracking
│
├── architecture/
│   ├── hypotheses/              ← H-001 through H-005
│   ├── proposals/               ← AP-001: Capability architecture
│   └── backlog/                 ← Future ideas & references
│
├── notes/
│   └── c-language/              ← C language study notes (Weng Kai MOOC)
│       └── ch1-2/               ← Chapters 1-2 review with Q&A
│
└── references/
    └── claude-code-architecture.md
```

---

## 💡 Design Principles

```
1. 只记不可推导的信息    →  Only remember what can't be re-derived
2. 每层抽象必须消除≥2个问题 →  Each abstraction must solve ≥2 real problems
3. 证据驱动，非功能驱动    →  Evidence-driven, not feature-driven
4. Capability优先         →  Capability first, adapter second, software last
```

---

## 📚 Also Includes: C Language Study Notes

Following Weng Kai's "C Programming" MOOC (Zhejiang University). Each chapter: **Knowledge Points → Questions → Answers with Explanations.** Wrong-answer-first layout.

| Chapter | Topics | Status |
|---------|--------|--------|
| Ch1-2 | Program structure, variables, data types, operators | ✅ Done |
| Ch3 | Conditionals and loops | ⏳ Coming soon |

---

## 🚀 Quick Start

```bash
git clone https://github.com/jim-688/cold-memory-kernel.git
cd cold-memory-kernel

# Start with the governance model
cat GOVERNANCE.md

# Explore the hypotheses
cat architecture/hypotheses/H-004.json
cat architecture/hypotheses/H-005.json

# Read the full architecture
cat ARCHITECTURE.md
```

---

## Built For

| | |
|---|---|
| 👤 **User** | Single-developer, student (Windows, Hermes Agent) |
| 📐 **Scale** | Lightweight by design — principles general, implementation pragmatic |
| 🛠️ **Stack** | Hermes Agent, DeepSeek/Kimi/Xiaomi/Ollama, VS Code/Git |

---

## 📜 License

MIT

---

<p align="center">
  <sub>⭐ If this helped you think about agent architecture, consider starring the repo!</sub>
</p>
