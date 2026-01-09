#!/usr/bin/env python3
"""
Archive a completed research session.
- Logs ALL URLs (used and unused)
- Extracts learnings to memory
- Syncs to global storage
- Updates session index

Usage:
  python3 archive_session.py
  python3 archive_session.py --no-extract    # Skip learning extraction
  python3 archive_session.py --keep-local    # Don't clean local workspace
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import os


def get_agent_core_dir() -> Path:
    return Path(os.environ.get("AGENT_CORE", Path.home() / ".agent-core"))


def get_local_agent_dir() -> Path:
    return Path.cwd() / ".agent"


def get_current_session() -> Optional[Dict]:
    """Load current session metadata."""
    local_dir = get_local_agent_dir() / "research"
    session_file = local_dir / "session.json"
    if session_file.exists():
        try:
            return json.loads(session_file.read_text())
        except json.JSONDecodeError:
            return None
    return None


def parse_scratchpad(session: Dict) -> Dict:
    """Load and parse scratchpad data."""
    scratchpad_path = Path(session["paths"]["scratchpad"])
    if scratchpad_path.exists():
        try:
            return json.loads(scratchpad_path.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def count_urls(scratchpad: Dict) -> Dict:
    """Count URL statistics."""
    return {
        "total": len(scratchpad.get("urls_visited", [])),
        "used": len(scratchpad.get("urls_used", [])),
        "skipped": len(scratchpad.get("urls_skipped", []))
    }


def extract_learnings(session: Dict, scratchpad: Dict) -> List[Dict]:
    """Extract key learnings from the session."""
    learnings = []
    
    # From viral candidates
    for item in scratchpad.get("viral_candidates", []):
        if isinstance(item, dict):
            learnings.append({
                "type": "tool",
                "name": item.get("name", "Unknown"),
                "url": item.get("url", ""),
                "insight": f"High-adoption: {item.get('why', item.get('notes', 'well-maintained'))}"
            })
    
    # From groundbreaker candidates
    for item in scratchpad.get("groundbreaker_candidates", []):
        if isinstance(item, dict):
            learnings.append({
                "type": "innovation",
                "name": item.get("name", "Unknown"),
                "url": item.get("url", ""),
                "insight": f"Novel: {item.get('novel', item.get('why', item.get('notes', 'emerging')))}"
            })
    
    # From arxiv papers
    for item in scratchpad.get("arxiv_papers", []):
        if isinstance(item, dict):
            learnings.append({
                "type": "paper",
                "name": item.get("title", item.get("name", "Unknown")),
                "url": item.get("url", ""),
                "insight": item.get("insight", item.get("notes", "Research finding"))
            })
    
    # From high-relevance URLs
    for item in scratchpad.get("urls_visited", []):
        if isinstance(item, dict) and item.get("relevance", 0) >= 3:
            if item.get("url") not in [l.get("url") for l in learnings]:
                learnings.append({
                    "type": "resource",
                    "name": item.get("name", item.get("url", "Unknown")),
                    "url": item.get("url", ""),
                    "insight": item.get("notes", "High relevance resource")
                })
    
    return learnings


def update_learnings_memory(session: Dict, learnings: List[Dict]) -> int:
    """Append learnings to global memory."""
    if not learnings:
        return 0
    
    memory_file = get_agent_core_dir() / "memory" / "learnings.md"
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create file if doesn't exist
    if not memory_file.exists():
        memory_file.write_text("# Research Learnings\n\nAuto-extracted from archived sessions.\n\n---\n\n")
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    entry = f"\n## {date} — {session['topic']}\n"
    entry += f"Session: `{session['session_id']}`\n\n"
    
    for l in learnings:
        if l["url"]:
            entry += f"- **{l['type'].title()}**: [{l['name']}]({l['url']}) — {l['insight']}\n"
        else:
            entry += f"- **{l['type'].title()}**: {l['name']} — {l['insight']}\n"
    
    entry += "\n---\n"
    
    with open(memory_file, "a") as f:
        f.write(entry)
    
    return len(learnings)


def update_session_index(session: Dict, duration_min: float, url_stats: Dict, key_finding: str):
    """Update global session index."""
    index_file = get_agent_core_dir() / "sessions" / "index.md"
    index_file.parent.mkdir(parents=True, exist_ok=True)
    
    if not index_file.exists():
        index_file.write_text(
            "# Session Index\n\n"
            "| Date | Session ID | Topic | Workflow | Duration | URLs | Key Finding |\n"
            "|------|------------|-------|----------|----------|------|-------------|\n"
        )
    
    date = datetime.now().strftime("%Y-%m-%d")
    url_summary = f"{url_stats['used']}/{url_stats['total']}"
    
    # Truncate key finding
    if len(key_finding) > 40:
        key_finding = key_finding[:37] + "..."
    
    row = f"| {date} | {session['session_id'][:25]}... | {session['topic'][:20]} | {session['workflow']} | {duration_min:.0f}m | {url_summary} | {key_finding} |\n"
    
    with open(index_file, "a") as f:
        f.write(row)


def generate_archive_report(session: Dict, scratchpad: Dict, url_stats: Dict, duration_min: float) -> str:
    """Generate comprehensive archive report."""
    now = datetime.now()
    
    report = f"""# Session Archive: {session['topic']}

## Metadata

| Field | Value |
|-------|-------|
| Session ID | `{session['session_id']}` |
| Workflow | {session['workflow']} |
| Environment | {session['environment']} |
| Started | {session['started']} |
| Archived | {now.isoformat()} |
| Duration | {duration_min:.1f} minutes |

---

## URL Statistics

| Metric | Count |
|--------|-------|
| Total URLs visited | {url_stats['total']} |
| URLs used in output | {url_stats['used']} |
| URLs skipped | {url_stats['skipped']} |

---

## Search Queries Used

### Viral Filter
```
{session['queries']['viral']['github']}
```

### Groundbreaker Filter
```
{session['queries']['groundbreaker']['github']}
```

---

## Complete URL Log

### URLs Used

"""
    
    for url in scratchpad.get("urls_used", []):
        report += f"- {url}\n"
    
    if not scratchpad.get("urls_used"):
        report += "_No URLs marked as used_\n"
    
    report += "\n### All URLs Visited\n\n"
    
    for entry in scratchpad.get("urls_visited", []):
        if isinstance(entry, dict):
            url = entry.get("url", "")
            source = entry.get("source", "web")
            notes = entry.get("notes", "")
            report += f"- [{source}] {url}"
            if notes:
                report += f" — {notes}"
            report += "\n"
        else:
            report += f"- {entry}\n"
    
    if not scratchpad.get("urls_visited"):
        report += "_No URLs logged_\n"
    
    report += f"""

---

## To Continue This Research

```bash
python3 init_session.py --continue {session['session_id']}
```

---

*Archived: {now.strftime("%Y-%m-%d %H:%M")}*
"""
    
    return report


def archive_session(extract_learnings_flag: bool = True, keep_local: bool = False) -> bool:
    """Main archive function."""
    session = get_current_session()
    if not session:
        print("❌ No active session found in .agent/research/")
        print("   Run init_session.py to start a session first.")
        return False
    
    local_dir = get_local_agent_dir() / "research"
    global_dir = get_agent_core_dir() / "sessions" / session["session_id"]
    
    global_dir.mkdir(parents=True, exist_ok=True)
    
    # Load scratchpad
    scratchpad = parse_scratchpad(session)
    url_stats = count_urls(scratchpad)
    
    # Calculate duration
    try:
        started = datetime.fromisoformat(session["started"])
        duration_min = (datetime.now() - started).total_seconds() / 60
    except:
        duration_min = 0
    
    # Extract learnings
    learnings_count = 0
    if extract_learnings_flag:
        learnings = extract_learnings(session, scratchpad)
        if learnings:
            learnings_count = update_learnings_memory(session, learnings)
    
    # Get key finding for index
    key_finding = "See report"
    if scratchpad.get("viral_candidates"):
        first = scratchpad["viral_candidates"][0]
        if isinstance(first, dict):
            key_finding = first.get("name", "See report")
    elif scratchpad.get("urls_used"):
        key_finding = f"{url_stats['used']} URLs used"
    
    # Update session metadata
    session["status"] = "archived"
    session["archived_at"] = datetime.now().isoformat()
    session["duration_minutes"] = duration_min
    session["stats"]["urls_visited"] = url_stats["total"]
    session["stats"]["urls_used"] = url_stats["used"]
    
    # Generate archive report
    archive_report = generate_archive_report(session, scratchpad, url_stats, duration_min)
    archive_path = local_dir / "session_archive.md"
    archive_path.write_text(archive_report)
    
    # Save updated session metadata
    (local_dir / "session.json").write_text(json.dumps(session, indent=2))
    
    # Copy all files to global
    for item in local_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, global_dir / item.name)
        elif item.is_dir():
            dest = global_dir / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
    
    # Update session index
    update_session_index(session, duration_min, url_stats, key_finding)
    
    # Clean local workspace
    if not keep_local:
        for item in local_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        
        # Leave breadcrumb
        (local_dir / ".last_session").write_text(session["session_id"])
    
    # Output summary
    print(f"\n✅ Session archived: {session['session_id']}")
    print(f"📁 Location: {global_dir}")
    print(f"📝 Learnings extracted: {learnings_count}")
    print(f"🔗 URLs logged: {url_stats['total']} total")
    print(f"⏱️  Duration: {duration_min:.1f} minutes")
    print()
    print(f"To revisit: /recall {session['topic']}")
    print(f"To continue: --continue {session['session_id']}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Archive completed research session",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--no-extract", action="store_true",
                        help="Skip extracting learnings to memory")
    parser.add_argument("--keep-local", action="store_true",
                        help="Keep local workspace (don't clean)")
    
    args = parser.parse_args()
    
    success = archive_session(
        extract_learnings_flag=not args.no_extract,
        keep_local=args.keep_local
    )
    
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
