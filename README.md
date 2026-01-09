# Agent Core

Unified research orchestration for CLI, Antigravity (VSCode OSS), and web environments.

Built for agentic workflows — parallel sessions, auto-accept, plan-first execution.

## Features

- 🔍 **Innovation Scout** — Dual-filter GitHub + arXiv research
- 📝 **URL Logging** — Track every URL visited (used or not)
- 🔄 **Cross-Environment Sync** — CLI ↔ Antigravity ↔ Web
- 🧠 **Long-Term Memory** — Auto-extract learnings from sessions
- 📊 **Session Management** — Archive, resume, review past research

## Quick Start

```bash
# Install
git clone https://github.com/Blackamethyst-ai/agent-core.git
cd agent-core
chmod +x setup.sh
./setup.sh

# Add aliases to ~/.zshrc (copy from setup output)
source ~/.zshrc

# Start researching
agent-init "your topic"
agent-log https://github.com/user/repo --used --relevance 3
agent-sync status
agent-archive
```

## Commands

| Command | Description |
|---------|-------------|
| `agent-init "topic"` | Start new research session |
| `agent-init --list` | List past sessions |
| `agent-init --continue ID` | Resume archived session |
| `agent-log <url> --used` | Log URL as used |
| `agent-log <url> --skipped` | Log URL as checked but skipped |
| `agent-sync status` | Show current state |
| `agent-sync push` | Push local → global |
| `agent-sync pull` | Pull global → local |
| `agent-archive` | Close session, extract learnings |

## Architecture

```
~/.agent-core/                    # Global (permanent)
├── config.json                   # Settings
├── sessions/                     # Archived sessions
│   ├── index.md                  # History
│   └── [session-id]/             # Each session
├── memory/
│   ├── global.md                 # Permanent facts
│   └── learnings.md              # Auto-extracted insights
├── workflows/                    # Research workflows
├── scripts/                      # Python tools
└── assets/                       # Templates

.agent/                           # Project-local
├── research/                     # Current session
│   ├── session.json
│   ├── session_log.md            # URL table + narrative
│   ├── scratchpad.json           # Machine-readable
│   └── [topic]_sources.csv       # Export
└── memory.md                     # Project memory
```

## Workflows

### Innovation Scout

```bash
agent-init "topic" --workflow innovation-scout
```

- **Viral Filter**: `stars:>500 pushed:>30days` — Production-ready
- **Groundbreaker Filter**: `stars:10..200 created:>90days` — Novel/emerging

### Deep Research

```bash
agent-init "topic" --workflow deep-research
```

Multi-source investigation with artifact extraction.

## Antigravity Shortcuts

| Key | Action |
|-----|--------|
| ⌘E | Switch to Agent Manager |
| ⌘L | Code with Agent |
| ⌘I | Edit code inline |

## Parallel Sessions

```
Tab 1: Planning/Orchestration
Tab 2-3: Feature development
Tab 4: Testing
Tab 5: Documentation
```

## Updating

```bash
cd ~/path/to/agent-core
git pull
./setup.sh --update
```

## Requirements

- Python 3.9+
- macOS / Linux
- Optional: Claude Code CLI, Antigravity IDE

## License

MIT

## Author

Dico Angelo / [Blackamethyst AI](https://github.com/Blackamethyst-ai)
