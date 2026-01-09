#!/bin/bash
# ============================================================
# Agent Core v2.0 - Setup Script
# ============================================================
# Unified agent system for CLI + Antigravity (VSCode OSS)
#
# Usage:
#   ./setup.sh              # Full install
#   ./setup.sh --update     # Update existing (pull from git first)
#   ./setup.sh --minimal    # No shell aliases
#   ./setup.sh --uninstall  # Remove agent-core
# ============================================================

set +e  # Don't exit on error

AGENT_CORE="$HOME/.agent-core"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m' GREEN='\033[0;32m' YELLOW='\033[1;33m'
    BLUE='\033[0;34m' CYAN='\033[0;36m' NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' CYAN='' NC=''
fi

log_ok() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_err() { echo -e "${RED}✗${NC} $1"; }
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }

echo ""
echo "============================================================"
echo "  Agent Core v2.0 Setup"
echo "============================================================"
echo ""

# Parse arguments
MINIMAL=false
UNINSTALL=false
UPDATE=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --minimal) MINIMAL=true ;;
        --uninstall) UNINSTALL=true ;;
        --update) UPDATE=true ;;
        --help|-h)
            echo "Usage: ./setup.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --update     Update existing installation"
            echo "  --minimal    Install without shell aliases"
            echo "  --uninstall  Remove agent-core completely"
            echo "  --help       Show this help"
            exit 0
            ;;
        *) log_err "Unknown: $1"; exit 1 ;;
    esac
    shift
done

# Uninstall
if [ "$UNINSTALL" = true ]; then
    echo "Uninstalling Agent Core..."
    rm -rf "$AGENT_CORE"
    log_ok "Removed $AGENT_CORE"
    echo ""
    echo "Note: Remove aliases from ~/.zshrc manually."
    exit 0
fi

# Create directories
echo "Creating directories..."
mkdir -p "$AGENT_CORE/sessions"
mkdir -p "$AGENT_CORE/memory"
mkdir -p "$AGENT_CORE/workflows"
mkdir -p "$AGENT_CORE/scripts"
mkdir -p "$AGENT_CORE/assets"
log_ok "Created $AGENT_CORE"

# Copy scripts
echo "Installing scripts..."
if [ -d "$SCRIPT_DIR/scripts" ]; then
    for f in "$SCRIPT_DIR/scripts/"*.py; do
        [ -f "$f" ] && cp "$f" "$AGENT_CORE/scripts/" && chmod +x "$AGENT_CORE/scripts/$(basename "$f")"
    done
    log_ok "Scripts installed"
else
    log_warn "No scripts directory found"
fi

# Copy workflows
echo "Installing workflows..."
if [ -d "$SCRIPT_DIR/workflows" ]; then
    for f in "$SCRIPT_DIR/workflows/"*.md; do
        [ -f "$f" ] && cp "$f" "$AGENT_CORE/workflows/"
    done
    log_ok "Workflows installed"
else
    log_warn "No workflows directory found"
fi

# Copy assets
echo "Installing assets..."
if [ -d "$SCRIPT_DIR/assets" ]; then
    for f in "$SCRIPT_DIR/assets/"*; do
        [ -f "$f" ] && cp "$f" "$AGENT_CORE/assets/"
    done
    log_ok "Assets installed"
else
    log_warn "No assets directory found"
fi

# Create config (only if new install or --update)
if [ ! -f "$AGENT_CORE/config.json" ] || [ "$UPDATE" = true ]; then
    echo "Creating config..."
    cat > "$AGENT_CORE/config.json" << 'EOF'
{
  "version": "2.0",
  "defaults": {
    "auto_accept": true,
    "model": "claude-opus-4-5-20251101",
    "thinking": true,
    "max_parallel_sessions": 5
  },
  "environments": {
    "cli": { "enabled": true, "auto_accept": true },
    "antigravity": {
      "enabled": true,
      "type": "vscode-oss",
      "shortcuts": { "agent_manager": "cmd+e", "code_with_agent": "cmd+l", "edit_inline": "cmd+i" }
    },
    "web": { "enabled": true }
  },
  "sync": { "enabled": true, "conflict_resolution": "latest_wins" },
  "logging": { "log_all_urls": true, "log_unused_urls": true },
  "research": {
    "viral_filter": { "min_stars": 500, "recency_days": 30 },
    "groundbreaker_filter": { "min_stars": 10, "max_stars": 200, "recency_days": 90 }
  }
}
EOF
    log_ok "Config created"
fi

# Initialize memory
if [ ! -f "$AGENT_CORE/memory/global.md" ]; then
    echo "Initializing memory..."
    cat > "$AGENT_CORE/memory/global.md" << EOF
# Global Memory

Last updated: $TIMESTAMP

## Preferences

## Technical Stack

## Resources
EOF
    log_ok "Memory initialized"
fi

if [ ! -f "$AGENT_CORE/memory/learnings.md" ]; then
    cat > "$AGENT_CORE/memory/learnings.md" << 'EOF'
# Research Learnings

Auto-extracted from archived sessions.

---

EOF
    log_ok "Learnings initialized"
fi

# Session index
if [ ! -f "$AGENT_CORE/sessions/index.md" ]; then
    cat > "$AGENT_CORE/sessions/index.md" << 'EOF'
# Session Index

| Date | Session ID | Topic | Workflow | Duration | URLs | Key Finding |
|------|------------|-------|----------|----------|------|-------------|
EOF
    log_ok "Session index created"
fi

# Configure Claude Code
if command -v claude &> /dev/null; then
    claude config set autoAccept true 2>/dev/null && log_ok "Claude auto-accept enabled"
fi

# Shell aliases
if [ "$MINIMAL" = false ]; then
    echo ""
    echo "============================================================"
    echo "  Add to ~/.zshrc"
    echo "============================================================"
    echo ""
    cat << 'ALIASES'
# Agent Core v2.0
export AGENT_CORE="$HOME/.agent-core"
alias agent-init='python3 $AGENT_CORE/scripts/init_session.py'
alias agent-log='python3 $AGENT_CORE/scripts/log_url.py'
alias agent-sync='python3 $AGENT_CORE/scripts/sync_environments.py'
alias agent-status='python3 $AGENT_CORE/scripts/sync_environments.py status'
alias agent-archive='python3 $AGENT_CORE/scripts/archive_session.py'
ALIASES
    echo ""
fi

# Done
echo "============================================================"
echo -e "${GREEN}  Setup Complete!${NC}"
echo "============================================================"
echo ""
echo "Quick start:"
echo "  agent-init 'topic'        # Start research"
echo "  agent-log <url> --used    # Log URL"
echo "  agent-status              # Check state"
echo "  agent-archive             # Close session"
echo ""
echo "Update from git:"
echo "  cd $(dirname "$SCRIPT_DIR") && git pull && ./setup.sh --update"
echo ""
