# Session Archiver Workflow

Close research sessions, log all URLs, archive outputs, and update long-term memory.

## Trigger
```
/archive
/archive [session-id]
```

## What Gets Archived

Every session produces:

| File | Purpose | Destination |
|------|---------|-------------|
| `session_log.md` | Human-readable narrative | Archive |
| `scratchpad.json` | Machine-readable data | Archive |
| `[topic]_report.md` | Final output | Archive + Project |
| `[topic]_sources.csv` | Raw source data | Archive |
| `snippets/` | Extracted code | Archive |

## Archive Process

### 1. Validate Session Complete

Check `.agent/research/` contains:
- [ ] `session_log.md` with URL table
- [ ] At least one output file
- [ ] `scratchpad.json` with final state

If incomplete, warn and offer to continue research.

### 2. Generate Session Archive

Create `~/.agent-core/sessions/[session-id]/session_archive.md`:

```markdown
# Session Archive: [Topic]
ID: [session-id]
Workflow: [innovation-scout|deep-research|custom]
Environment: [cli|antigravity]
Started: [timestamp]
Completed: [timestamp]
Duration: [X minutes]

## Summary
[Executive summary from report]

## Outcomes
- Primary finding: [Name](URL)
- Key insight: ...
- Artifacts generated: [list]

## Complete URL Log

### URLs Used in Final Output
| URL | Type | Relevance | Contribution |
|-----|------|-----------|--------------|

### URLs Visited But Not Used
| URL | Type | Why Skipped |
|-----|------|-------------|

### Failed/Unreachable URLs
| URL | Error | Timestamp |
|-----|-------|-----------|

## Files Archived
- `session_log.md`
- `scratchpad.json`
- `[topic]_report.md`
- `[topic]_sources.csv`
- `snippets/` (if any)

## Memory Extractions
Facts added to long-term memory:
- [fact 1]
- [fact 2]

## Related Sessions
- [Previous session on similar topic]
- [Follow-up session if any]
```

### 3. Copy Files to Archive

```bash
mkdir -p ~/.agent-core/sessions/[session-id]
cp -r .agent/research/* ~/.agent-core/sessions/[session-id]/
```

### 4. Extract Learnings to Memory

Prompt or auto-extract:
- Key findings worth remembering
- Useful resources discovered
- Patterns identified

Append to `~/.agent-core/memory/learnings.md`:

```markdown
## [Date] - [Topic] ([session-id])
- [Learning 1] ([source](URL))
- [Learning 2] ([source](URL))
```

### 5. Update Session Index

Append to `~/.agent-core/sessions/index.md`:

```markdown
| Date | Session ID | Topic | Workflow | Duration | Key Finding |
|------|------------|-------|----------|----------|-------------|
| [date] | [id] | [topic] | [type] | [min] | [one-liner] |
```

### 6. Clean Local Workspace

```bash
rm -rf .agent/research/*
echo "Session archived: [session-id]" > .agent/research/.last_session
```

### 7. Confirm Archive

Output:
```
✅ Session archived: [session-id]
📁 Location: ~/.agent-core/sessions/[session-id]/
📝 Learnings extracted: [N] facts
🔗 URLs logged: [N] total ([M] used, [K] skipped)

To revisit: /recall [topic]
To continue: /deep-research [topic] --continue
```

## URL Logging Standards

**Every URL must be logged with**:
- Timestamp (when visited)
- Source type (github, arxiv, docs, blog, etc.)
- HTTP status (200, 404, etc.)
- Used flag (✓/✗)
- Relevance score (★★★/★★☆/★☆☆/☆☆☆)
- Notes (why used or skipped)

**Why log unused URLs?**
- Prevents re-visiting dead ends
- Documents research thoroughness
- Enables future re-research
- Creates audit trail

## Antigravity Integration

If archiving from Antigravity:
1. Close all research browser tabs
2. Export tab history to session_log.md
3. Capture final screenshots if configured
4. Sync to `~/.agent-core/sessions/`

## Re-opening Archived Sessions

```
/research --continue [session-id]
```

1. Load archived session from `~/.agent-core/sessions/[session-id]/`
2. Restore `scratchpad.json` state
3. Continue research with prior context
