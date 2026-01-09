# Deep Research Workflow

Deploy comprehensive research on a technical topic, competitor, or domain.

## Trigger
```
/deep-research [topic]
```

## Requirements
- **Minimum 3 distinct sources** (docs, blogs, repos, papers)
- **Extract artifacts**: code snippets, configs, architecture patterns
- **Log all URLs** visited during research

## Execution

### 1. Initialize
```bash
python3 ~/.agent-core/scripts/init_session.py "[topic]" --workflow deep-research
```

### 2. Research Strategy

Plan sources before diving in:

| Source Type | Examples | Extract |
|-------------|----------|---------|
| Official Docs | docs.*, readthedocs | API patterns, configs |
| GitHub Repos | READMEs, /docs, /examples | Code snippets, architecture |
| Technical Blogs | engineering.*, medium | Case studies, lessons |
| arXiv/Papers | arxiv.org, papers.* | Novel approaches |
| Discussions | HN, Reddit, Discord | Real-world feedback |

### 3. Browser Subagent (Antigravity)

If in Antigravity environment, launch browser subagent:

```
Research Goal: [specific objective]
Constraints:
- Visit minimum 3 sources
- Extract code/config examples
- Log every URL to session_log.md
- Checkpoint findings every 5 minutes
```

### 4. CLI Research (Terminal)

If in Terminal CLI, use web_search + web_fetch:

1. Search for authoritative sources
2. Fetch and extract relevant content
3. Log URLs to session_log.md
4. Save snippets to scratchpad.json

### 5. Extraction Protocol

**Code Snippets** — Save to `.agent/research/snippets/`:
```
snippets/
├── [source]_[description].py
├── [source]_config.json
└── [source]_architecture.md
```

**Patterns** — Document in scratchpad:
```json
{
  "patterns_discovered": [
    {
      "name": "...",
      "source": "URL",
      "description": "...",
      "code_ref": "snippets/..."
    }
  ]
}
```

### 6. Log All URLs

**Critical**: Every URL visited must be logged, even if:
- Content was irrelevant
- Page failed to load
- Information was skimmed only

```markdown
## URLs Visited
| Time | URL | Status | Used | Notes |
|------|-----|--------|------|-------|
| 19:30 | https://... | ✓ 200 | ✓ | Main source |
| 19:32 | https://... | ✓ 200 | ✗ | Off-topic |
| 19:33 | https://... | ✗ 404 | — | Dead link |
```

### 7. Synthesis

Generate `.agent/research/[topic]_research.md`:

```markdown
# Deep Research: [TOPIC]
Generated: [DATE] | Session: [ID]
Sources consulted: [N]

## Executive Summary
[Key findings and recommendations]

## Source Analysis

### [Source 1 Name](URL)
**Type**: Documentation | Blog | Repo | Paper
**Key Takeaways**:
- Point 1
- Point 2

**Extracted Artifacts**:
- `snippets/source1_example.py` — [description]

### [Source 2 Name](URL)
...

## Patterns Discovered

### Pattern: [Name]
**Source**: [URL]
**Description**: ...
**Implementation**:
```code
[snippet]
```

## Recommendations

Based on this research:
1. [Actionable recommendation with source link]
2. [Actionable recommendation with source link]

## Next Steps
- [ ] [Suggested follow-up action]
- [ ] [Suggested follow-up action]

## Full URL Log
See `session_log.md` for complete browsing history.
```

### 8. Offer Follow-up

After synthesis, offer:
- Create new component based on findings
- Generate implementation plan
- Archive session for future reference
- Continue researching specific subtopic

## Environment Handoff

Research can span environments:

1. **Plan in CLI**: Define research goal, identify sources
2. **Execute in Antigravity**: Browser automation for deep extraction
3. **Synthesize in CLI**: Generate report, update memory

Use `/sync` to transfer state between environments.
