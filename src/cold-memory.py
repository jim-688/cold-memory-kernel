"""
Cold Memory Manager — structured hot/cold memory system for Hermes Agent.

Architecture (agentmemory-inspired 3-tier):
  Hot Memory (memory tool, 2200 chars) — injected every turn
  ├── user_profile    — identity, goals, core constraints (NEVER evict)
  ├── active_progress — current learning progress
  └── recent_prefs    — recent corrections, preferences (<30 days)

  Cold Memory (~/.hermes/memory/cold/, unlimited, JSON structured)
  ├── episodic/       — session summaries, timestamped events (TTL: 90 days)
  ├── semantic/       — extracted facts, stable preferences, user profile archive
  └── procedural/     — tool workflows, system configs, reusable patterns

Usage:
  python cold-memory.py add <type> <content> [--tags a,b,c] [--importance 0.8]
  python cold-memory.py search <query> [--type episodic] [--limit 5]
  python cold-memory.py list [--type semantic] [--limit 10]
  python cold-memory.py archive         # auto-archive old/expired entries
  python cold-memory.py get <id>
  python cold-memory.py migrate         # migrate old markdown -> structured JSON
  python cold-memory.py hot-archive     # archive hot memory to cold
"""

import os, sys, json, time, re, shutil, uuid
from datetime import datetime, timezone, timedelta

COLD_DIR = os.path.expanduser("~/.hermes/memory/cold")
INDEX_PATH = os.path.join(COLD_DIR, "index.json")

# Default TTLs
TTL = {
    "episodic": 90,      # days
    "semantic": None,    # never expires
    "procedural": None,  # never expires
}

# Default importance weights by type
DEFAULT_IMPORTANCE = {
    "episodic": 0.5,
    "semantic": 0.8,
    "procedural": 0.6,
}


def _load_index():
    if not os.path.exists(INDEX_PATH):
        return {"version": "1.0", "last_updated": _now(), "entries": {"episodic": {}, "semantic": {}, "procedural": {}}, "stats": {"total_entries": 0, "total_size_bytes": 0}}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_index(index):
    index["last_updated"] = _now()
    total = 0
    for t in ["episodic", "semantic", "procedural"]:
        total += len(index["entries"].get(t, {}))
    index["stats"]["total_entries"] = total
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _gen_id():
    return "mem_" + uuid.uuid4().hex[:12]


def _ensure_dir(t):
    d = os.path.join(COLD_DIR, t)
    os.makedirs(d, exist_ok=True)
    return d


def evaluate_importance(content, mem_type, tags=None):
    """Evaluate importance score (0.0-1.0) of a memory entry."""
    base = DEFAULT_IMPORTANCE.get(mem_type, 0.5)
    
    boosts = 0.0
    content_lower = content.lower()
    
    # High importance signals
    high_signals = [
        "记住", "记住这个", "重要", "关键", "必须", "永远", 
        "correct", "important", "critical", "must", "always",
        "用户纠正", "错误", "教训",
    ]
    for sig in high_signals:
        if sig in content_lower:
            boosts += 0.15
    
    # Medium signals
    mid_signals = [
        "偏好", "喜欢", "讨厌", "prefer", "like", "hate",
        "习惯", "habit", "usually", "always",
        "目标", "goal", "plan", "打算",
    ]
    for sig in mid_signals:
        if sig in content_lower:
            boosts += 0.08
    
    # Tags boost
    if tags:
        high_tags = ["preference", "correction", "lesson", "constraint", "goal"]
        for t in tags:
            if t.lower() in high_tags:
                boosts += 0.1
    
    return min(1.0, base + boosts)


def add_entry(mem_type, content, tags=None, importance=None, source=None):
    """Add a new cold memory entry."""
    assert mem_type in ["episodic", "semantic", "procedural"], f"Invalid type: {mem_type}"
    
    entry_id = _gen_id()
    now = _now()
    
    if importance is None:
        importance = evaluate_importance(content, mem_type, tags)
    
    entry = {
        "id": entry_id,
        "type": mem_type,
        "content": content,
        "tags": tags or [],
        "importance": round(importance, 2),
        "ttl": TTL.get(mem_type),
        "access_count": 0,
        "created_at": now,
        "last_accessed": now,
        "source": source or "manual",
    }
    
    # Save to individual file
    d = _ensure_dir(mem_type)
    filepath = os.path.join(d, f"{entry_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    
    # Update index
    index = _load_index()
    index["entries"][mem_type][entry_id] = {
        "id": entry_id,
        "summary": content[:80] + ("..." if len(content) > 80 else ""),
        "tags": tags or [],
        "importance": round(importance, 2),
        "created_at": now,
    }
    _save_index(index)
    
    print(f"Added {mem_type}:{entry_id} (importance={round(importance,2)})")
    return entry_id


def search(query, mem_type=None, limit=5):
    """Search cold memory by keyword matching + importance ranking."""
    index = _load_index()
    results = []
    
    types = [mem_type] if mem_type else ["episodic", "semantic", "procedural"]
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    for t in types:
        for eid, meta in index["entries"].get(t, {}).items():
            # Load full entry for full-text search
            filepath = os.path.join(COLD_DIR, t, f"{eid}.json")
            if not os.path.exists(filepath):
                continue
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    entry = json.load(f)
            except:
                continue
            
            content = entry["content"].lower()
            
            # Scoring: exact phrase match > keyword matches > tag matches
            score = 0.0
            if query_lower in content:
                score += 10.0  # exact phrase match
            else:
                for term in query_terms:
                    if term in content:
                        score += 3.0
                    for tag in entry.get("tags", []):
                        if term in tag.lower():
                            score += 1.0
            
            if score > 0:
                results.append({
                    "id": eid,
                    "type": t,
                    "content": entry["content"][:150] + ("..." if len(entry["content"]) > 150 else ""),
                    "tags": entry.get("tags", []),
                    "importance": entry.get("importance", 0.5),
                    "score": round(score, 1),
                    "created_at": entry.get("created_at", ""),
                    "last_accessed": entry.get("last_accessed", ""),
                })
    
    # Sort: by score desc, then importance desc
    results.sort(key=lambda x: (-x["score"], -x["importance"]))
    
    # Update access count for top results
    for r in results[:limit]:
        touch_entry(r["id"], r["type"])
    
    return results[:limit]


def touch_entry(eid, mem_type):
    """Update access count and timestamp."""
    filepath = os.path.join(COLD_DIR, mem_type, f"{eid}.json")
    if not os.path.exists(filepath):
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            entry = json.load(f)
        entry["access_count"] = entry.get("access_count", 0) + 1
        entry["last_accessed"] = _now()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
        
        # Update index
        index = _load_index()
        if eid in index["entries"].get(mem_type, {}):
            pass  # summary stays same
        _save_index(index)
    except:
        pass


def list_entries(mem_type=None, limit=20):
    """List cold memory entries, sorted by importance desc."""
    index = _load_index()
    results = []
    
    types = [mem_type] if mem_type else ["episodic", "semantic", "procedural"]
    for t in types:
        for eid, meta in index["entries"].get(t, {}).items():
            results.append({
                "id": eid,
                "type": t,
                "summary": meta.get("summary", ""),
                "tags": meta.get("tags", []),
                "importance": meta.get("importance", 0.5),
                "created_at": meta.get("created_at", ""),
            })
    
    results.sort(key=lambda x: -x["importance"])
    return results[:limit]


def get_entry(eid, mem_type=None):
    """Get a single entry by ID."""
    types = [mem_type] if mem_type else ["episodic", "semantic", "procedural"]
    for t in types:
        filepath = os.path.join(COLD_DIR, t, f"{eid}.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


def archive_expired():
    """Archive (delete) expired episodic entries."""
    index = _load_index()
    now = datetime.now(timezone.utc)
    expired = []
    
    for eid, meta in list(index["entries"].get("episodic", {}).items()):
        created = datetime.fromisoformat(meta.get("created_at", ""))
        days_old = (now - created).days
        if days_old > TTL["episodic"]:
            expired.append(eid)
    
    for eid in expired:
        filepath = os.path.join(COLD_DIR, "episodic", f"{eid}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
        del index["entries"]["episodic"][eid]
        print(f"Expired: {eid}")
    
    if expired:
        _save_index(index)
    print(f"Archived {len(expired)} expired entries")
    return len(expired)


def migrate_markdown():
    """Migrate old .md files in cold/ to structured JSON."""
    migrated = 0
    old_file = os.path.join(COLD_DIR, "system-history.md")
    if os.path.exists(old_file):
        with open(old_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split by sections
        sections = re.split(r'\n## ', content)
        for sec in sections:
            if not sec.strip():
                continue
            lines = sec.strip().split('\n')
            section_title = lines[0].strip()
            
            # Determine type and tags
            mem_type = "procedural"
            tags = ["system-history"]
            if "API" in section_title or "Tool" in section_title:
                mem_type = "procedural"
            elif "Completed" in section_title:
                mem_type = "episodic"
                tags.append("completed")
            elif "Media" in section_title or "Search" in section_title:
                mem_type = "procedural"
                tags.append("reference")
            
            body = '\n'.join(lines[1:]).strip()
            if body:
                add_entry(mem_type, f"## {section_title}\n{body}", tags=tags, importance=0.4, source="migration")
                migrated += 1
        
        # Rename old file
        os.rename(old_file, old_file + ".bak")
        print(f"Migrated {migrated} entries from system-history.md")
    
    return migrated


def hot_archive(hot_entries_dict):
    """Archive hot memory entries to cold storage.
    
    Args:
        hot_entries_dict: dict of {entry_text: importance_score}
    """
    archived = 0
    for content, importance in hot_entries_dict.items():
        # Determine type by content
        mem_type = "episodic"
        tags = []
        
        if any(k in content.lower() for k in ["工具", "命令", "脚本", "配置", "tool", "command", "install", "setup"]):
            mem_type = "procedural"
            tags.append("config")
        elif any(k in content.lower() for k in ["偏好", "喜欢", "讨厌", "prefer", "communication", "沟通"]):
            mem_type = "semantic"
            tags.append("preference")
        elif any(k in content.lower() for k in ["教训", "lesson", "错误", "error", "修"]):
            mem_type = "semantic"
            tags.append("lesson")
        elif any(k in content.lower() for k in ["完成", "done", "completed", "fix"]):
            mem_type = "episodic"
            tags.append("completed")
        
        add_entry(mem_type, content, tags=tags, importance=importance, source="hot-archive")
        archived += 1
    
    return archived


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        if len(sys.argv) < 4:
            print("Usage: cold-memory.py add <type> <content> [--tags a,b,c] [--importance 0.8]")
            return
        mem_type = sys.argv[2]
        content = sys.argv[3]
        tags = None
        importance = None
        if "--tags" in sys.argv:
            idx = sys.argv.index("--tags")
            tags = sys.argv[idx + 1].split(",")
        if "--importance" in sys.argv:
            idx = sys.argv.index("--importance")
            importance = float(sys.argv[idx + 1])
        add_entry(mem_type, content, tags=tags, importance=importance)
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: cold-memory.py search <query> [--type episodic] [--limit 5]")
            return
        query = sys.argv[2]
        mem_type = None
        limit = 5
        if "--type" in sys.argv:
            idx = sys.argv.index("--type")
            mem_type = sys.argv[idx + 1]
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            limit = int(sys.argv[idx + 1])
        results = search(query, mem_type=mem_type, limit=limit)
        print(f"\nSearch results for '{query}':")
        print("-" * 60)
        if not results:
            print("  No results found.")
        for r in results:
            print(f"  [{r['type']}] {r['id']} (score={r['score']}, imp={r['importance']})")
            print(f"  {r['content']}")
            print(f"  tags: {r['tags']}")
            print()
    
    elif cmd == "list":
        mem_type = None
        limit = 20
        if "--type" in sys.argv:
            idx = sys.argv.index("--type")
            mem_type = sys.argv[idx + 1]
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            limit = int(sys.argv[idx + 1])
        results = list_entries(mem_type=mem_type, limit=limit)
        print(f"\nCold memory entries:")
        print("-" * 60)
        for r in results:
            print(f"  [{r['type']}] {r['id']} (imp={r['importance']})")
            print(f"  {r['summary']}")
            print(f"  tags: {r['tags']}")
            print()
    
    elif cmd == "get":
        if len(sys.argv) < 3:
            print("Usage: cold-memory.py get <id> [--type episodic]")
            return
        eid = sys.argv[2]
        mem_type = None
        if "--type" in sys.argv:
            idx = sys.argv.index("--type")
            mem_type = sys.argv[idx + 1]
        entry = get_entry(eid, mem_type=mem_type)
        if entry:
            print(json.dumps(entry, indent=2, ensure_ascii=False))
        else:
            print(f"Entry {eid} not found.")
    
    elif cmd == "archive":
        n = archive_expired()
        print(f"Expiry archive complete: {n} entries removed.")
    
    elif cmd == "migrate":
        n = migrate_markdown()
        print(f"Migration complete: {n} entries migrated.")
    
    elif cmd == "hot-archive":
        # Read from stdin: JSON object of {content: importance}
        data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
        if not data:
            print("Usage: echo '{\"content\": 0.8}' | python cold-memory.py hot-archive")
            data = json.loads(sys.stdin.read())
        n = hot_archive(data)
        print(f"Archived {n} entries from hot memory.")
    
    elif cmd == "health":
        """Health check: verify index integrity, file existence, report stats."""
        index = _load_index()
        issues = []
        total_files = 0
        total_size = 0
        
        for t in ["episodic", "semantic", "procedural"]:
            d = _ensure_dir(t)
            for eid in index["entries"].get(t, {}):
                fp = os.path.join(d, f"{eid}.json")
                if os.path.exists(fp):
                    total_files += 1
                    total_size += os.path.getsize(fp)
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            entry = json.load(f)
                        # Verify required fields
                        for field in ["id", "type", "content", "importance"]:
                            if field not in entry:
                                issues.append(f"{eid}: missing field '{field}'")
                    except json.JSONDecodeError:
                        issues.append(f"{eid}: corrupt JSON")
                else:
                    issues.append(f"{eid}: file missing")
        
        # Check for orphaned files (files not in index)
        for t in ["episodic", "semantic", "procedural"]:
            d = _ensure_dir(t)
            for fname in os.listdir(d):
                if fname.endswith(".json"):
                    eid = fname[:-5]
                    if eid not in index["entries"].get(t, {}):
                        issues.append(f"orphan: {t}/{fname}")
        
        print("=== Cold Memory Health Check ===")
        print(f"Status: {'❌ ISSUES' if issues else '✅ OK'}")
        print(f"Entries in index: {index['stats']['total_entries']}")
        print(f"Files on disk: {total_files}")
        print(f"Total size: {total_size:,} bytes")
        print(f"Index last updated: {index.get('last_updated', 'unknown')}")
        if issues:
            print(f"\nIssues ({len(issues)}):")
            for i in issues:
                print(f"  ⚠️  {i}")
        else:
            print(f"\n✅ No issues found.")
        return len(issues) == 0


if __name__ == "__main__":
    main()
