# Cold Memory Kernel

*The evolving architecture behind a practical AI Agent.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A structured memory and governance system for AI agents — from cold storage to layered architecture. Built for a single-user student scenario (Windows, Hermes Agent), but the principles are framework-agnostic.

## Why this exists

This started as a fix for one problem: **14 memory entries written, 0 ever searched.** The agent was remembering things but never using them. It has since evolved into a four-layer architecture governing how an agent stores, routes, retrieves, and acts on information.

## Architecture

```
Hot Memory     → Routing hints + recent corrections (2200 chars, injected every turn)
Cold Memory    → Structured knowledge: episodic / semantic / procedural
Config/Scripts → Executable truth: API keys, endpoints, retry logic
Runtime        → Session state, tool outputs (ephemeral)
```

Core principle: **Hot memory never stores executable truth. It only routes.**

## Governance Model

The system uses four object types to manage architecture evolution:

| Type | Description | Example |
|------|-------------|---------|
| **Constraint** | Must follow, no validation needed | Register ≠ Expose separation |
| **Hypothesis** | Awaiting Observation Week data | Tool Gating, Provider Health Score |
| **Backlog** | Queued for future evaluation | Skill Discovery, Hook System |
| **Proposal** | Complete design, pre-validation | AP-001: Capability-Driven Architecture |

New ideas: `Idea → Proposal → Backlog → Hypothesis Review → Hypothesis → Validated/Invalidated`

## Repository Structure

```
├── GOVERNANCE.md               ← Architecture governance (5 questions)
├── schema.yaml                 ← Memory schema (Learning Event structure)
├── observation-checklist.md    ← Observation Week tracking
├── ARCHITECTURE.md             ← System overview (historical)
├── architecture/
│   ├── hypotheses/             ← H-001 through H-005
│   ├── proposals/              ← AP-001: Capability architecture
│   └── backlog/                ← Future ideas
├── references/
│   └── claude-code-architecture.md  ← Learnings from Claude Code
└── README.md
```

## Key Principles

1. **只记不可推导的信息** (Only remember what can't be re-derived)
2. **每增加一层抽象，都必须能消除至少两个具体问题** (Each abstraction must solve ≥2 problems)
3. **证据驱动架构** (Evidence-driven, not feature-driven)
4. **使用驱动，不是完美驱动** (Usage drives design, not perfection)

## Current Status

| Component | Status |
|-----------|--------|
| Memory Schema v1 | ✅ Learning Event + Admission Rule |
| Tool Metadata | ✅ isReadOnly/isDestructive/supportsParallel |
| Architecture Governance | ✅ GOVERNANCE.md |
| H-001~H-003 | ✅ provisional |
| H-004: Tool Gating | ✅ provisional |
| H-005: Provider Health Score | ✅ provisional |
| AP-001: Capability Architecture | ✅ proposal |
| Observation Week | 🚧 In progress |
| Kimi Code / Xiaomi / OpenClaw integration | ✅ Dual-channel |
| Everything search adapter | ⏸️ Phase 2a |

## Design Decisions

Key architecture decisions are documented in the hypothesis files. Each includes:
- Problem statement and rationale
- Verification criteria
- Alternatives considered
- Expected benefit/cost

## License

MIT
