# Agent Core v3.0 Specification
# Pareto-Guided Combinatorial Creativity Engine (PGCCE)

**Version:** 3.0.0-draft
**Date:** 2026-01-09
**Status:** Implementation Spec
**Based on:** Synthesis of arXiv papers 2412.14141, 2509.21043, 2511.18298

---

## Executive Summary

PGCCE extends Agent Core v2.0 with a closed-loop combinatorial creativity system that:
1. Retrieves knowledge across abstraction levels and domains
2. Translates concepts between domain-specific vocabularies
3. Generates candidate combinations
4. Scores candidates on dual novelty×utility axes
5. Selects Pareto-optimal candidates
6. Feeds successful patterns back to steer future retrieval

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PGCCE v3.0 ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    1. MULTI-LEVEL RETRIEVAL                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │   │
│  │  │ Concrete │  │ Pattern  │  │ Abstract │  │ Meta-Pattern     │ │   │
│  │  │ L0       │→ │ L1       │→ │ L2       │→ │ L3               │ │   │
│  │  │ "BERT"   │  │ "Transf" │  │ "Attn"   │  │ "Sparse routing" │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              2. CROSS-DOMAIN TRANSLATION AGENTS                  │   │
│  │                                                                  │   │
│  │   Domain A          Shared            Domain B                   │   │
│  │   Vocabulary   →    Ontology     →    Vocabulary                 │   │
│  │   "attention"       [FOCUS]           "salience"                 │   │
│  │   "gradient"        [SIGNAL]          "feedback"                 │   │
│  │   "embedding"       [REPRESENT]       "encoding"                 │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                  3. CANDIDATE GENERATOR                          │   │
│  │                                                                  │   │
│  │   Cross-domain pairs → LLM combination → Candidate ideas         │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              4. DUAL-AXIS NOVELTY×UTILITY SCORING                │   │
│  │                                                                  │   │
│  │   ┌─────────────────────────────────────────────────────────┐   │   │
│  │   │  Novelty (0-1)                                          │   │   │
│  │   │     ▲                                                   │   │   │
│  │   │ 1.0 ┤           ○ High-N, Low-U (impractical)          │   │   │
│  │   │     │        ★                                          │   │   │
│  │   │ 0.5 ┤     ★     ★  ← Pareto Frontier                   │   │   │
│  │   │     │  ○           ★                                    │   │   │
│  │   │ 0.0 ┼──────────────────────────────────▶ Utility (0-1) │   │   │
│  │   │           ○ Low-N, Low-U (discard)                      │   │   │
│  │   └─────────────────────────────────────────────────────────┘   │   │
│  │                                                                  │   │
│  │   Novelty Score = f(semantic_distance, prior_frequency)         │   │
│  │   Utility Score = g(feasibility, relevance, impact_estimate)    │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              5. PARETO FRONTIER SELECTION                        │   │
│  │                                                                  │   │
│  │   Select candidates where no other candidate dominates on       │   │
│  │   BOTH axes. Keep top-k Pareto-optimal solutions.               │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              6. FEEDBACK LOOP (STEERING)                         │   │
│  │                                                                  │   │
│  │   Pareto winners → Extract patterns → Refine retrieval queries  │   │
│  │                                                                  │   │
│  │   "What abstraction levels produced best results?"               │   │
│  │   "Which domain pairs had highest yield?"                        │   │
│  │   "What translation mappings worked?"                            │   │
│  │                                                                  │   │
│  │   → Update retrieval weights                                     │   │
│  │   → Prioritize productive domain pairs                           │   │
│  │   → Expand successful abstraction levels                         │   │
│  │                                                                  │   │
│  └────────────────────────────────┬────────────────────────────────┘   │
│                                   │                                     │
│                                   └──────────────► (back to step 1)     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Multi-Level Retrieval System

**Purpose:** Retrieve concepts at varying abstraction levels to enable cross-domain bridging.

**File:** `scripts/retrieval_engine.py`

```python
class AbstractionLevel(Enum):
    L0_CONCRETE = 0    # Specific implementations: "BERT", "ResNet", "PostgreSQL"
    L1_PATTERN = 1     # Design patterns: "transformer", "skip connections", "ACID"
    L2_ABSTRACT = 2    # Abstract concepts: "attention", "residual flow", "consistency"
    L3_META = 3        # Meta-patterns: "sparse routing", "hierarchical decomposition"

class RetrievalEngine:
    def __init__(self, embedding_model: str = "text-embedding-3-large"):
        self.embedder = EmbeddingModel(embedding_model)
        self.level_indices = {level: VectorIndex() for level in AbstractionLevel}
        self.abstraction_classifier = AbstractionClassifier()

    def index_concept(self, concept: str, source: str, domain: str) -> None:
        """Index a concept at its detected abstraction level."""
        level = self.abstraction_classifier.classify(concept)
        embedding = self.embedder.embed(concept)
        self.level_indices[level].add(ConceptNode(
            text=concept,
            embedding=embedding,
            source=source,
            domain=domain,
            level=level
        ))

    def retrieve_cross_level(
        self,
        query: str,
        source_level: AbstractionLevel,
        target_levels: list[AbstractionLevel],
        top_k: int = 10
    ) -> list[ConceptNode]:
        """Retrieve related concepts across abstraction levels."""
        query_embedding = self.embedder.embed(query)
        results = []
        for level in target_levels:
            level_results = self.level_indices[level].search(
                query_embedding,
                k=top_k
            )
            results.extend(level_results)
        return self._rank_by_bridging_potential(results, source_level)

    def retrieve_cross_domain(
        self,
        concept: str,
        source_domain: str,
        target_domains: list[str],
        level: AbstractionLevel
    ) -> list[CrossDomainMatch]:
        """Find analogous concepts in other domains at same abstraction level."""
        source_embedding = self.embedder.embed(concept)
        matches = []
        for domain in target_domains:
            domain_concepts = self.level_indices[level].filter_by_domain(domain)
            for node in domain_concepts.search(source_embedding, k=5):
                matches.append(CrossDomainMatch(
                    source=concept,
                    source_domain=source_domain,
                    target=node.text,
                    target_domain=domain,
                    similarity=node.score,
                    level=level
                ))
        return matches
```

**Data Structures:**

```python
@dataclass
class ConceptNode:
    text: str
    embedding: np.ndarray
    source: str           # URL or paper ID
    domain: str           # "ML", "biology", "economics", etc.
    level: AbstractionLevel
    metadata: dict = field(default_factory=dict)

@dataclass
class CrossDomainMatch:
    source: str
    source_domain: str
    target: str
    target_domain: str
    similarity: float
    level: AbstractionLevel
```

---

### 2. Cross-Domain Translation Agents

**Purpose:** Translate domain-specific vocabulary into shared ontology and back.

**File:** `scripts/translation_agents.py`

```python
class SharedOntology:
    """Core concepts that bridge domains."""
    CONCEPTS = {
        "FOCUS": ["attention", "salience", "priority", "selection"],
        "SIGNAL": ["gradient", "feedback", "error", "delta"],
        "REPRESENT": ["embedding", "encoding", "feature", "latent"],
        "COMPOSE": ["layer", "module", "component", "block"],
        "ROUTE": ["gating", "switching", "selection", "dispatch"],
        "MEMORY": ["cache", "buffer", "state", "storage"],
        "OPTIMIZE": ["loss", "objective", "fitness", "reward"],
    }

class TranslationAgent:
    def __init__(self, llm_client, domain: str):
        self.llm = llm_client
        self.domain = domain
        self.vocabulary = self._load_domain_vocabulary(domain)
        self.ontology = SharedOntology()

    def to_shared(self, term: str) -> tuple[str, float]:
        """Map domain term to shared ontology concept."""
        prompt = f"""
        Domain: {self.domain}
        Term: {term}

        Map this term to the most appropriate shared concept:
        {list(self.ontology.CONCEPTS.keys())}

        Return: concept_name, confidence (0-1)
        """
        return self.llm.structured_call(prompt, OntologyMapping)

    def from_shared(self, concept: str, target_domain: str) -> list[str]:
        """Generate domain-specific terms from shared concept."""
        prompt = f"""
        Shared concept: {concept}
        Target domain: {target_domain}

        Generate 3-5 domain-specific terms that express this concept
        in {target_domain} vocabulary.
        """
        return self.llm.structured_call(prompt, list[str])

    def translate(
        self,
        term: str,
        source_domain: str,
        target_domain: str
    ) -> TranslationResult:
        """Full translation pipeline: source → shared → target."""
        shared_concept, confidence = self.to_shared(term)
        target_terms = self.from_shared(shared_concept, target_domain)
        return TranslationResult(
            source_term=term,
            source_domain=source_domain,
            shared_concept=shared_concept,
            target_terms=target_terms,
            target_domain=target_domain,
            confidence=confidence
        )

class TranslationOrchestrator:
    """Manages multiple domain-specific translation agents."""

    def __init__(self, llm_client):
        self.agents = {}
        self.llm = llm_client

    def get_agent(self, domain: str) -> TranslationAgent:
        if domain not in self.agents:
            self.agents[domain] = TranslationAgent(self.llm, domain)
        return self.agents[domain]

    def translate_concept_pair(
        self,
        concept_a: str,
        domain_a: str,
        concept_b: str,
        domain_b: str
    ) -> ConceptBridge:
        """Create a bridge between two concepts from different domains."""
        agent_a = self.get_agent(domain_a)
        agent_b = self.get_agent(domain_b)

        shared_a, conf_a = agent_a.to_shared(concept_a)
        shared_b, conf_b = agent_b.to_shared(concept_b)

        return ConceptBridge(
            concept_a=concept_a,
            domain_a=domain_a,
            shared_a=shared_a,
            concept_b=concept_b,
            domain_b=domain_b,
            shared_b=shared_b,
            bridge_strength=self._compute_bridge_strength(shared_a, shared_b),
            combined_confidence=(conf_a + conf_b) / 2
        )
```

---

### 3. Candidate Generator

**Purpose:** Generate novel idea candidates by combining cross-domain concepts.

**File:** `scripts/candidate_generator.py`

```python
class CombinationStrategy(Enum):
    ANALOGY = "analogy"           # A is to B as C is to ?
    BLEND = "blend"               # Merge properties of A and B
    TRANSFER = "transfer"         # Apply method from A to problem B
    INVERT = "invert"             # What if we did the opposite?
    SCALE = "scale"               # What if we scaled this 1000x?

class CandidateGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.strategies = list(CombinationStrategy)

    def generate_candidates(
        self,
        concept_bridge: ConceptBridge,
        problem_context: str,
        strategies: list[CombinationStrategy] = None,
        n_per_strategy: int = 3
    ) -> list[IdeaCandidate]:
        """Generate idea candidates using combination strategies."""
        strategies = strategies or self.strategies
        candidates = []

        for strategy in strategies:
            prompt = self._build_prompt(concept_bridge, problem_context, strategy)
            ideas = self.llm.structured_call(prompt, list[RawIdea])

            for idea in ideas[:n_per_strategy]:
                candidates.append(IdeaCandidate(
                    id=generate_uuid(),
                    description=idea.description,
                    mechanism=idea.mechanism,
                    source_bridge=concept_bridge,
                    strategy=strategy,
                    raw_novelty_signals=idea.novelty_signals,
                    raw_utility_signals=idea.utility_signals,
                    timestamp=datetime.now()
                ))

        return candidates

    def _build_prompt(
        self,
        bridge: ConceptBridge,
        context: str,
        strategy: CombinationStrategy
    ) -> str:
        prompts = {
            CombinationStrategy.ANALOGY: f"""
                In {bridge.domain_a}, "{bridge.concept_a}" works by {bridge.shared_a}.
                In {bridge.domain_b}, "{bridge.concept_b}" works by {bridge.shared_b}.

                Problem context: {context}

                Generate ideas: If we apply the mechanism of {bridge.concept_a}
                to the domain of {bridge.domain_b}, what novel solutions emerge?
            """,
            CombinationStrategy.BLEND: f"""
                Concept A ({bridge.domain_a}): {bridge.concept_a}
                Concept B ({bridge.domain_b}): {bridge.concept_b}
                Shared abstraction: {bridge.shared_a} ↔ {bridge.shared_b}

                Problem context: {context}

                Generate ideas that BLEND properties of both concepts into
                something new that didn't exist in either domain.
            """,
            # ... other strategies
        }
        return prompts.get(strategy, prompts[CombinationStrategy.ANALOGY])

@dataclass
class IdeaCandidate:
    id: str
    description: str
    mechanism: str
    source_bridge: ConceptBridge
    strategy: CombinationStrategy
    raw_novelty_signals: list[str]
    raw_utility_signals: list[str]
    novelty_score: float = None
    utility_score: float = None
    pareto_rank: int = None
    timestamp: datetime = None
```

---

### 4. Dual-Axis Scoring System

**Purpose:** Score candidates on both novelty and utility dimensions.

**File:** `scripts/dual_axis_scorer.py`

```python
class NoveltyScorer:
    """Compute novelty score based on semantic distance and prior frequency."""

    def __init__(self, embedding_model, corpus_index):
        self.embedder = embedding_model
        self.corpus = corpus_index  # Index of known ideas/papers

    def score(self, candidate: IdeaCandidate) -> NoveltyScore:
        idea_embedding = self.embedder.embed(candidate.description)

        # Semantic distance from nearest known ideas
        nearest = self.corpus.search(idea_embedding, k=10)
        avg_distance = 1 - np.mean([n.similarity for n in nearest])

        # Combination rarity: how often do these domains intersect?
        domain_pair_freq = self.corpus.get_domain_pair_frequency(
            candidate.source_bridge.domain_a,
            candidate.source_bridge.domain_b
        )
        rarity_score = 1 - min(domain_pair_freq / 100, 1.0)

        # Abstraction jump bonus: larger jumps = more novel
        level_jump = abs(
            candidate.source_bridge.concept_a_level.value -
            candidate.source_bridge.concept_b_level.value
        )
        jump_bonus = level_jump * 0.1

        raw_score = (
            0.5 * avg_distance +
            0.3 * rarity_score +
            0.2 * jump_bonus
        )

        return NoveltyScore(
            value=min(raw_score, 1.0),
            semantic_distance=avg_distance,
            domain_rarity=rarity_score,
            abstraction_jump=level_jump,
            nearest_existing=nearest[:3]
        )


class UtilityScorer:
    """Compute utility score based on feasibility, relevance, impact."""

    def __init__(self, llm_client, context_docs: list[str]):
        self.llm = llm_client
        self.context = context_docs

    def score(self, candidate: IdeaCandidate, problem: str) -> UtilityScore:

        # Feasibility: Can this actually be built/implemented?
        feasibility = self._score_feasibility(candidate)

        # Relevance: Does this solve the stated problem?
        relevance = self._score_relevance(candidate, problem)

        # Impact estimate: How significant would success be?
        impact = self._score_impact(candidate)

        raw_score = (
            0.4 * feasibility +
            0.4 * relevance +
            0.2 * impact
        )

        return UtilityScore(
            value=raw_score,
            feasibility=feasibility,
            relevance=relevance,
            impact=impact,
            blockers=self._identify_blockers(candidate)
        )

    def _score_feasibility(self, candidate: IdeaCandidate) -> float:
        prompt = f"""
        Idea: {candidate.description}
        Mechanism: {candidate.mechanism}

        Rate feasibility (0-1) based on:
        - Technical maturity of required components
        - Availability of necessary data/resources
        - Clarity of implementation path

        Return: score (float), reasoning (str)
        """
        result = self.llm.structured_call(prompt, FeasibilityResult)
        return result.score

    def _score_relevance(self, candidate: IdeaCandidate, problem: str) -> float:
        prompt = f"""
        Problem: {problem}
        Proposed idea: {candidate.description}

        Rate relevance (0-1):
        - Does this directly address the problem?
        - Does it solve root cause or just symptoms?
        - Would the target users value this solution?

        Return: score (float), reasoning (str)
        """
        result = self.llm.structured_call(prompt, RelevanceResult)
        return result.score


class DualAxisScorer:
    """Orchestrate novelty and utility scoring."""

    def __init__(self, novelty_scorer: NoveltyScorer, utility_scorer: UtilityScorer):
        self.novelty = novelty_scorer
        self.utility = utility_scorer

    def score_candidate(
        self,
        candidate: IdeaCandidate,
        problem: str
    ) -> ScoredCandidate:
        novelty_score = self.novelty.score(candidate)
        utility_score = self.utility.score(candidate, problem)

        candidate.novelty_score = novelty_score.value
        candidate.utility_score = utility_score.value

        return ScoredCandidate(
            candidate=candidate,
            novelty=novelty_score,
            utility=utility_score,
            combined_score=novelty_score.value * utility_score.value,  # Geometric mean
            timestamp=datetime.now()
        )
```

---

### 5. Pareto Frontier Selection

**Purpose:** Select candidates that are not dominated on both axes.

**File:** `scripts/pareto_selector.py`

```python
class ParetoSelector:
    """Select Pareto-optimal candidates from scored pool."""

    def __init__(self, min_novelty: float = 0.2, min_utility: float = 0.2):
        self.min_novelty = min_novelty
        self.min_utility = min_utility

    def select(
        self,
        candidates: list[ScoredCandidate],
        max_frontier_size: int = 10
    ) -> ParetoResult:
        # Filter below-threshold candidates
        viable = [
            c for c in candidates
            if c.novelty.value >= self.min_novelty
            and c.utility.value >= self.min_utility
        ]

        if not viable:
            return ParetoResult(frontier=[], dominated=candidates, stats={})

        # Compute Pareto frontier
        frontier = []
        dominated = []

        for candidate in viable:
            is_dominated = False
            to_remove = []

            for existing in frontier:
                if self._dominates(existing, candidate):
                    is_dominated = True
                    break
                elif self._dominates(candidate, existing):
                    to_remove.append(existing)

            if not is_dominated:
                frontier = [f for f in frontier if f not in to_remove]
                dominated.extend(to_remove)
                frontier.append(candidate)
            else:
                dominated.append(candidate)

        # Rank frontier by combined score
        frontier.sort(key=lambda c: c.combined_score, reverse=True)

        # Assign Pareto ranks
        for i, c in enumerate(frontier):
            c.candidate.pareto_rank = i + 1

        return ParetoResult(
            frontier=frontier[:max_frontier_size],
            dominated=dominated,
            stats={
                "total_candidates": len(candidates),
                "viable_candidates": len(viable),
                "frontier_size": len(frontier),
                "avg_novelty": np.mean([c.novelty.value for c in frontier]),
                "avg_utility": np.mean([c.utility.value for c in frontier]),
            }
        )

    def _dominates(self, a: ScoredCandidate, b: ScoredCandidate) -> bool:
        """Returns True if a dominates b (better on both axes)."""
        return (
            a.novelty.value >= b.novelty.value and
            a.utility.value >= b.utility.value and
            (a.novelty.value > b.novelty.value or a.utility.value > b.utility.value)
        )


@dataclass
class ParetoResult:
    frontier: list[ScoredCandidate]
    dominated: list[ScoredCandidate]
    stats: dict
```

---

### 6. Feedback Loop / Steering System

**Purpose:** Learn from successful combinations to improve future retrieval.

**File:** `scripts/feedback_loop.py`

```python
class FeedbackLoop:
    """Extract patterns from Pareto winners to steer future retrieval."""

    def __init__(self, retrieval_engine: RetrievalEngine, llm_client):
        self.retrieval = retrieval_engine
        self.llm = llm_client
        self.history = FeedbackHistory()

    def analyze_winners(self, pareto_result: ParetoResult) -> FeedbackSignals:
        """Extract learning signals from Pareto-optimal candidates."""
        frontier = pareto_result.frontier

        if not frontier:
            return FeedbackSignals.empty()

        # Analyze successful domain pairs
        domain_pairs = Counter()
        for c in frontier:
            pair = tuple(sorted([
                c.candidate.source_bridge.domain_a,
                c.candidate.source_bridge.domain_b
            ]))
            domain_pairs[pair] += c.combined_score

        # Analyze successful abstraction levels
        level_scores = defaultdict(float)
        for c in frontier:
            bridge = c.candidate.source_bridge
            level_scores[bridge.concept_a_level] += c.combined_score
            level_scores[bridge.concept_b_level] += c.combined_score

        # Analyze successful strategies
        strategy_scores = defaultdict(float)
        for c in frontier:
            strategy_scores[c.candidate.strategy] += c.combined_score

        # Extract successful translation patterns
        translation_patterns = self._extract_translation_patterns(frontier)

        return FeedbackSignals(
            top_domain_pairs=domain_pairs.most_common(5),
            top_abstraction_levels=sorted(
                level_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            top_strategies=sorted(
                strategy_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            translation_patterns=translation_patterns,
            timestamp=datetime.now()
        )

    def apply_steering(self, signals: FeedbackSignals) -> RetrievalConfig:
        """Update retrieval configuration based on feedback signals."""
        config = self.retrieval.get_config()

        # Boost successful domain pairs
        for (domain_a, domain_b), score in signals.top_domain_pairs:
            config.domain_weights[domain_a] *= (1 + score * 0.2)
            config.domain_weights[domain_b] *= (1 + score * 0.2)

        # Prioritize successful abstraction levels
        for level, score in signals.top_abstraction_levels:
            config.level_weights[level] *= (1 + score * 0.3)

        # Expand search in productive directions
        new_queries = self._generate_expansion_queries(signals)
        config.expansion_queries = new_queries

        # Store for persistence
        self.history.add(signals)

        return config

    def _generate_expansion_queries(
        self,
        signals: FeedbackSignals
    ) -> list[str]:
        """Generate new retrieval queries based on successful patterns."""
        prompt = f"""
        Successful domain pairs: {signals.top_domain_pairs}
        Successful abstraction levels: {signals.top_abstraction_levels}
        Successful strategies: {signals.top_strategies}

        Generate 5 new search queries that would find MORE concepts
        in these productive directions. Focus on:
        1. Adjacent domains to the successful pairs
        2. Similar abstraction levels
        3. Concepts that enable the successful strategies

        Return: list of search query strings
        """
        return self.llm.structured_call(prompt, list[str])


@dataclass
class FeedbackSignals:
    top_domain_pairs: list[tuple[tuple[str, str], float]]
    top_abstraction_levels: list[tuple[AbstractionLevel, float]]
    top_strategies: list[tuple[CombinationStrategy, float]]
    translation_patterns: list[TranslationPattern]
    timestamp: datetime

    @classmethod
    def empty(cls) -> "FeedbackSignals":
        return cls([], [], [], [], datetime.now())
```

---

## Workflow Integration

**File:** `workflows/combinatorial-creativity.md`

```markdown
# Combinatorial Creativity Workflow (PGCCE)

Generate novel ideas through systematic cross-domain combination with
Pareto-optimal selection on novelty×utility axes.

## Trigger
```
/creativity <problem-statement> [--domains D1,D2,...] [--iterations N]
```

## Execution

### 1. Initialize PGCCE Session
```bash
python3 ~/.agent-core/scripts/init_pgcce.py "<problem>" --domains "D1,D2,D3"
```

### 2. Multi-Level Retrieval
- Index concepts from specified domains at L0-L3 abstraction levels
- Retrieve cross-domain concept pairs
- Output: `scratchpad.json` → `concept_pairs[]`

### 3. Cross-Domain Translation
- For each concept pair, compute shared ontology mapping
- Generate concept bridges with translation confidence
- Output: `scratchpad.json` → `concept_bridges[]`

### 4. Candidate Generation
- Apply combination strategies (analogy, blend, transfer, invert, scale)
- Generate 3-5 candidates per bridge per strategy
- Output: `scratchpad.json` → `candidates[]`

### 5. Dual-Axis Scoring
- Score each candidate on novelty (0-1)
- Score each candidate on utility (0-1)
- Output: `scratchpad.json` → `scored_candidates[]`

### 6. Pareto Selection
- Compute Pareto frontier
- Rank by combined score
- Output: `scratchpad.json` → `pareto_frontier[]`

### 7. Feedback & Iteration
- Extract patterns from winners
- Update retrieval weights
- Generate expansion queries
- If iterations remain, GOTO step 2

### 8. Generate Report
Create `<problem>_creativity_report.md`:

```markdown
# Creativity Report: <PROBLEM>
Generated: <DATE> | Iterations: <N>

## Pareto-Optimal Ideas

### Rank 1: <Title>
**Novelty:** 0.XX | **Utility:** 0.XX
**Source:** <Domain A> × <Domain B>
**Mechanism:** <description>
**Next steps:** <actionable items>

### Rank 2: ...

## Iteration History
| Iter | Candidates | Frontier Size | Top Domains |
|------|------------|---------------|-------------|

## Feedback Signals Applied
- Domain boosts: ...
- Level priorities: ...
- Expansion queries: ...
```
```

---

## Directory Structure (v3.0)

```
~/.agent-core/
├── config.json                 # Updated for v3.0
├── memory/
│   └── global.md
├── scripts/
│   ├── init_session.py         # v2.0 (unchanged)
│   ├── sync_environments.py    # v2.0 (unchanged)
│   ├── log_url.py              # v2.0 (unchanged)
│   ├── archive_session.py      # v2.0 (unchanged)
│   │
│   │ # ─── NEW v3.0 PGCCE ───
│   ├── init_pgcce.py           # PGCCE session initializer
│   ├── retrieval_engine.py     # Multi-level retrieval
│   ├── translation_agents.py   # Cross-domain translation
│   ├── candidate_generator.py  # Combination strategies
│   ├── dual_axis_scorer.py     # Novelty × Utility scoring
│   ├── pareto_selector.py      # Pareto frontier selection
│   ├── feedback_loop.py        # Steering system
│   └── pgcce_orchestrator.py   # Main engine orchestrator
│
├── workflows/
│   ├── innovation-scout.md     # v2.0
│   ├── deep-research.md        # v2.0
│   ├── remember.md             # v2.0
│   ├── session-archiver.md     # v2.0
│   │
│   │ # ─── NEW v3.0 ───
│   └── combinatorial-creativity.md
│
├── indices/                    # NEW: Vector indices
│   ├── concepts_l0.faiss
│   ├── concepts_l1.faiss
│   ├── concepts_l2.faiss
│   ├── concepts_l3.faiss
│   └── known_ideas.faiss       # For novelty scoring
│
├── ontology/                   # NEW: Shared ontology
│   ├── core_concepts.json
│   └── domain_vocabularies/
│       ├── ml.json
│       ├── biology.json
│       ├── economics.json
│       └── ...
│
└── sessions/
    └── <session-id>/
        ├── session.json
        ├── concept_pairs.json      # NEW
        ├── concept_bridges.json    # NEW
        ├── scored_candidates.json  # NEW
        ├── pareto_history.json     # NEW
        └── feedback_signals.json   # NEW
```

---

## Configuration (v3.0)

**File:** `config.json`

```json
{
  "version": "3.0",
  "environments": {
    "cli": {
      "enabled": true,
      "default_model": "claude",
      "web_search": true
    },
    "antigravity": {
      "enabled": true,
      "browser_subagent": true,
      "auto_sync": true
    }
  },
  "sync": {
    "enabled": true,
    "conflict_resolution": "latest_wins",
    "auto_push": true
  },
  "logging": {
    "log_all_urls": true,
    "checkpoint_interval_minutes": 5
  },
  "pgcce": {
    "embedding_model": "text-embedding-3-large",
    "llm_model": "claude-sonnet-4-20250514",
    "default_domains": ["ML", "biology", "physics", "economics", "design"],
    "abstraction_levels": ["L0", "L1", "L2", "L3"],
    "combination_strategies": ["analogy", "blend", "transfer", "invert", "scale"],
    "scoring": {
      "min_novelty": 0.2,
      "min_utility": 0.2,
      "novelty_weights": {
        "semantic_distance": 0.5,
        "domain_rarity": 0.3,
        "abstraction_jump": 0.2
      },
      "utility_weights": {
        "feasibility": 0.4,
        "relevance": 0.4,
        "impact": 0.2
      }
    },
    "pareto": {
      "max_frontier_size": 10,
      "min_candidates_per_iteration": 20
    },
    "feedback": {
      "domain_boost_factor": 0.2,
      "level_boost_factor": 0.3,
      "history_window": 10
    }
  }
}
```

---

## API / CLI Commands

```bash
# Initialize PGCCE session
agent-creativity "design a new recommendation algorithm" --domains "ML,psychology,economics"

# Run single iteration
agent-creativity-step --iteration 1

# View Pareto frontier
agent-pareto --session <id>

# View feedback signals
agent-feedback --session <id>

# Export results
agent-creativity-export --format md|json|csv
```

---

## Dependencies

```
# requirements-v3.txt
numpy>=1.24.0
faiss-cpu>=1.7.4          # Vector similarity search
tiktoken>=0.5.0           # Token counting
anthropic>=0.18.0         # Claude API
openai>=1.12.0            # Embeddings API
pydantic>=2.0             # Data validation
rich>=13.0                # CLI output
```

---

## Implementation Priority

| Phase | Components | Effort |
|-------|------------|--------|
| **P0** | `retrieval_engine.py`, `dual_axis_scorer.py`, `pareto_selector.py` | Core loop |
| **P1** | `translation_agents.py`, `candidate_generator.py` | Generation |
| **P2** | `feedback_loop.py`, `pgcce_orchestrator.py` | Closed loop |
| **P3** | Workflow integration, CLI commands | UX |
| **P4** | Ontology expansion, domain vocabularies | Scale |

---

## Success Metrics

1. **Pareto frontier quality**: % of generated ideas that domain experts rate as "genuinely novel AND useful"
2. **Iteration improvement**: Does feedback steering increase frontier quality over iterations?
3. **Domain coverage**: Can the system productively bridge N+ domains?
4. **Time to insight**: How quickly does a high-quality candidate emerge?

---

*Spec Version: 3.0.0-draft*
*Compatible with: Agent Core v2.0+*
