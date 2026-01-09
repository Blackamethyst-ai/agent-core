# Environment Configuration

Setup and sync protocol for Terminal CLI and Antigravity (VSCode OSS) environments.

## Environment Overview

| Environment | Type | Best For |
|-------------|------|----------|
| **Terminal CLI** | Claude Code in terminal | Planning, synthesis, parallel sessions |
| **Antigravity** | VSCode OSS desktop app | Coding, preview, file editing |
| **Claude.ai/code** | Web interface | Handoff, visual review |

## Workflow Patterns

### Parallel Workflows
```
1/ Run 5 Claudes in parallel in terminal
   - Number tabs 1-5
   - Use system notifications for input
   
2/ Run 5-10 Claudes on claude.ai/code in parallel
   - Handoff local sessions to web (&)
   - Manually kick off, or --teleport back
```

### Model & Strategy
```
3/ Use Opus 4.5 with thinking for everything
   - Best coding model, bigger & slower
   - But FASTER in the end due to less steering & better tool use
   
4/ Team shares a single CLAUDE.md for the repo
   - Check into git
   - Multiple team contributions weekly
   - Add incorrect actions for Claude to learn
```

### Session Management
```
6/ Most sessions start in Plan Mode (shift+tab twice)
   - Write a PR goal, iterate on plan
   - Switch to auto-accept edits mode for 1-shot completion
   - Good plan is key
   
7/ Slash commands: /help, /config, /reset, etc.
   - Integrate custom scripts/tools for automation
```

## Environment Detection

### Terminal CLI (Claude Code)
```bash
# Detected when running `claude` command
command -v claude && [ -t 1 ]
```

**Capabilities**:
- Parallel sessions (tabs 1-5)
- Web search
- File operations
- Code execution
- Memory access
- Plan mode → Auto-accept flow

**Session defaults**:
```bash
# Always auto-accept (user preference)
claude config set autoAccept true

# Use Opus 4.5 with thinking
claude config set model opus-4.5
```

### Antigravity (VSCode OSS Desktop)
```
Version: 1.13.3
Base: VSCode OSS 1.104.0
Runtime: Electron 37.3.1 / Chromium 138
```

**Capabilities**:
- Full VSCode editing
- Browser preview panel
- Integrated terminal
- Extensions ecosystem
- File tree navigation
- Git integration

**Agent integration**:
- Reads `CLAUDE.md` at project root
- Reads `.agent/` directory
- Syncs via `~/.agent-core/`

### Handoff: CLI ↔ Antigravity

```bash
# From CLI, hand off to web/Antigravity
claude --teleport  # Opens in browser
# OR
claude &           # Background, continue in another session

# From Antigravity, teleport back to CLI
# Use integrated terminal: claude --continue
```

## Global Configuration

### Setup (`~/.agent-core/config.json`)

```json
{
  "version": "1.0",
  "environments": {
    "cli": {
      "enabled": true,
      "default_model": "claude",
      "web_search": true
    },
    "antigravity": {
      "enabled": true,
      "browser_subagent": true,
      "screenshot_capture": true,
      "auto_sync": true
    }
  },
  "sync": {
    "enabled": true,
    "sync_dir": "~/.agent-core",
    "conflict_resolution": "latest_wins",
    "auto_push": true,
    "auto_pull": true
  },
  "memory": {
    "global_path": "~/.agent-core/memory/global.md",
    "learnings_path": "~/.agent-core/memory/learnings.md",
    "auto_extract": true
  },
  "logging": {
    "log_all_urls": true,
    "log_unused_urls": true,
    "log_failed_urls": true,
    "checkpoint_interval_minutes": 5
  }
}
```

### Initialize Global Structure

```bash
#!/bin/bash
# Run once to set up global agent-core

AGENT_CORE="$HOME/.agent-core"

mkdir -p "$AGENT_CORE"/{sessions,memory,workflows}

# Create default config
cat > "$AGENT_CORE/config.json" << 'EOF'
{
  "version": "1.0",
  "sync": { "enabled": true },
  "logging": { "log_all_urls": true }
}
EOF

# Create empty memory files
touch "$AGENT_CORE/memory/global.md"
touch "$AGENT_CORE/memory/learnings.md"

# Create session index
echo "| Date | Session ID | Topic | Workflow | Duration | Key Finding |" > "$AGENT_CORE/sessions/index.md"
echo "|------|------------|-------|----------|----------|-------------|" >> "$AGENT_CORE/sessions/index.md"

echo "✅ Agent Core initialized at: $AGENT_CORE"
```

## Sync Protocol

### Push (CLI → Global)

```bash
python3 ~/.agent-core/scripts/sync_environments.py push
```

1. Copy `.agent/research/*` → `~/.agent-core/sessions/[current]/`
2. Merge `.agent/memory.md` updates → global memory
3. Update `last_sync` timestamp

### Pull (Global → Local)

```bash
python3 ~/.agent-core/scripts/sync_environments.py pull
```

1. Copy latest session state to `.agent/research/`
2. Load global memory into context
3. Update `last_sync` timestamp

### Auto-Sync Triggers

| Event | Action |
|-------|--------|
| Session start | Pull latest state |
| Checkpoint (5 min) | Push current state |
| `/archive` | Final push + archive |
| Environment switch | Bidirectional sync |

### Conflict Resolution

When same file modified in both environments:

1. **latest_wins** (default): Use most recent timestamp
2. **merge**: Attempt to merge (memory files only)
3. **prompt**: Ask user which version to keep

## Cross-Environment Workflow

### Example: Research Spanning Both Environments

1. **CLI: Plan**
   ```
   /innovation-scout transformer architectures
   ```
   - Defines research goal
   - Initial web search
   - Creates session workspace
   - Auto-push state

2. **Antigravity: Execute**
   ```
   /sync pull
   /deep-research --continue
   ```
   - Pulls CLI session state
   - Browser subagent opens tabs
   - Deep extraction from repos
   - Screenshots key findings
   - Auto-push results

3. **CLI: Synthesize**
   ```
   /sync pull
   /archive
   ```
   - Pulls Antigravity findings
   - Generates final report
   - Archives session
   - Updates memory

## Antigravity-Specific Setup

### Browser Subagent Configuration

In Antigravity, configure browser subagent to:

1. **Log URLs**: Write every navigation to `session_log.md`
2. **Checkpoint**: Save state every 5 minutes
3. **Extract artifacts**: Copy code snippets to `snippets/`
4. **Screenshot**: Capture key findings (optional)

### Tab Management

```markdown
## Browser Tabs (Antigravity)

| Tab | URL | Purpose | Status |
|-----|-----|---------|--------|
| 1 | https://... | Main research | Active |
| 2 | https://... | Comparison | Background |
```

On `/archive`, close all research tabs and log final state.

## Desktop Integration

### Global Workflow Export

```bash
# Export workflows to Desktop for easy access
TARGET="$HOME/Desktop/AntigravityGlobal"
mkdir -p "$TARGET/workflows"
cp ~/.agent-core/workflows/*.md "$TARGET/workflows/"
```

### Quick Install Alias

Add to `~/.zshrc`:
```bash
alias agent-init='python3 ~/.agent-core/scripts/init_session.py'
alias agent-sync='python3 ~/.agent-core/scripts/sync_environments.py'
alias agent-archive='python3 ~/.agent-core/scripts/archive_session.py'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Sync conflict | Check timestamps, use `--force` flag |
| Missing session | Check `~/.agent-core/sessions/` |
| Memory not loading | Verify file paths in config.json |
| Antigravity not detecting | Check `$ANTIGRAVITY_SESSION` env var |
