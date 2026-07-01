# Architecture

> Describes the architecture as of [current commit]. Major changes trigger a doc update.

---

## Evolution

```
Cold Memory (single layer)
        │
        ▼
Trust Policy (L0/L1/L2)
        │
        ▼
Layered Memory (hot + cold)
        │
        ▼
Hermes Memory Architecture (4-layer: Hot → Cold → Config → Runtime)
        │
        ▼
Governance modes (Closure / Maintenance / Extension)
```

The system started as a fix for one problem: "memory entries were written but never searched." Each layer was added in response to a real failure mode, not pre-planned.

---

## Layers

### Hot Memory (Routing Layer)

**Role:** Lightweight index. Tells the agent *what exists, where to find it, and what to watch out for.*

**Does NOT store:**
- Executable configuration (endpoints, auth keys, schemas)
- Full knowledge content
- Verbatim conversation history

**Stores:**
- Capability tags ("xiaomi-api")
- Route hints ("requires wrapper timeout")
- Special warnings ("thinking must be disabled")

### Cold Memory (Knowledge Layer)

**Role:** Structured long-term storage. Three tiers:

| Tier | Content | TTL | Example |
|------|---------|-----|---------|
| Episodic | Session summaries, event records | 90 days | "2026-07-01: Round 1 Archive completed" |
| Semantic | Facts, preferences, stable knowledge | Never | "User studies big data, goal is 专升本" |
| Procedural | Workflows, configs, reusable patterns | Never | "API key lookup order" |

### Config / Script Layer (Executable Truth)

**Role:** The single source of executable configuration. Endpoints, auth formats, retry logic, payload schemas live here — in `.env`, `openclaw.json`, wrapper scripts, or cold storage JSON.

Runtime never guesses; it loads from here.

### Runtime (Execution Layer)

**Role:** `load config → execute`. No speculation, no fallback to hot memory for execution details.

---

## Runtime Principles

1. **L0 is authoritative.** Runtime output (command results, API responses) overrides memory.
2. **L1 is working state.** Current session facts, verified before use.
3. **L2 is reference only.** Cold cache, read by default. Never inferred from.
4. **Hot memory is never authoritative.** It routes; it doesn't execute.
5. **Retrieval is uncertainty-driven.** Not every query triggers cold memory search — only when confidence is low.
6. **Project state tracks "where am I?"** Not "what do I know?" — that's cold memory's job.

---

## Current Scope

| State | Component |
|-------|-----------|
| ✅ Stable | Cold Memory (3-tier JSON, 17 entries, 10KB) |
| ✅ Stable | Trust Policy (L0/L1/L2 boundaries verified) |
| ✅ Stable | Activation Gate (v4, keyword-triggered) |
| ✅ Stable | Hot Memory routing principle |
| ✅ Stable | Project State (milestone-triggered snapshots) |
| ✅ Stable | Closure/Maintenance/Extension governance |
| 🚧 In progress | Observation Week — verifying in real use |
| ⏳ Future | Automatic activation refinement |
| ⏳ Future | Cold → Hot promotion mechanisms |

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Hot memory doesn't store truth | Prevents prompt bloat, version drift, and logic duplication |
| Only 4 fields in project state | Project state tracks "where am I?", not "what do I know?" |
| Merge queue decided by usage | Real usage reveals overlap better than static analysis |
| Archive index retained | Lowers discovery cost — system knows a capability exists even when inactive |
| Documentation describes stable consensus | Prevents docs from becoming inflated design notes |
