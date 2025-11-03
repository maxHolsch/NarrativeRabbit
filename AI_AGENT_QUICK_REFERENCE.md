# AI Narrative Intelligence Agent - Quick Reference Guide

## 🚀 Quick Start - Continuing Implementation

### Next Two Files to Create

#### 1. Resistance Mapper Template

```python
"""
Resistance Mapper - Sub-Agent for AI Narrative Intelligence System.

Maps resistance patterns across the organization and identifies root causes.
"""
from typing import List, Dict, Any, Optional
import logging
from collections import Counter, defaultdict

from ...db import neo4j_client

logger = logging.getLogger(__name__)


class ResistanceMapper:
    """
    Maps resistance patterns across the organization.

    Identifies:
    - Where resistance is strongest
    - Types of resistance (passive/skeptical/active/fearful)
    - Root causes
    - Whether resistance is spreading
    - Blocking effects on initiatives
    """

    # Define resistance patterns
    RESISTANCE_PATTERNS = {
        'passive': {
            'markers': ['waiting to see', 'not prioritized', 'when we have time'],
            'severity': 'low'
        },
        'skeptical': {
            'markers': ['not convinced', 'needs proof', 'where\'s the evidence'],
            'severity': 'medium'
        },
        'active': {
            'markers': ['won\'t work here', 'tried before', 'fundamentally flawed'],
            'severity': 'high'
        },
        'fearful': {
            'markers': ['worried about', 'concerned that', 'might lose'],
            'severity': 'high'
        }
    }

    def __init__(self):
        """Initialize the resistance mapper."""
        self.client = neo4j_client

    def map_resistance_landscape(self) -> Dict[str, Any]:
        """
        Map resistance across all groups.

        Returns:
            Complete resistance landscape analysis
        """
        groups = self._get_all_groups()

        resistance_map = {}
        for group in groups:
            resistance_map[group] = {
                'resistance_score': self._calculate_resistance_score(group),
                'patterns': self.identify_resistance_patterns(group),
                'narratives': self._get_resistance_narratives(group),
                'root_causes': self.infer_root_causes(group),
                'interventions': self._suggest_interventions(group)
            }

        return {
            'by_group': resistance_map,
            'hotspots': self._identify_hotspots(resistance_map),
            'common_patterns': self._find_common_patterns(resistance_map),
            'network_effects': self.analyze_resistance_spread()
        }

    def identify_resistance_patterns(self, group: str) -> List[Dict[str, Any]]:
        """
        Identify resistance patterns in a group.

        Args:
            group: Group name

        Returns:
            List of detected resistance patterns
        """
        # Get group stories
        group_stories = self._get_group_ai_stories(group)

        detected_patterns = []
        for pattern_name, pattern_def in self.RESISTANCE_PATTERNS.items():
            matches = [
                s for s in group_stories
                if any(marker in s.get('summary', '').lower() for marker in pattern_def['markers'])
            ]

            if matches:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'severity': pattern_def['severity'],
                    'frequency': len(matches),
                    'examples': matches[:3]
                })

        return detected_patterns

    def infer_root_causes(self, group: str) -> Dict[str, Any]:
        """
        Infer why a group is resistant.

        Possible causes:
        - Past failed initiatives
        - Threat to expertise/role
        - Resource constraints
        - Value misalignment
        - Lack of understanding

        Args:
            group: Group name

        Returns:
            Root cause analysis
        """
        group_stories = self._get_group_ai_stories(group)

        causes = {
            'past_failures': self._detect_past_failure_references(group_stories),
            'threat_perception': self._detect_threat_narratives(group_stories),
            'resource_issues': self._detect_resource_concerns(group_stories),
            'value_misalignment': self._detect_value_conflicts(group_stories),
            'knowledge_gap': self._detect_understanding_issues(group_stories)
        }

        # Rank by evidence strength
        ranked_causes = sorted(
            causes.items(),
            key=lambda x: self._calculate_evidence_strength(x[1]),
            reverse=True
        )

        return {
            'primary_cause': ranked_causes[0] if ranked_causes else None,
            'all_causes': ranked_causes,
            'causal_chains': self._extract_causal_chains(group_stories)
        }

    def analyze_resistance_spread(self) -> Dict[str, Any]:
        """
        Analyze if resistance is spreading through narrative contagion.

        Returns:
            Resistance spread analysis
        """
        # Find stories that reference other groups' experiences
        query = """
        MATCH (s1:Story)-[:REFERENCES]->(s2:Story)
        WHERE s1.ai_related = true
          AND s2.ai_related = true
          AND (s1.ai_sentiment < -0.3 OR s1.narrative_function = 'warning')
        MATCH (p1:Person)-[:TELLS]->(s1)
        MATCH (p2:Person)-[:TELLS]->(s2)
        MATCH (p1)-[:BELONGS_TO]->(g1:Group)
        MATCH (p2)-[:BELONGS_TO]->(g2:Group)
        RETURN g1.name as citing_group,
               g2.name as source_group,
               s1.id as citing_story,
               s2.id as source_story,
               count(*) as references
        """

        cross_references = self.client.execute_read_query(query)

        # Build contagion network
        contagion_network = self._build_narrative_network(cross_references)

        # Identify influential cautionary tales
        influential_stories = self._identify_influential_stories(contagion_network)

        return {
            'contagion_network': contagion_network,
            'influential_cautionary_tales': influential_stories,
            'spread_velocity': self._calculate_spread_velocity(cross_references)
        }

    # Helper methods follow existing pattern...
    def _get_all_groups(self) -> List[str]:
        query = "MATCH (g:Group) RETURN g.name as name"
        results = self.client.execute_read_query(query)
        return [r['name'] for r in results]

    def _get_group_ai_stories(self, group: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (g:Group {name: $group})<-[:BELONGS_TO]-(p:Person)-[:TELLS]->(s:Story)
        WHERE s.ai_related = true
        RETURN s
        """
        results = self.client.execute_read_query(query, {"group": group})
        return [dict(r["s"]) for r in results]

    # Implement remaining helper methods following patterns from existing analyzers...
```

#### 2. Adoption Readiness Scorer Template

```python
"""
Adoption Readiness Scorer - Sub-Agent for AI Narrative Intelligence System.

Scores organizational readiness for AI adoption based on narrative patterns.
"""
from typing import List, Dict, Any, Optional
import logging

from ...db import neo4j_client

logger = logging.getLogger(__name__)


class AdoptionReadinessScorer:
    """
    Scores organizational readiness based on narrative patterns.

    Dimensions:
    - Narrative alignment
    - Cultural receptivity
    - Trust foundation
    - Learning orientation
    - Leadership coherence
    - Cross-group coordination
    """

    def __init__(self):
        """Initialize the adoption readiness scorer."""
        self.client = neo4j_client

    def assess_readiness(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Assess overall AI adoption readiness.

        Args:
            initiative_id: Optional specific initiative

        Returns:
            Comprehensive readiness assessment
        """
        dimensions = {
            'narrative_alignment': self.score_narrative_alignment(initiative_id),
            'cultural_receptivity': self.score_cultural_receptivity(),
            'trust_foundation': self.score_trust_levels(),
            'learning_orientation': self.score_learning_orientation(),
            'leadership_coherence': self.score_leadership_coherence(),
            'coordination': self.score_coordination_narrative()
        }

        # Calculate weighted overall score
        weights = {
            'narrative_alignment': 0.20,
            'cultural_receptivity': 0.20,
            'trust_foundation': 0.15,
            'learning_orientation': 0.15,
            'leadership_coherence': 0.15,
            'coordination': 0.15
        }

        overall_score = sum(
            dimensions[dim]['score'] * weights[dim]
            for dim in dimensions
        )

        return {
            'overall_readiness': overall_score,
            'readiness_level': self._classify_readiness(overall_score),
            'dimension_scores': dimensions,
            'strengths': self._identify_strengths(dimensions),
            'risks': self._identify_risks(dimensions),
            'recommendations': self._generate_recommendations(dimensions),
            'forecast': self.forecast_adoption_trajectory(dimensions)
        }

    def score_narrative_alignment(self, initiative_id: Optional[str]) -> Dict[str, Any]:
        """
        Do different groups tell compatible stories?

        Args:
            initiative_id: Optional initiative to focus on

        Returns:
            Narrative alignment score and analysis
        """
        # Get stories by group
        stories_by_group = self._get_stories_by_group(initiative_id)

        # Compare across groups
        alignment_scores = []
        groups = list(stories_by_group.keys())

        for i, group1 in enumerate(groups):
            for group2 in groups[i+1:]:
                alignment = self._calculate_narrative_alignment(
                    stories_by_group[group1],
                    stories_by_group[group2]
                )
                alignment_scores.append(alignment)

        avg_alignment = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0

        return {
            'score': avg_alignment,
            'pairwise_alignments': alignment_scores,
            'interpretation': self._interpret_alignment(avg_alignment)
        }

    def score_trust_levels(self) -> Dict[str, Any]:
        """
        Do narratives indicate trust in leadership/process?

        Returns:
            Trust level score and analysis
        """
        trust_indicators = {
            'positive': ['delivered', 'followed through', 'transparent', 'listened'],
            'negative': ['promised but', 'abandoned', 'top-down', 'no one asked']
        }

        all_stories = self._get_all_ai_stories()

        positive_count = sum(
            1 for s in all_stories
            if any(ind in s.get('summary', '').lower() for ind in trust_indicators['positive'])
        )

        negative_count = sum(
            1 for s in all_stories
            if any(ind in s.get('summary', '').lower() for ind in trust_indicators['negative'])
        )

        total = positive_count + negative_count
        trust_score = positive_count / total if total > 0 else 0.5

        return {
            'score': trust_score,
            'positive_signals': positive_count,
            'negative_signals': negative_count,
            'interpretation': self._interpret_trust(trust_score)
        }

    def forecast_adoption_trajectory(self, dimensions: Dict) -> Dict[str, Any]:
        """
        Predict adoption trajectory based on current signals.

        Args:
            dimensions: Readiness dimension scores

        Returns:
            Trajectory forecast
        """
        # Analyze trend over time
        time_series = self._analyze_narrative_time_series()

        # Determine trajectory
        if time_series['trend'] == 'positive' and dimensions['cultural_receptivity']['score'] > 0.6:
            trajectory = 'accelerating'
        elif time_series['trend'] == 'negative' or dimensions['trust_foundation']['score'] < 0.4:
            trajectory = 'stalling'
        else:
            trajectory = 'uncertain'

        return {
            'predicted_trajectory': trajectory,
            'confidence': self._calculate_forecast_confidence(time_series, dimensions),
            'key_factors': self._identify_trajectory_factors(time_series, dimensions)
        }

    # Implement remaining methods following existing patterns...
```

## 🔑 Key Code Patterns

### 1. Cypher Query Pattern
```python
def query_pattern(self, param):
    query = """
    MATCH (n:Node)
    WHERE n.property = $value
    RETURN n
    LIMIT $limit
    """

    results = self.client.execute_read_query(
        query,
        {"value": param, "limit": 100}
    )

    return [dict(r["n"]) for r in results]
```

### 2. Scoring Pattern (0-1 scale)
```python
def score_dimension(self, data):
    # Count indicators
    positive_count = count_positive_indicators(data)
    negative_count = count_negative_indicators(data)

    # Calculate score
    total = positive_count + negative_count
    score = positive_count / total if total > 0 else 0.5

    return {
        'score': score,  # Always 0-1
        'positive': positive_count,
        'negative': negative_count,
        'interpretation': self._interpret_score(score)
    }
```

### 3. Interpretation Pattern
```python
def _interpret_score(self, score: float) -> str:
    """Generate human-readable interpretation"""
    if score > 0.7:
        return "Strong positive signal"
    elif score > 0.5:
        return "Moderate positive signal"
    elif score > 0.3:
        return "Moderate negative signal"
    else:
        return "Strong negative signal"
```

### 4. Evidence Pattern
```python
def analyze_with_evidence(self, data):
    # Perform analysis
    score = calculate_score(data)

    # Extract evidence
    evidence_stories = [
        story['id'] for story in data
        if meets_criteria(story)
    ]

    return {
        'score': score,
        'evidence': evidence_stories[:5],  # Top 5
        'interpretation': interpret(score)
    }
```

### 5. Aggregation Pattern
```python
def aggregate_scores(self, dimension_scores):
    weights = {
        'dimension_a': 0.3,
        'dimension_b': 0.3,
        'dimension_c': 0.2,
        'dimension_d': 0.2
    }

    overall = sum(
        dimension_scores[dim]['score'] * weights[dim]
        for dim in dimension_scores
    )

    return min(overall, 1.0)  # Cap at 1.0
```

## 📊 Testing Patterns

### Unit Test Template
```python
import pytest
from src.services.analysis.your_analyzer import YourAnalyzer

@pytest.fixture
def analyzer():
    return YourAnalyzer()

@pytest.fixture
def sample_story():
    return {
        'id': 'test-1',
        'summary': 'We tried AI copilot',
        'ai_related': True,
        'ai_sentiment': 0.7
    }

def test_method_name(analyzer, sample_story):
    result = analyzer.method_name([sample_story])

    assert 'score' in result
    assert 0 <= result['score'] <= 1
    assert 'interpretation' in result
```

### Integration Test Template
```python
def test_full_analysis_workflow():
    analyzer = YourAnalyzer()

    # With real Neo4j connection
    result = analyzer.main_method()

    assert result is not None
    assert 'overall_score' in result
    assert 'dimensions' in result
    assert all(
        0 <= dim['score'] <= 1
        for dim in result['dimensions'].values()
    )
```

## 🛠️ Common Utilities

### Text Analysis
```python
def contains_keywords(text: str, keywords: List[str]) -> bool:
    """Check if text contains any keywords"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

def extract_keywords(text: str, keyword_list: List[str]) -> Set[str]:
    """Extract matching keywords from text"""
    text_lower = text.lower()
    return {kw for kw in keyword_list if kw in text_lower}
```

### Sentiment Analysis
```python
def categorize_sentiment(sentiment: float) -> str:
    """Categorize sentiment score"""
    if sentiment > 0.5:
        return 'very positive'
    elif sentiment > 0.2:
        return 'positive'
    elif sentiment > -0.2:
        return 'neutral'
    elif sentiment > -0.5:
        return 'negative'
    else:
        return 'very negative'
```

### Counter Helpers
```python
from collections import Counter

def most_common_with_threshold(items: List[str], threshold: float) -> List[str]:
    """Get items appearing above threshold frequency"""
    counts = Counter(items)
    total = len(items)
    return [
        item for item, count in counts.items()
        if count / total >= threshold
    ]
```

## 🚨 Common Pitfalls to Avoid

1. **Forgetting to check for None/empty lists**
   ```python
   # BAD
   score = sum(values) / len(values)

   # GOOD
   score = sum(values) / len(values) if values else 0.5
   ```

2. **Not handling missing properties**
   ```python
   # BAD
   sentiment = story['ai_sentiment']

   # GOOD
   sentiment = story.get('ai_sentiment', 0)
   ```

3. **Scores outside 0-1 range**
   ```python
   # BAD
   return {'score': raw_score}

   # GOOD
   return {'score': min(max(raw_score, 0.0), 1.0)}
   ```

4. **Forgetting to convert Neo4j results to dicts**
   ```python
   # BAD
   return results

   # GOOD
   return [dict(r["s"]) for r in results]
   ```

## 📚 Quick Reference Links

- **Narrative Gap Analyzer:** `/backend/src/services/analysis/narrative_gap_analyzer.py`
- **Frame Competition Analyzer:** `/backend/src/services/analysis/frame_competition_analyzer.py`
- **Cultural Signal Detector:** `/backend/src/services/analysis/cultural_signal_detector.py`
- **Neo4j Client:** `/backend/src/db/neo4j_client.py`
- **Models:** `/backend/src/models/`

## ⚡ Pro Tips

1. **Start Small:** Implement one method at a time and test
2. **Use Print Statements:** During development, print intermediate results
3. **Test with Sample Data:** Create a few sample stories to test logic
4. **Follow Existing Patterns:** Copy structure from completed analyzers
5. **Read Helper Methods:** Many calculations are done in helper methods
6. **Check Data Types:** Neo4j returns different types than expected sometimes
7. **Use Optional Types:** Many parameters should be Optional[str] not str

## 🎯 Validation Checklist

Before considering a component complete:

- [ ] All methods have docstrings
- [ ] All scores are 0-1 range
- [ ] All methods return Dict[str, Any] as specified
- [ ] Interpretations are meaningful and actionable
- [ ] Evidence is included (story IDs)
- [ ] Error cases are handled (empty data, None values)
- [ ] Follows patterns from existing analyzers
- [ ] Neo4j queries use proper RETURN and LIMIT
- [ ] Results can be JSON serialized

---

**Quick Wins:**
1. Copy existing analyzer structure
2. Replace method names and docstrings
3. Implement main methods using same patterns
4. Test with sample data
5. Refine interpretations based on results
