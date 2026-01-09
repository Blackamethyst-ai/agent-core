# Parallel Sessions Workflow

Run multiple Claude instances in parallel for complex tasks.

## Trigger
```
/parallel [task description]
```

## Core Pattern

> "Run 5 Claudes in parallel in terminal. Number tabs 1-5, use system notifications for input."

## Setup

### Terminal Tabs (1-5)

```bash
# Tab 1: Planning/Orchestration
claude --session planning

# Tab 2: Feature A
claude --session feature-a

# Tab 3: Feature B  
claude --session feature-b

# Tab 4: Testing
claude --session testing

# Tab 5: Documentation
claude --session docs
```

### Naming Convention

| Tab | Role | Session Name |
|-----|------|--------------|
| 1 | Orchestrator | `[project]-planning` |
| 2 | Feature work | `[project]-feature-[name]` |
| 3 | Feature work | `[project]-feature-[name]` |
| 4 | Testing/QA | `[project]-testing` |
| 5 | Docs/Review | `[project]-docs` |

## Coordination Protocol

### 1. Orchestrator (Tab 1) Plans

```markdown
## Parallel Task Distribution

**Goal**: [Overall objective]

**Tab 2 Assignment**:
- [ ] Task A
- [ ] Task B

**Tab 3 Assignment**:
- [ ] Task C
- [ ] Task D

**Tab 4 Assignment**:
- [ ] Write tests for A, B
- [ ] Write tests for C, D

**Tab 5 Assignment**:
- [ ] Update README
- [ ] Document API changes
```

### 2. Workers Execute

Each tab:
1. Reads CLAUDE.md for context
2. Executes assigned tasks
3. Commits to feature branch
4. Signals completion via `/sync push`

### 3. Orchestrator Merges

Tab 1:
1. `/sync pull` from all sessions
2. Review changes
3. Resolve conflicts
4. Create PR

## Session Handoff

### Local → Web
```bash
# Background current session, open in browser
claude & 
# Opens claude.ai/code with session

# OR explicit teleport
claude --teleport
```

### Web → Local
```bash
# In terminal, pull web session
claude --continue [session-id]
```

### Antigravity Integration

In Antigravity's integrated terminal:
```bash
# Run CLI Claude alongside VSCode editing
claude --session antigravity-support
```

## Auto-Accept Mode

For 1-shot completion after planning:

```bash
# Plan first (interactive)
claude
> /plan [detailed goal]
> [iterate until plan is solid]

# Then execute with auto-accept
claude config set autoAccept true
> /execute
```

Or use keyboard shortcut:
- **Shift+Tab twice** → Plan mode
- **Confirm plan** → Auto-accept kicks in

## Sync Between Parallel Sessions

Each session writes to:
- `.agent/sessions/[session-name]/` — Local state
- `~/.agent-core/sessions/` — Global sync point

Merge protocol:
```bash
# In orchestrator (Tab 1)
/sync pull --all  # Pull all parallel sessions
/merge            # Interactive merge tool
/sync push        # Push merged state
```

## Example: Feature Development

```
Tab 1 (Planning):
  "Build user auth with OAuth"
  → Breaks into: UI, API, Tests, Docs
  
Tab 2 (UI):
  "Build login component"
  → Works on frontend
  
Tab 3 (API):
  "Build OAuth endpoints"
  → Works on backend
  
Tab 4 (Tests):
  "Write auth test suite"
  → Waits, then tests both
  
Tab 5 (Docs):
  "Document auth flow"
  → Writes docs in parallel
```

## Best Practices

1. **Good plan is key** — Spend time in Tab 1 before spawning workers
2. **Clear boundaries** — Each tab owns specific files/features
3. **Sync often** — `/sync push` after each major completion
4. **Number your tabs** — Consistent 1-5 mapping
5. **Use notifications** — System alerts when input needed
