#!/usr/bin/env python3
"""
Log a URL to the current research session.
Logs to session_log.md (markdown table), scratchpad.json, and sources.csv.

Usage:
  python3 log_url.py <url> [OPTIONS]
  
Examples:
  python3 log_url.py https://github.com/user/repo --used --relevance 3
  python3 log_url.py https://arxiv.org/abs/1234.5678 --notes "Novel approach"
  python3 log_url.py https://example.com --skipped --notes "404 error"
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import os


def get_agent_core_dir() -> Path:
    return Path(os.environ.get("AGENT_CORE", Path.home() / ".agent-core"))


def get_local_agent_dir() -> Path:
    return Path.cwd() / ".agent"


def get_current_session() -> Optional[Dict[str, Any]]:
    """Load the current active session."""
    session_path = get_local_agent_dir() / "research" / "session.json"
    if session_path.exists():
        return json.loads(session_path.read_text())
    return None


def detect_source(url: str) -> str:
    """Auto-detect source type from URL."""
    domain = urlparse(url).netloc.lower()
    
    if "github.com" in domain:
        return "github"
    elif "arxiv.org" in domain:
        return "arxiv"
    elif "huggingface.co" in domain:
        return "huggingface"
    elif "medium.com" in domain or "blog" in domain:
        return "blog"
    elif "docs." in domain or "documentation" in url.lower():
        return "docs"
    elif "reddit.com" in domain:
        return "reddit"
    elif "news.ycombinator.com" in domain:
        return "hackernews"
    elif "twitter.com" in domain or "x.com" in domain:
        return "twitter"
    elif "youtube.com" in domain:
        return "youtube"
    else:
        return "web"


def extract_name(url: str, source: str) -> str:
    """Extract a name/title from URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    
    if source == "github" and "/" in path:
        parts = path.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    elif source == "arxiv":
        match = re.search(r'(\d{4}\.\d{4,5})', url)
        if match:
            return f"arxiv:{match.group(1)}"
    
    # Default: last path segment
    if path:
        return path.split("/")[-1][:50]
    return parsed.netloc


def relevance_to_stars(relevance: int) -> str:
    """Convert relevance score (0-3) to star string."""
    if relevance >= 3:
        return "★★★"
    elif relevance == 2:
        return "★★☆"
    elif relevance == 1:
        return "★☆☆"
    else:
        return "☆☆☆"


def ensure_scratchpad_keys(scratchpad: Dict) -> Dict:
    """Ensure scratchpad has all required keys."""
    defaults = {
        "urls_visited": [],
        "urls_used": [],
        "urls_skipped": [],
        "viral_candidates": [],
        "groundbreaker_candidates": [],
        "arxiv_papers": [],
        "findings": [],
        "checkpoints": []
    }
    for key, default in defaults.items():
        if key not in scratchpad:
            scratchpad[key] = default
    return scratchpad


def log_to_markdown(session: Dict, entry: Dict):
    """Append URL entry to session_log.md."""
    log_path = Path(session["paths"]["session_log"])
    
    if not log_path.exists():
        return
    
    content = log_path.read_text()
    
    # Build table row
    used_mark = "✓" if entry["used"] else ("✗" if entry.get("skipped") else "—")
    row = f"| {entry['time']} | {entry['source']} | {entry['url']} | {used_mark} | {entry['relevance_stars']} | {entry['notes']} |"
    
    # Find the URL table and append after header
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("|---") and i > 0 and "Source" in lines[i-1]:
            # Insert after the separator line
            lines.insert(i + 1, row)
            break
    
    log_path.write_text("\n".join(lines))


def log_to_scratchpad(session: Dict, entry: Dict):
    """Add URL entry to scratchpad.json."""
    scratchpad_path = Path(session["paths"]["scratchpad"])
    
    if not scratchpad_path.exists():
        return
    
    scratchpad = json.loads(scratchpad_path.read_text())
    scratchpad = ensure_scratchpad_keys(scratchpad)
    
    # Add URL entry
    url_entry = {
        "url": entry["url"],
        "source": entry["source"],
        "name": entry["name"],
        "timestamp": entry["timestamp"],
        "relevance": entry["relevance"],
        "notes": entry["notes"]
    }
    
    scratchpad["urls_visited"].append(url_entry)
    
    if entry["used"]:
        scratchpad["urls_used"].append(entry["url"])
    elif entry.get("skipped"):
        scratchpad["urls_skipped"].append(entry["url"])
    
    scratchpad["last_updated"] = entry["timestamp"]
    
    scratchpad_path.write_text(json.dumps(scratchpad, indent=2))


def log_to_csv(session: Dict, entry: Dict):
    """Append URL to sources.csv."""
    csv_path = Path(session["paths"]["sources"])
    
    if not csv_path.exists():
        return
    
    def escape(s):
        s = str(s)
        if "," in s or '"' in s or "\n" in s:
            return f'"{s.replace(chr(34), chr(34)+chr(34))}"'
        return s
    
    row = ",".join([
        escape(entry["name"]),
        escape(entry["url"]),
        escape(entry["source"]),
        escape(entry.get("filter", "")),
        escape(entry.get("stars", "")),
        escape(entry["timestamp"][:10]),
        escape(entry["relevance"]),
        escape("yes" if entry["used"] else "no"),
        escape(entry["notes"])
    ])
    
    with open(csv_path, "a") as f:
        f.write(row + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Log a URL to the current research session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://github.com/user/repo --used --relevance 3
  %(prog)s https://arxiv.org/abs/2401.12345 --notes "Great paper"
  %(prog)s https://example.com --skipped --notes "Outdated"
        """
    )
    parser.add_argument("url", help="URL to log")
    parser.add_argument("--source", "-s",
                        choices=["github", "arxiv", "huggingface", "blog", "docs", 
                                "reddit", "hackernews", "twitter", "youtube", "web"],
                        help="Source type (auto-detected if not specified)")
    parser.add_argument("--name", "-n", help="Name/title (auto-extracted if not specified)")
    parser.add_argument("--used", "-u", action="store_true", help="Mark as used in final output")
    parser.add_argument("--skipped", action="store_true", help="Mark as visited but skipped")
    parser.add_argument("--relevance", "-r", type=int, choices=[0, 1, 2, 3], default=2,
                        help="Relevance score: 0=none, 1=low, 2=medium, 3=high (default: 2)")
    parser.add_argument("--notes", help="Notes about this URL")
    parser.add_argument("--filter", "-f", choices=["viral", "groundbreaker"],
                        help="Which search filter found this")
    parser.add_argument("--stars", type=int, help="GitHub stars (if applicable)")
    
    args = parser.parse_args()
    
    # Get current session
    session = get_current_session()
    if not session:
        print("❌ No active session found. Run init_session.py first.")
        return 1
    
    # Build entry
    now = datetime.now()
    source = args.source or detect_source(args.url)
    name = args.name or extract_name(args.url, source)
    
    entry = {
        "url": args.url,
        "source": source,
        "name": name,
        "timestamp": now.isoformat(),
        "time": now.strftime("%H:%M"),
        "used": args.used,
        "skipped": args.skipped,
        "relevance": args.relevance,
        "relevance_stars": relevance_to_stars(args.relevance),
        "notes": args.notes or "",
        "filter": args.filter or "",
        "stars": args.stars
    }
    
    # Log to all outputs
    log_to_markdown(session, entry)
    log_to_scratchpad(session, entry)
    log_to_csv(session, entry)
    
    # Output confirmation
    used_str = "✓ USED" if args.used else ("✗ SKIPPED" if args.skipped else "○ LOGGED")
    print(f"{used_str}: [{source}] {name}")
    print(f"   {args.url}")
    if args.notes:
        print(f"   Notes: {args.notes}")
    
    return 0


if __name__ == "__main__":
    exit(main())
