# Search Strategies Reference

## GitHub Search Syntax

### Basic Filters
```
stars:>N          # Minimum stars
stars:N..M        # Star range
pushed:>YYYY-MM-DD    # Recent activity
created:>YYYY-MM-DD   # Recently created
language:python   # By language
topic:machine-learning # By topic tag
```

### Viral Filter Template
```
[keywords] stars:>500 pushed:>2024-12-01 language:[lang]
```

### Groundbreaker Filter Template
```
[keywords] stars:10..200 created:>2024-10-01
```

### Domain-Specific Queries

**AI/ML:**
```
transformer architecture stars:>100
neural network [specific-type] stars:>50
[framework] plugin extension
```

**Web/Frontend:**
```
react component [feature] stars:>200
nextjs template stars:>100
```

**Infrastructure:**
```
kubernetes operator [domain]
terraform module [provider]
```

## arXiv Search

### Category Codes
| Code | Domain |
|------|--------|
| cs.AI | Artificial Intelligence |
| cs.LG | Machine Learning |
| cs.CV | Computer Vision |
| cs.CL | Computation & Language (NLP) |
| cs.NE | Neural & Evolutionary Computing |
| cs.SE | Software Engineering |
| stat.ML | Machine Learning (Statistics) |

### Search URL Patterns
```
https://arxiv.org/search/?query=[terms]&searchtype=all
https://arxiv.org/list/cs.LG/recent
https://export.arxiv.org/api/query?search_query=all:[terms]&max_results=20
```

### Extraction Shortcuts
- Abstract: `https://arxiv.org/abs/XXXX.XXXXX`
- PDF: `https://arxiv.org/pdf/XXXX.XXXXX`
- HTML (if available): `https://arxiv.org/html/XXXX.XXXXX`

## Relevance Scoring

Rate each finding:
- ★★★ Directly applicable, high quality
- ★★☆ Relevant with adaptation needed
- ★☆☆ Tangentially related, worth noting
- ☆☆☆ Not relevant, skip

## Cross-Reference Signals

Strong innovation indicators:
- GitHub repo links arXiv paper (implementation of research)
- arXiv paper has "code available" badge
- Multiple independent implementations of same paper
- Recent spike in GitHub stars (trending)
- Citations from major labs (Google, Meta, Anthropic, OpenAI)
