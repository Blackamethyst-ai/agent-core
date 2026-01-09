# Innovation Scout Workflow

Scour arXiv and GitHub for cutting-edge innovations relevant to the current context.

## Trigger
```
/innovation-scout [topic]
```

If no topic provided, detect from:
1. Current project (`package.json`, `README.md`, etc.)
2. Recent conversation context
3. Prompt user

## Execution

### 1. Initialize
```bash
python3 ~/.agent-core/scripts/init_session.py "[topic]" --workflow innovation-scout
```

### 2. Dual-Filter Search

**Filter A — Viral** (community-vetted, production-ready):
```
[topic] stars:>500 pushed:>[30 days ago]
```
- Focus: High adoption, active maintenance, good docs
- Signal: Stars, recent commits, issue response time

**Filter B — Groundbreaker** (novel, experimental):
```
[topic] stars:10..200 created:>[90 days ago]
```
- Focus: Novel architectures, unique approaches, research implementations
- Signal: Linked papers, novel keywords, lab affiliations

**arXiv Categories**:
| Domain | Categories |
|--------|------------|
| AI/ML | cs.AI, cs.LG, cs.CL, cs.CV |
| Systems | cs.OS, cs.DC, cs.SE |
| Math | math.OC, stat.ML |

### 3. Log Everything

Append to `.agent/research/session_log.md`:

```markdown
## Innovation Scout: [topic]
Started: [timestamp]
Environment: [cli|antigravity]

### URLs Visited
| Time | Source | URL | Filter | Used | Relevance |
|------|--------|-----|--------|------|-----------|
```

### 4. Checkpoint Findings

Update `.agent/research/scratchpad.json`:
```json
{
  "workflow": "innovation-scout",
  "viral_candidates": [
    {"name": "...", "url": "...", "stars": N, "why": "..."}
  ],
  "groundbreaker_candidates": [
    {"name": "...", "url": "...", "stars": N, "novel": "..."}
  ],
  "arxiv_papers": [
    {"title": "...", "url": "...", "arxiv_id": "...", "insight": "..."}
  ]
}
```

### 5. Generate Report

Create `.agent/research/[topic]_innovation_report.md`:

```markdown
# Innovation Report: [TOPIC]
Generated: [DATE] | Session: [ID]
Sources: [N] GitHub repos, [M] arXiv papers

## Executive Summary
[2-3 sentences on key findings and recommendations]

## The Viral Choice
**[Name](URL)** — ★ [stars] | Updated [date]
- Why: [Production-readiness rationale]
- Key features: [bullet points]
- Integration: [how to adopt]

## The Groundbreaker Choice
**[Name](URL)** — ★ [stars] | Created [date]
- Why: [Innovation value rationale]  
- Novel approach: [what's new]
- Caveats: [maturity concerns]

## Additional Discoveries

### High-Adoption Options
| Name | Stars | Why Consider |
|------|-------|--------------|
| [Name](URL) | N | One-line |

### Emerging Innovations
| Name | Stars | Novel Aspect |
|------|-------|--------------|
| [Name](URL) | N | One-line |

### arXiv Papers
| Title | ID | Key Insight |
|-------|-----|-------------|
| [Title](URL) | XXXX.XXXXX | One-line |

## Search Methodology
- Viral filter: `[query used]`
- Groundbreaker filter: `[query used]`
- arXiv categories: [list]
- Total URLs visited: N (see session_log.md)
```

### 6. Export Sources

Create `.agent/research/[topic]_sources.csv`:
```csv
name,url,type,filter,stars,date,relevance,used,notes
```

### 7. Archive (Optional)

Run `/archive` to close session and sync to global storage.

## Antigravity-Specific

If running in Antigravity with browser subagent:
1. Subagent opens actual browser tabs
2. Capture screenshots of key findings
3. Extract code snippets directly from repos
4. Navigate to `/tree/main/docs` or `/wiki` for docs
