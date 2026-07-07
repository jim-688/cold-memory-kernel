# Cold Memory Kernel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jim-688/cold-memory-kernel?style=social)](https://github.com/jim-688/cold-memory-kernel)
[![GitHub last commit](https://img.shields.io/github/last-commit/jim-688/cold-memory-kernel)](https://github.com/jim-688/cold-memory-kernel)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

> **The evolving memory and governance architecture behind a practical AI Agent — from cold storage to layered runtime.**

A structured architecture system built for Hermes Agent, encompassing memory management, tool governance, provider routing, and capability-driven design. Started as a fix for a single problem — *"14 memory entries written, 0 ever searched"* — and evolved into a full architecture framework.

----

## Architecture Overview

```
Hot Memory     → Routing hints + recent corrections (2200 chars, injected every turn)
Cold Memory    → Structured knowledge: episodic / semantic / procedural
Config/Scripts → Executable truth: API keys, endpoints, retry logic
Runtime        → Session state, tool outputs (ephemeral)
```

## Governance Model

| Type | Description | Example |
|------|-------------|---------|
| **Constraint** | Must follow, no validation needed | Register ≠ Expose separation |
| **Hypothesis** | Awaiting Observation Week data | H-004: Tool Gating, H-005: Provider Health Score |
| **Backlog** | Queued for future evaluation | Skill Discovery, Hook System |
| **Proposal** | Complete design, pre-validation | AP-001: Capability-Driven Architecture |

**Flow:** `Idea → Proposal → Backlog → Hypothesis Review → Hypothesis → Validated/Invalidated`

## Key Hypotheses

| ID | Statement | Status |
|----|-----------|--------|
| H-001 | Search Policy — when to search vs. use internal knowledge | provisional |
| H-002 | Safety Policy — tiered safety response | provisional |
| H-003 | Decision Principles — meta-principles for agent decisions | provisional |
| H-004 | Tool Gating — expose tools by task capability, not by default | provisional |
| H-005 | Provider Health Score — dynamic provider routing by latency/success rate | provisional |

## Repository Structure

```
├── README.md
├── ARCHITECTURE.md         ← System overview
├── GOVERNANCE.md           ← 5-question governance framework
├── schema.yaml             ← Memory schema definition
├── observation-checklist.md
├── architecture/
│   ├── hypotheses/         ← H-001 through H-005
│   ├── proposals/          ← AP-001: Capability architecture
│   └── backlog/            ← Future ideas
└── references/
    └── claude-code-architecture.md
```

## Design Principles

1. **Only remember what can't be re-derived** — Admission Rule for memory
2. **Each abstraction must solve ≥2 real problems** — no complexity without justification
3. **Evidence-driven, not feature-driven** — Observation Week before implementation
4. **Capability first, adapter second, software last** — AP-001 direction

## Built For

- **User**: Single-developer, student environment (Windows, Hermes Agent)
- **Scale**: Lightweight by design — principles are general but implementation is pragmatic
- **Stack**: Hermes Agent, DeepSeek/Kimi/Xiaomi/Ollama providers, VS Code/Git

## Getting Started

```bash
# Clone and explore
git clone https://github.com/jim-688/cold-memory-kernel.git
cd cold-memory-kernel
# Read the governance model
cat GOVERNANCE.md
# Explore hypotheses
cat architecture/hypotheses/H-004.json
```

## License

MIT
