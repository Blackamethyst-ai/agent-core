---
name: agent-core
description: Unified agent orchestration for research, innovation scouting, and memory across CLI (Claude Code), Antigravity (VSCode OSS), and web environments.
version: 2.0.0
---

# Agent Core v2.0

Research orchestration skill for agentic workflows.

## Triggers

- `/innovation-scout [topic]` — GitHub + arXiv dual-filter search
- `/deep-research [topic]` — Multi-source investigation
- `/remember [fact]` — Store to memory
- `/recall [query]` — Query memory
- `/sync` — Push/pull session state
- `/archive` — Close session

## Quick Reference

```
Mode:     Auto-accept (always)
Model:    Opus 4.5 with thinking
Plan:     Shift+Tab twice → iterate → execute
Parallel: Up to 5 terminal tabs
```

## Commands

| Alias | Script | Description |
|-------|--------|-------------|
| `agent-init` | init_session.py | Start session |
| `agent-log` | log_url.py | Log URLs |
| `agent-sync` | sync_environments.py | Sync state |
| `agent-status` | sync_environments.py status | Quick status |
| `agent-archive` | archive_session.py | Close session |

## Search Filters

**Viral**: `[topic] stars:>500 pushed:>[30d]`
**Groundbreaker**: `[topic] stars:10..200 created:>[90d]`

## URL Logging

Log ALL URLs — used or not:

```bash
agent-log <url> --used --relevance 3
agent-log <url> --skipped --notes "reason"
```

## Setup

```bash
./setup.sh
```
