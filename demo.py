#!/usr/bin/env python3
"""
Cold Memory Kernel — Architecture Demo.

Simulates the Hermes routing pipeline: Task → Capability → Policy → Router → Provider.
"""
import json, random, time
from pathlib import Path

ROOT = Path(__file__).parent

PROVIDERS = {
    "DeepSeek": {"cost": 0.02, "latency_ms": 320, "capabilities": ["code", "reasoning", "tool_use"], "status": "healthy"},
    "Kimi":     {"cost": 0.01, "latency_ms": 800, "capabilities": ["analysis", "long_text"],    "status": "healthy"},
    "Xiaomi":   {"cost": 0.005,"latency_ms": 1500,"capabilities": ["long_context", "reasoning"],"status": "degraded"},
    "小Q":      {"cost": 0,    "latency_ms": 3000,"capabilities": ["simple", "local"],         "status": "offline"},
}

TASKS = [
    ("Write a Java class", "code", "DeepSeek"),
    ("Analyze this paper", "analysis", "Kimi"),
    ("Summarize 100K tokens", "long_context", "Xiaomi"),
    ("Fix this bug", "reasoning", "DeepSeek"),
    ("Quick math", "simple", "小Q"),
]

def simulate():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       Cold Memory Kernel — Routing Pipeline Demo        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    for task, capability, expected in TASKS:
        print(f"  Task:          {task}")
        print(f"  └─ Capability:  {capability}")
        print(f"     ├─ Policy:   Score providers by capability match + health + latency")
        print(f"     ├─ Router:   Select best available...")
        time.sleep(0.3)

        # Simple scoring
        scores = {}
        for name, info in PROVIDERS.items():
            if info["status"] == "offline":
                continue
            cap_score = 1.0 if capability in info["capabilities"] else 0.2
            health_score = 0.9 if info["status"] == "healthy" else 0.5
            latency_score = max(0, 1 - info["latency_ms"] / 5000)
            scores[name] = (cap_score * 0.5 + health_score * 0.3 + latency_score * 0.2) * 100

        best = max(scores, key=scores.get)
        print(f"     └─ Selected:  {best} (score: {scores[best]:.0f}/100)")
        print(f"        Expected:  {expected} {'✅' if best == expected else '❌'}")
        print()

    print("─── Provider Health Scores ───")
    for name, info in PROVIDERS.items():
        status_icon = "🟢" if info["status"] == "healthy" else "🟡" if info["status"] == "degraded" else "🔴"
        print(f"  {status_icon} {name:10s}  {info['latency_ms']:>4}ms  ${info['cost']:.3f}/req  {info['status']}")

    print()
    state = json.loads((ROOT / "project_state.json").read_text())
    print(f"  Current Phase: {state['phase']}  |  {state['status']}")

if __name__ == "__main__":
    simulate()
