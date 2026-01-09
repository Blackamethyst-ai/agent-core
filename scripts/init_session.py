#!/usr/bin/env python3
"""
Initialize a new agent session with proper workspace structure.
Supports CLI, Antigravity (VSCode OSS), and web environments.

Usage:
  python3 init_session.py <topic> [--workflow TYPE] [--env ENV]
  python3 init_session.py --continue SESSION_ID
  python3 init_session.py --list
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List


def get_agent_core_dir() -> Path:
    return Path(os.environ.get("AGENT_CORE", Path.home() / ".agent-core"))


def get_local_agent_dir() -> Path:
    return Path.cwd() / ".agent"


def detect_environment() -> str:
    if os.environ.get("VSCODE_PID") or os.environ.get("TERM_PROGRAM") == "vscode":
        return "antigravity"
    if os.environ.get("CLAUDE_WEB_SESSION"):
        return "web"
    return "cli"


def load_config() -> Dict[str, Any]:
    config_path = get_agent_core_dir() / "config.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except json.JSONDecodeError:
            pass
    return {"defaults": {"auto_accept": True}, "research": {}}


def generate_session_id(topic: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    topic_hash = hashlib.md5(topic.encode()).hexdigest()[:6]
    safe_topic = "".join(c if c.isalnum() or c == "-" else "-" for c in topic.lower())
    safe_topic = safe_topic[:20].strip("-")
    return f"{safe_topic}-{timestamp}-{topic_hash}"


def create_search_queries(topic: str, config: Dict) -> Dict:
    today = datetime.now()
    research = config.get("research", {})
    viral = research.get("viral_filter", {"min_stars": 500, "recency_days": 30})
    ground = research.get("groundbreaker_filter", {"min_stars": 10, "max_stars": 200, "recency_days": 90})
    
    viral_cutoff = (today - timedelta(days=viral.get("recency_days", 30))).strftime("%Y-%m-%d")
    ground_cutoff = (today - timedelta(days=ground.get("recency_days", 90))).strftime("%Y-%m-%d")
    
    return {
        "viral": {
            "github": f"{topic} stars:>{viral.get('min_stars', 500)} pushed:>{viral_cutoff}",
            "description": f"High-adoption (>{viral.get('min_stars', 500)} stars)"
        },
        "groundbreaker": {
            "github": f"{topic} stars:{ground.get('min_stars', 10)}..{ground.get('max_stars', 200)} created:>{ground_cutoff}",
            "arxiv": topic,
            "description": f"Novel ({ground.get('min_stars', 10)}-{ground.get('max_stars', 200)} stars)"
        }
    }


def create_session_log(session: Dict) -> str:
    """Generate session log markdown content."""
    return f"""# Research Session: {session['topic']}

**Session ID:** `{session['session_id']}`
**Workflow:** {session['workflow']}
**Environment:** {session['environment']}
**Started:** {session['started']}
**Status:** {session['status']}

---

## Search Queries

### Viral Filter (High Adoption)
```
{session['queries']['viral']['github']}
```
{session['queries']['viral']['description']}

### Groundbreaker Filter (Novel/Emerging)
```
{session['queries']['groundbreaker']['github']}
```
{session['queries']['groundbreaker']['description']}

---

## URLs Visited

> Log ALL URLs here - even if not used in final output

| Time | Source | URL | Used | Relevance | Notes |
|------|--------|-----|------|-----------|-------|

---

## Key Findings

### Viral Candidates

_High-adoption frameworks..._

### Groundbreaker Candidates

_Novel/emerging frameworks..._

### arXiv Papers

_Recent research..._

---

## Checkpoints

| Time | URLs Visited | Findings | Notes |
|------|--------------|----------|-------|

---

## Session Notes

_Free-form notes during research..._

"""


def create_scratchpad(session: Dict) -> Dict:
    """Generate scratchpad JSON structure with ALL required keys."""
    return {
        "session_id": session["session_id"],
        "topic": session["topic"],
        "workflow": session["workflow"],
        "environment": session["environment"],
        "started": session["started"],
        # Research findings
        "viral_candidates": [],
        "groundbreaker_candidates": [],
        "arxiv_papers": [],
        # URL tracking (ALL THREE REQUIRED)
        "urls_visited": [],
        "urls_used": [],
        "urls_skipped": [],
        # Progress tracking
        "findings": [],
        "checkpoints": [],
        "last_checkpoint": None,
        "last_updated": session["started"]
    }


def init_session(topic: str, workflow: str = "research", env: Optional[str] = None) -> Dict:
    config = load_config()
    env = env or detect_environment()
    session_id = generate_session_id(topic)
    timestamp = datetime.now().isoformat()
    safe_topic = "".join(c if c.isalnum() or c == "-" else "-" for c in topic.lower())[:30].strip("-")
    
    local_dir = get_local_agent_dir() / "research"
    global_dir = get_agent_core_dir() / "sessions" / session_id
    
    local_dir.mkdir(parents=True, exist_ok=True)
    global_dir.mkdir(parents=True, exist_ok=True)
    
    session = {
        "session_id": session_id,
        "topic": topic,
        "safe_topic": safe_topic,
        "workflow": workflow,
        "environment": env,
        "started": timestamp,
        "status": "active",
        "queries": create_search_queries(topic, config),
        "paths": {
            "local": str(local_dir),
            "global": str(global_dir),
            "session_log": str(local_dir / "session_log.md"),
            "scratchpad": str(local_dir / "scratchpad.json"),
            "report": str(local_dir / f"{safe_topic}_report.md"),
            "sources": str(local_dir / f"{safe_topic}_sources.csv")
        },
        "stats": {
            "urls_visited": 0,
            "urls_used": 0,
            "checkpoints": 0,
            "last_sync": None
        }
    }
    
    # Create session log
    Path(session["paths"]["session_log"]).write_text(create_session_log(session))
    
    # Create scratchpad with COMPLETE schema
    scratchpad = create_scratchpad(session)
    Path(session["paths"]["scratchpad"]).write_text(json.dumps(scratchpad, indent=2))
    
    # Create sources CSV
    Path(session["paths"]["sources"]).write_text(
        "name,url,type,filter,stars,date,relevance,used,notes\n"
    )
    
    # Save session metadata (local + global)
    (local_dir / "session.json").write_text(json.dumps(session, indent=2))
    (global_dir / "session.json").write_text(json.dumps(session, indent=2))
    
    return session


def load_session(session_id: str) -> Dict:
    """Load an existing session to continue."""
    global_dir = get_agent_core_dir() / "sessions" / session_id
    metadata_path = global_dir / "session.json"
    
    if not metadata_path.exists():
        raise FileNotFoundError(f"Session not found: {session_id}")
    
    session = json.loads(metadata_path.read_text())
    session["status"] = "resumed"
    session["resumed_at"] = datetime.now().isoformat()
    
    local_dir = get_local_agent_dir() / "research"
    local_dir.mkdir(parents=True, exist_ok=True)
    
    for file in global_dir.iterdir():
        if file.is_file():
            (local_dir / file.name).write_bytes(file.read_bytes())
    
    session["paths"]["local"] = str(local_dir)
    (local_dir / "session.json").write_text(json.dumps(session, indent=2))
    
    return session


def list_sessions(limit: int = 10) -> List[Dict]:
    """List recent sessions."""
    sessions_dir = get_agent_core_dir() / "sessions"
    if not sessions_dir.exists():
        return []
    
    sessions = []
    for d in sorted(sessions_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if d.is_dir() and (d / "session.json").exists():
            try:
                meta = json.loads((d / "session.json").read_text())
                sessions.append({
                    "id": meta.get("session_id", d.name),
                    "topic": meta.get("topic", "Unknown"),
                    "workflow": meta.get("workflow", "research"),
                    "status": meta.get("status", "unknown"),
                    "started": meta.get("started", "")
                })
            except json.JSONDecodeError:
                pass
        if len(sessions) >= limit:
            break
    
    return sessions


def main():
    parser = argparse.ArgumentParser(
        description="Initialize agent research session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "transformer architectures"
  %(prog)s "react hooks" --workflow innovation-scout
  %(prog)s --continue session-id-here
  %(prog)s --list
        """
    )
    parser.add_argument("topic", nargs="?", help="Research topic")
    parser.add_argument("--workflow", "-w", default="research",
                        choices=["research", "innovation-scout", "deep-research"],
                        help="Workflow type (default: research)")
    parser.add_argument("--env", "-e", choices=["cli", "antigravity", "web"],
                        help="Override environment detection")
    parser.add_argument("--continue", "-c", dest="continue_session", metavar="ID",
                        help="Continue existing session by ID")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List recent sessions")
    
    args = parser.parse_args()
    
    # List sessions
    if args.list:
        sessions = list_sessions()
        if not sessions:
            print("No sessions found.")
            return
        print("\nRecent Sessions:")
        print("-" * 70)
        for s in sessions:
            status_icon = "🟢" if s["status"] == "active" else "📁"
            print(f"{status_icon} {s['id']}")
            print(f"   Topic: {s['topic']} | Workflow: {s['workflow']}")
            print(f"   Started: {s['started']}")
            print()
        return
    
    # Continue existing session
    if args.continue_session:
        try:
            session = load_session(args.continue_session)
            print(f"✅ Session resumed: {session['session_id']}")
            print(f"   Topic: {session['topic']}")
            print(f"   Local: {session['paths']['local']}")
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)
        return
    
    # New session requires topic
    if not args.topic:
        parser.error("Topic is required (or use --continue SESSION_ID or --list)")
    
    try:
        session = init_session(
            topic=args.topic,
            workflow=args.workflow,
            env=args.env
        )
        
        print(f"\n✅ Session initialized: {session['session_id']}")
        print(f"   Topic: {session['topic']}")
        print(f"   Workflow: {session['workflow']}")
        print(f"   Environment: {session['environment']}")
        print(f"   Local: {session['paths']['local']}")
        print()
        print("📝 Files created:")
        print("   • session_log.md   (narrative + URL table)")
        print("   • scratchpad.json  (machine-readable state)")
        print("   • sources.csv      (raw data export)")
        print()
        print("🔍 Search queries:")
        print(f"   Viral: {session['queries']['viral']['github']}")
        print(f"   Groundbreaker: {session['queries']['groundbreaker']['github']}")
        print()
        print("💡 Next steps:")
        print("   1. Research with the queries above")
        print("   2. Log URLs: agent-log <url> --used --relevance 3")
        print("   3. Archive when done: agent-archive")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
