#!/usr/bin/env python3
"""
Sync session state between CLI, Antigravity, and web environments.
All environments share ~/.agent-core/ as the sync point.

Usage:
  python3 sync_environments.py status     # Show sync status
  python3 sync_environments.py push       # Push local → global
  python3 sync_environments.py pull       # Pull global → local
  python3 sync_environments.py pull ID    # Pull specific session
"""

import argparse
import json
import shutil
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List


def get_agent_core_dir() -> Path:
    return Path(os.environ.get("AGENT_CORE", Path.home() / ".agent-core"))


def get_local_agent_dir() -> Path:
    return Path.cwd() / ".agent"


def detect_environment() -> str:
    """Detect current environment."""
    if os.environ.get("VSCODE_PID") or os.environ.get("TERM_PROGRAM") == "vscode":
        return "antigravity"
    if os.environ.get("CLAUDE_WEB_SESSION"):
        return "web"
    return "cli"


def get_current_session() -> Optional[Dict]:
    """Load the current active session."""
    local_dir = get_local_agent_dir() / "research"
    session_file = local_dir / "session.json"
    if session_file.exists():
        try:
            return json.loads(session_file.read_text())
        except json.JSONDecodeError:
            return None
    return None


def list_global_sessions(limit: int = 10) -> List[Dict]:
    """List sessions in global storage."""
    sessions_dir = get_agent_core_dir() / "sessions"
    if not sessions_dir.exists():
        return []
    
    sessions = []
    for session_dir in sorted(sessions_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if session_dir.is_dir() and session_dir.name != "index.md":
            metadata_path = session_dir / "session.json"
            if metadata_path.exists():
                try:
                    meta = json.loads(metadata_path.read_text())
                    meta["_path"] = str(session_dir)
                    meta["_mtime"] = datetime.fromtimestamp(session_dir.stat().st_mtime).isoformat()
                    sessions.append(meta)
                except json.JSONDecodeError:
                    pass
        if len(sessions) >= limit:
            break
    
    return sessions


def push_session() -> bool:
    """Push local session state to global storage."""
    session = get_current_session()
    if not session:
        print("❌ No active session found in .agent/research/")
        print("   Run init_session.py to start a session first.")
        return False
    
    local_dir = get_local_agent_dir() / "research"
    global_dir = get_agent_core_dir() / "sessions" / session["session_id"]
    
    global_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files
    files_synced = []
    for item in local_dir.iterdir():
        if item.is_file():
            dest = global_dir / item.name
            shutil.copy2(item, dest)
            files_synced.append(item.name)
        elif item.is_dir():
            dest = global_dir / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            files_synced.append(f"{item.name}/")
    
    # Update sync timestamp
    session["stats"]["last_sync"] = datetime.now().isoformat()
    session["stats"]["sync_direction"] = "push"
    session["stats"]["sync_env"] = detect_environment()
    
    # Save updated metadata
    (local_dir / "session.json").write_text(json.dumps(session, indent=2))
    (global_dir / "session.json").write_text(json.dumps(session, indent=2))
    
    print(f"✅ Pushed session: {session['session_id']}")
    print(f"   Files synced: {', '.join(files_synced)}")
    print(f"   Destination: {global_dir}")
    return True


def pull_session(session_id: Optional[str] = None) -> bool:
    """Pull session state from global storage to local."""
    global_base = get_agent_core_dir() / "sessions"
    
    if session_id:
        global_dir = global_base / session_id
    else:
        # Find most recent session
        sessions = list_global_sessions(limit=1)
        if not sessions:
            print("❌ No sessions found in global storage")
            return False
        session_id = sessions[0]["session_id"]
        global_dir = global_base / session_id
    
    if not global_dir.exists():
        print(f"❌ Session not found: {session_id}")
        return False
    
    local_dir = get_local_agent_dir() / "research"
    local_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files
    files_synced = []
    for item in global_dir.iterdir():
        if item.is_file():
            dest = local_dir / item.name
            shutil.copy2(item, dest)
            files_synced.append(item.name)
        elif item.is_dir():
            dest = local_dir / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            files_synced.append(f"{item.name}/")
    
    # Update sync timestamp in local copy
    session_path = local_dir / "session.json"
    if session_path.exists():
        session = json.loads(session_path.read_text())
        session["stats"]["last_sync"] = datetime.now().isoformat()
        session["stats"]["sync_direction"] = "pull"
        session["stats"]["sync_env"] = detect_environment()
        session_path.write_text(json.dumps(session, indent=2))
        
        print(f"✅ Pulled session: {session['session_id']}")
        print(f"   Topic: {session['topic']}")
    else:
        print(f"✅ Pulled session: {session_id}")
    
    print(f"   Files synced: {', '.join(files_synced)}")
    print(f"   Destination: {local_dir}")
    return True


def show_status():
    """Show comprehensive sync status."""
    env = detect_environment()
    agent_core = get_agent_core_dir()
    local_agent = get_local_agent_dir()
    local_session = get_current_session()
    
    print()
    print("📊 Sync Status")
    print("=" * 50)
    print()
    
    # Environment
    env_icons = {"cli": "🖥️ ", "antigravity": "🚀", "web": "🌐"}
    print(f"Environment: {env_icons.get(env, '❓')} {env.upper()}")
    print()
    
    # Local session
    print(f"📁 Local ({local_agent / 'research'}):")
    if local_session:
        status_icon = "🟢" if local_session.get("status") == "active" else "🟡"
        print(f"   {status_icon} {local_session['session_id']}")
        print(f"      Topic: {local_session['topic']}")
        print(f"      Status: {local_session.get('status', 'unknown')}")
        
        last_sync = local_session.get("stats", {}).get("last_sync")
        if last_sync:
            sync_dir = local_session.get("stats", {}).get("sync_direction", "?")
            print(f"      Last sync: {last_sync} ({sync_dir})")
        else:
            print(f"      Last sync: Not yet synced")
        
        # Count URLs from scratchpad
        scratchpad_path = local_agent / "research" / "scratchpad.json"
        if scratchpad_path.exists():
            try:
                sp = json.loads(scratchpad_path.read_text())
                urls = len(sp.get("urls_visited", []))
                used = len(sp.get("urls_used", []))
                print(f"      URLs: {urls} visited, {used} used")
            except:
                pass
    else:
        print("   No active session")
    print()
    
    # Global sessions
    print(f"🌐 Global ({agent_core / 'sessions'}):")
    sessions = list_global_sessions(limit=5)
    if sessions:
        print(f"   Total sessions: {len(list((agent_core / 'sessions').iterdir())) if (agent_core / 'sessions').exists() else 0}")
        print("   Recent sessions:")
        for s in sessions:
            status = s.get("status", "unknown")
            icon = "🟢" if status == "active" else "📁"
            print(f"     - {s['session_id']}: {s['topic']}")
    else:
        print("   No sessions found")
    print()
    
    # Memory
    print(f"💾 Memory ({agent_core / 'memory'}):")
    memory_dir = agent_core / "memory"
    if memory_dir.exists():
        for mem_file in sorted(memory_dir.glob("*.md")):
            try:
                lines = len(mem_file.read_text().splitlines())
                print(f"   {mem_file.name}: {lines} lines")
            except:
                print(f"   {mem_file.name}")
    else:
        print("   Not initialized")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Sync agent sessions between environments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status              # Show sync status
  %(prog)s push                # Push local to global
  %(prog)s pull                # Pull latest from global
  %(prog)s pull SESSION_ID     # Pull specific session
        """
    )
    parser.add_argument("command", nargs="?", default="status",
                        choices=["status", "push", "pull"],
                        help="Command (default: status)")
    parser.add_argument("session_id", nargs="?",
                        help="Session ID (for pull)")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Force overwrite without confirmation")
    
    args = parser.parse_args()
    
    if args.command == "status":
        show_status()
    elif args.command == "push":
        push_session()
    elif args.command == "pull":
        pull_session(args.session_id)


if __name__ == "__main__":
    main()
