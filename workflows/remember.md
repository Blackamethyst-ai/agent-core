# Remember Workflow

Store and recall facts, preferences, and learnings in persistent memory.

## Triggers
```
/remember [fact or preference]
/recall [query]
/memory status
/memory clear [scope]
```

## Memory Hierarchy

```
~/.agent-core/memory/
├── global.md           # Cross-project, permanent facts
├── learnings.md        # Research insights, patterns discovered
└── archive/            # Archived project memories

.agent/memory.md        # Project-specific memory
```

## Memory Schema

### Global Memory (`~/.agent-core/memory/global.md`)

```markdown
# Global Memory
Last updated: [timestamp]

## Identity & Preferences
- [User preferences, defaults, style choices]

## Technical Stack
- [Languages, frameworks, tools used]

## Architecture Patterns
- [Preferred patterns, anti-patterns to avoid]

## Contacts & Resources
- [Key URLs, APIs, people]

## Learnings
- [Insights from research sessions]
```

### Project Memory (`.agent/memory.md`)

```markdown
# Project Memory: [Project Name]
Last updated: [timestamp]

## Project Context
- [What this project is, goals]

## Architecture Decisions
- [Key decisions and rationale]

## Preferences
- [Project-specific preferences]

## History
- [Timeline of major changes]

## Open Questions
- [Unresolved decisions]
```

## Operations

### Remember (Store)

```
/remember User prefers TypeScript over JavaScript
```

1. Parse the fact/preference
2. Determine scope (global vs project)
3. Categorize (Identity, Technical, Architecture, etc.)
4. Append to appropriate memory file
5. Confirm what was stored

**Auto-categorization**:
| Keywords | Category |
|----------|----------|
| prefer, like, always, never | Preferences |
| use, stack, framework | Technical Stack |
| pattern, approach, architecture | Architecture |
| learned, discovered, insight | Learnings |

### Recall (Query)

```
/recall typescript preferences
```

1. Search both global and project memory
2. Return relevant entries with context
3. Indicate source (global vs project)

### Memory Status

```
/memory status
```

Shows:
- Global memory: [N] entries, last updated [date]
- Project memory: [N] entries, last updated [date]
- Recent additions

### Memory Clear

```
/memory clear project    # Clear project memory
/memory clear global     # Clear global memory (requires confirmation)
```

## Auto-Remember (Research Sessions)

After `/archive`, automatically extract and store:

1. **Key findings** → `~/.agent-core/memory/learnings.md`
2. **Useful resources** → Global memory under Resources
3. **Patterns discovered** → Architecture Patterns

Format:
```markdown
## [Date] - [Research Topic]
Session: [session-id]
- Finding 1 ([source](URL))
- Finding 2 ([source](URL))
```

## Memory in Context

When starting any session:

1. Load project memory (`.agent/memory.md`) if exists
2. Load relevant global memory sections
3. Include in context for informed responses

When ending session:

1. Prompt: "Any learnings to remember?"
2. Auto-suggest facts worth storing
3. Update memory files

## Sync Considerations

Memory files sync via `~/.agent-core/`:
- Changes in CLI immediately available in Antigravity
- Changes in Antigravity sync on next CLI session
- Conflict resolution: Latest timestamp wins

## Privacy

Memory stays local to user's machine. Never:
- Upload to external services
- Include in API requests
- Share across users
