# Architecture

> Full system architecture as of July 2026.  
> See [GOVERNANCE.md](GOVERNANCE.md) for governance model, [schema.yaml](schema.yaml) for memory schema.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        User Query / Task                            │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           ROUTER                                    │
│                                                                     │
│   Task → Capability → Provider Selection → Execute                 │
│                                                                     │
│   Fallback Chain:  DeepSeek(primary) → Kimi → Xiaomi → 小Q(local)  │
└──┬──────────────┬──────────────┬──────────────┬────────────────────┘
   │              │              │              │
   ▼              ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ DeepSeek │ │   Kimi   │ │  Xiaomi  │ │   小Q    │
│  V4      │ │  k2.5    │ │ mimo-v2.5│ │ Qwen3-8B │
│──────────│ │──────────│ │──────────│ │──────────│
│ Primary  │ │ Analyst  │ │ Long ctx │ │ Local    │
│ Tool acc │ │ Deep     │ │ 1M token │ │ Free     │
│ ess      │ │ analysis │ │          │ │ Offline  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

---

## Memory Architecture (4-Layer)

```
   🔥 HOT MEMORY (2,200 chars, injected every turn)
   ┌─────────────────────────────────────────────────────┐
   │ Route hints, recent corrections, capability pointers │
   │ Only routes — never stores executable truth          │
   └─────────────────────┬───────────────────────────────┘
                         │
                         ▼
   ❄️ COLD MEMORY (unlimited, file-based)
   ┌─────────────────────────────────────────────────────┐
   │  Episodic  │  Semantic  │  Procedural               │
   │  (events)  │  (facts)   │  (workflows)              │
   │            │            │                            │
   │  H-001~005 │  Schema    │  Observation checklist     │
   │  AP-001    │  Rules     │  Governance model          │
   └─────────────────────┬───────────────────────────────┘
                         │
                         ▼
   ⚙️ CONFIG (`.env`, `config.yaml`)
   ┌─────────────────────────────────────────────────────┐
   │ API keys, endpoints, retry logic, tool definitions   │
   │ Executable truth — never in hot memory               │
   └─────────────────────┬───────────────────────────────┘
                         │
                         ▼
   ⏳ RUNTIME (session-scoped, ephemeral)
   ┌─────────────────────────────────────────────────────┐
   │ Tool outputs, task progress, conversation context    │
   │ Discarded when session ends                          │
   └─────────────────────────────────────────────────────┘
```

---

## Governance Model

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐
│  Idea    │───▶│ Proposal │───▶│ Backlog  │───▶│ Hypothesis   │
│ (random  │    │ (designed│    │ (queued) │    │ Review       │
│  thought)│    │  doc)    │    │          │    │              │
└──────────┘    └──────────┘    └──────────┘    └──────┬───────┘
                                                        │
                                            ┌───────────┴───────────┐
                                            ▼                       ▼
                                    ┌──────────────┐       ┌──────────────┐
                                    │  Hypothesis  │       │  Invalidated  │
                                    │  (provisional│       │  (rejected)   │
                                    │  /validated) │       │               │
                                    └──────────────┘       └──────────────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │  Constraint  │
                                    │  (must follow)│
                                    └──────────────┘
```

---

## Object Definitions

| Object | Description | Location |
|--------|-------------|----------|
| **Constraint** 🔒 | Must follow, no validation needed | `architecture/constraints/` |
| **Hypothesis** 🔬 | Awaiting evidence from Observation Week | `architecture/hypotheses/` |
| **Backlog** 📋 | Queued for future evaluation | `architecture/backlog/` |
| **Proposal** 📐 | Complete design doc, pre-validation | `architecture/proposals/` |

---

## Key Files

| File | Purpose |
|------|---------|
| `GOVERNANCE.md` | 5-question governance framework |
| `schema.yaml` | Memory schema (Learning Event, Admission Rule) |
| `observation-checklist.md` | Observation Week tracking checklist |
| `ARCHITECTURE.md` | This file — system overview |
| `project_state.json` | Current project phase and status |

---

## Current Status

```
Phase:     Observation Week 1 / Feature Freeze
Status:    Collecting real usage data
Next:      Architecture Review → Phase 2a (Environment Registry)
```

---

## Design Constraints

- **Single-user, Windows environment** — No distributed system complexity
- **Lightweight** — No Redis, Kafka, or databases needed
- **Pragmatic** — Each abstraction must solve ≥2 real problems
- **Discovery cost matters** — Archived capabilities must remain discoverable
