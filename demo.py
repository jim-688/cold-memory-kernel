#!/usr/bin/env python3
"""
Cold Memory Kernel — CLI demo.

Shows how the architecture governance model works in practice.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent

def show_architecture():
    print("""
╔══════════════════════════════════════════════════════════╗
║           Cold Memory Kernel — Architecture             ║
╚══════════════════════════════════════════════════════════╝

  🔥 HOT    → Route hints (2,200 chars, injected every turn)
  ❄️ COLD   → Structured knowledge (episodic/semantic/procedural)
  ⚙️ CONFIG → API keys, endpoints, retry logic
  ⏳ RUNTIME→ Session state (ephemeral)

  Principle: Hot memory never stores executable truth. It only routes.
    """)

def show_hypotheses():
    print("Active Hypotheses:\n")
    hyps_dir = ROOT / "architecture" / "hypotheses"
    for f in sorted(hyps_dir.glob("*.json")):
        data = json.loads(f.read_text())
        print(f"  {data['id']}: {data['statement'][:70]}...")
        print(f"       Status: {data['status']}  |  Confidence: {data.get('confidence','?')}")
        print()

def show_proposals():
    print("Active Proposals:\n")
    props_dir = ROOT / "architecture" / "proposals"
    for f in sorted(props_dir.glob("*.md")):
        print(f"  {f.stem}")
    print()

def show_status():
    state = json.loads((ROOT / "project_state.json").read_text())
    print(f"  Phase: {state['phase']}")
    print(f"  Status: {state['status']}")
    print(f"  Updated: {state['updated_at']}")
    print()

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    if cmd == "arch" or cmd == "all":
        show_architecture()
    if cmd == "hyps" or cmd == "all":
        show_hypotheses()
    if cmd == "props" or cmd == "all":
        show_proposals()
    if cmd == "status" or cmd == "all":
        show_status()
    if cmd == "all":
        print("Usage: python demo.py [arch|hyps|props|status]")
