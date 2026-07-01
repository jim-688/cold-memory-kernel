# Cold Memory Kernel

**Permissioned Temporal Memory Kernel v0.1**

A lightweight, structured cold memory system for AI agents, with trust hierarchy (L0/L1/L2), activation gate, and write-back permission control.

Built in a single day to fix a core problem: **memory retrieval friction so high that 14 entries were written but 0 were ever searched.**

---

## Architecture

### Three-Layer Trust Hierarchy

```
L0 (External Truth)     → Runtime / system commands / credentials
L1 (Validated Session)  → Working state, current verified facts
L2 (Cold Cache)         → Historical records, reference only
```

### Five-State Kernel (Thinking Process)

Before any output, the system runs through five cognitive states:

```
① Observe  → Collect facts only. No judgment.
② Separate → Split into: Fact / Unknown / Speculation (never mix)
③ Expand   → List at least 3 possibilities before narrowing
④ Evaluate → Compare evidence weights, not feelings
⑤ Commit   → Confirm: am I answering or just filling silence?
```

### Five-Layer Protocol (Output Structure)

```
L0: Activation Gate     → Should I query cold memory? (keyword trigger)
L1: Fact                → What do I actually know?
L2: Evidence            → What's my basis? (logs, output, config)
L3: Judgment            → Based on evidence, I conclude... (with confidence)
L4: Action              → What to verify next?
```

---

## Key Design Decisions

### Why not a vector database?
For a student learning assistant, keyword search + importance scoring covers 95% of use cases. Vector search adds complexity without proportional value at this scale.

### Why JSON files not SQLite?
Zero dependencies, human-readable, git-friendly. The cold memory is a "structured text stack" not a database — SQLite would be premature optimization.

### Why L2 is read-only by default?
Prevents historical data from contaminating active decision-making. L2 can only influence via controlled promotion (confidence ≥ 0.8 + corroboration), currently disabled in baseline v0.

---

## Components

| File | Purpose |
|------|---------|
| `src/cold-memory.py` | Cold memory manager: add, search, list, health check, archive |
| `src/should_activate.py` | Activation gate: when to trigger memory search |
| `src/xiaomi_stable.py` | Xiaomi API stable wrapper (max_tokens fixed to 2048) |

---

## Trace Validation

The system passed 3 rounds of boundary testing:

| Trace | Test | Result |
|-------|------|--------|
| v1 | Authority separation (L2 write-blocked) | ✅ PASS |
| v2-A | Missing field → no inference | ✅ PASS |
| v2-B | L0 vs L2 conflict → L0 wins | ✅ PASS |
| v2-C | Partial corruption → no hallucination | ✅ PASS |
| v3 | Temporal consistency (L1 override L2 stale) | ✅ PASS |
| v4 | Implicit activation (not yet tested) | ⏳ PENDING |

---

## Status

**STABLE v0.1** — authority-correct, semantically safe, temporally consistent.

One remaining risk: **activation reliability** — the system is correct when called, but whether it spontaneously self-triggers in a new session is the final validation.

---

## References

- Hermes Agent Issue [#52881](https://github.com/NousResearch/hermes-agent/issues/52881): Layered Memory System
- agentmemory (rohitg00): 4-tier memory model inspiration
- claude-mem (thedotmack): Progressive retrieval pattern
- Consulted: DeepSeek, Kimi, Xiaomi, Claude, ChatGPT during design

---

## License

MIT
