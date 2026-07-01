# Cold Memory Kernel

*The evolving memory architecture behind Hermes.*

**Permissioned Temporal Memory Kernel — from cold storage to layered runtime.**

A structured memory system for AI agents, originally built as a cold-memory fix for a single problem: **14 entries written, 0 ever searched.** It has since evolved into a four-layer architecture governing how an agent stores, routes, retrieves, and acts on memory across sessions.

---

## Why is it still called cold-memory-kernel?

The repository keeps its historical name to preserve links, discussions, and issue history. The cold-memory layer is now one component of a broader architecture — see [ARCHITECTURE.md](ARCHITECTURE.md) for the full picture.

---

## Architecture at a glance

```
Hot Memory       → Routing hints + special warnings (no executable truth)
     ↓
Cold Memory      → Structured knowledge (episodic / semantic / procedural)
     ↓
Config / Script  → Executable truth (endpoints, auth, retry logic)
     ↓
Runtime          → load config → execute
```

Core principle: **Hot memory never stores executable truth. It only routes.**

---

## Repository structure

```
├── README.md           ← this file
├── ARCHITECTURE.md     ← system design overview
├── design/             ← design docs & traces
├── scripts/            ← CLI tools (cold-memory.py, should_activate.py)
├── src/                ← kernel implementation
└── CHANGELOG.md
```

---

## Current status

| Component | Status |
|-----------|--------|
| Cold Memory (3-tier JSON) | ✅ v1.0 — 17 entries, 10KB, episodic/semantic/procedural |
| Trust Policy (L0/L1/L2) | ✅ v0 — authority boundaries verified |
| Activation Gate | ✅ v4 — keyword-triggered retrieval |
| L2 Metadata Policy | ✅ v1 — reference-only, no inference |
| Hot Memory | ✅ Routing principle established, 64% utilization |
| Project State | ✅ Milestone-triggered snapshots |
| Closure/Maintenance/Extension | ✅ Governance modes defined |
| Observation-driven refinement | 🚧 Observation Week — verifying in real use |

---

Built for a single-user student scenario (Windows laptop, Hermes Agent). Principles are general but the implementation is lightweight by design.
