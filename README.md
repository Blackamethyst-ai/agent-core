<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:4a0080,100:00d9ff&height=200&section=header&text=Agent%20Core&fontSize=60&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Unified%20Research%20Orchestration&descSize=20&descAlignY=55" />
</p>

<p align="center">
  <strong>Agentic research workflows for CLI, Antigravity, and web environments</strong>
</p>

<p align="center">
  <em>"Let the invention be hidden in your vision"</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.1.0-00d9ff?style=for-the-badge" alt="Version" />
  <img src="https://img.shields.io/badge/Python-3.9+-4a0080?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge" alt="Status" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-CLI-1a1a2e?style=for-the-badge" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Antigravity-VSCode_OSS-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" alt="Antigravity" />
  <img src="https://img.shields.io/badge/Cross_Environment-Sync-00d9ff?style=for-the-badge" alt="Sync" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Metaventions_AI-Architected_Intelligence-1a1a2e?style=for-the-badge" alt="Metaventions AI" />
</p>

---

## Summary | Features | Quick Start | Commands | Architecture | Workflows

---

## What's New in v2.1 (January 2026)

| Feature | Description |
|---------|-------------|
| **ResearchGravity v3.3** | YouTube channel research integration |
| **Ecosystem Registry** | 6 projects now cross-referenced |
| **Session Lineage** | Full provenance tracking across projects |

---

## Summary

**Agent Core** is a unified research orchestration framework designed for agentic workflows. It enables parallel sessions, auto-accept execution, and plan-first development across multiple environments.

### Key Capabilities

- **Innovation Scout** — Dual-filter GitHub + arXiv research (Viral + Groundbreaker)
- **URL Logging** — Track every URL visited with relevance scoring
- **Cross-Environment Sync** — Seamless CLI ↔ Antigravity ↔ Web state sharing
- **Long-Term Memory** — Auto-extract learnings from research sessions
- **Session Management** — Archive, resume, and review past research

---

## Quick Start

```bash
# Clone
git clone https://github.com/Blackamethyst-ai/agent-core.git
cd agent-core

# Install
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

---

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

---

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

---

## Workflows

### Innovation Scout

```bash
agent-init "topic" --workflow innovation-scout
```

| Filter | Query | Purpose |
|--------|-------|---------|
| **Viral** | `stars:>500 pushed:>30days` | Production-ready, validated |
| **Groundbreaker** | `stars:10..200 created:>90days` | Novel, emerging patterns |

### Deep Research

```bash
agent-init "topic" --workflow deep-research
```

Multi-source investigation with artifact extraction across GitHub, arXiv, HuggingFace, and more.

---

## Scripts

| Script | Alias | Purpose |
|--------|-------|---------|
| `init_session.py` | `agent-init` | Initialize research sessions |
| `log_url.py` | `agent-log` | Log URLs with metadata |
| `sync_environments.py` | `agent-sync` | Cross-environment state sync |
| `archive_session.py` | `agent-archive` | Archive and extract learnings |

---

## Antigravity Shortcuts

| Key | Action |
|-----|--------|
| ⌘E | Switch to Agent Manager |
| ⌘L | Code with Agent |
| ⌘I | Edit code inline |

---

## Parallel Sessions

```
Tab 1: Planning/Orchestration
Tab 2-3: Feature development
Tab 4: Testing
Tab 5: Documentation
```

---

## Updating

```bash
cd ~/path/to/agent-core
git pull
./setup.sh --update
```

---

## Requirements

- Python 3.9+
- macOS / Linux
- Optional: Claude Code CLI, Antigravity IDE

---

## License

MIT License — See [LICENSE](LICENSE)

---

## Contact

**Metaventions AI**
Dico Angelo
dicoangelo@metaventionsai.com

<p align="center">
  <a href="https://metaventions-ai-architected-intelligence-1061986917838.us-west1.run.app/">
    <img src="https://img.shields.io/badge/Metaventions_AI-Website-00d9ff?style=for-the-badge" alt="Website" />
  </a>
  <a href="https://github.com/Blackamethyst-ai">
    <img src="https://img.shields.io/badge/GitHub-Blackamethyst--ai-1a1a2e?style=for-the-badge&logo=github" alt="GitHub" />
  </a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:4a0080,100:00d9ff&height=100&section=footer" />
</p>
