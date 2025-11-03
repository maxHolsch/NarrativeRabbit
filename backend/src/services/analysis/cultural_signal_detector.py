"""
Cultural Signal Detector - Sub-Agent for AI Narrative Intelligence System.

Detects cultural patterns in how AI is discussed.
Identifies whether narratives indicate innovation vs risk-averse culture.
"""
from typing import List, Dict, Any, Optional
import logging
from collections import Counter

from ...db import neo4j_client

logger = logging.getLogger(__name__)


class CulturalSignalDetector:
    """
    Detects cultural signals in AI narratives.

    Identifies:
    - Innovation culture indicators
    - Risk aversion signals
    - Experimentation patterns
    - Failure tolerance
    - Employee agency
    """

    # Signal definitions
    INNOVATION_SIGNALS = {
        'strong': [
            'Stories celebrate experiments, even failures',
            'AI described as tool for exploration',
            'Multiple groups share "we tried X" stories',
            'Failures framed as learning opportunities',
            'Language: "experiment", "explore", "iterate"'
        ],
        'moderate': [
            'Some experimentation stories',
            'Cautious optimism language',
            'Structured pilot programs discussed'
        ],
        'weak': [
            'Few experimentation stories',
            'AI discussed theoretically',
            'Focus on "when others do it" not "when we do it"'
        ]
    }

    RISK_AVERSION_SIGNALS = {
        'strong': [
            'Cautionary tales dominate',
            'AI framed as dangerous/unpredictable',
            'Stories emphasize need for control',
            'Few "success with AI" stories',
            'Language: "ensure", "prevent", "control", "risk"'
        ],
        'moderate': [
            'Balance of caution and opportunity',
            'Emphasis on "safe" use cases',
            'Approval processes featured in stories'
        ],
        'weak': [
            'Risk mentioned but not dominant',
            'Balanced view of pros/cons'
        ]
    }

    def __init__(self):
        """Initialize the cultural signal detector."""
        self.client = neo4j_client

    def assess_innovation_culture(self) -> Dict[str, Any]:
        """
        Assess whether the narrative landscape indicates innovation culture.

        Returns:
            Innovation culture assessment with scores across dimensions
        """
        # Get all AI stories
        stories = self._get_all_ai_stories()

        if not stories:
            return {
                'error': 'No AI stories found for analysis',
                'overall_score': 0.5
            }

        # Score on multiple dimensions
        scores = {
            'experimentation': self.score_experimentation(stories),
            'failure_tolerance': self.score_failure_framing(stories),
            'agency': self.score_employee_agency(stories),
            'speed': self.score_iteration_speed(stories),
            'diversity': self.score_narrative_diversity(stories)
        }

        # Aggregate into overall assessment
        overall = self._aggregate_culture_score(scores)

        return {
            'overall_score': overall,
            'dimension_scores': scores,
            'key_evidence': self._extract_key_evidence(stories, scores),
            'culture_type': self._classify_culture(overall),
            'recommendations': self._generate_recommendations(scores)
        }

    def _get_all_ai_stories(self) -> List[Dict[str, Any]]:
        """Get all AI-related stories."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
        RETURN s
        ORDER BY s.timestamp DESC
        LIMIT 100
        """

        results = self.client.execute_read_query(query)
        return [dict(r["s"]) for r in results]

    def score_experimentation(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score experimentation culture based on stories.

        Looks for:
        - Stories about trying AI
        - Grassroots vs executive experiments
        - Cross-functional experimentation
        - Outcome sharing

        Args:
            stories: All AI stories

        Returns:
            Experimentation score and analysis
        """
        experiment_stories = [
            s for s in stories
            if self._is_experimentation_story(s)
        ]

        # Pattern analysis
        patterns = {
            'grassroots_experiments': len([
                s for s in experiment_stories
                if s.get('source') in ['individual', 'team', 'slack', 'interview']
            ]),
            'executive_experiments': len([
                s for s in experiment_stories
                if s.get('source') in ['executive', 'leadership', 'official']
            ]),
            'cross_functional': len([
                s for s in experiment_stories
                if len(s.get('primary_themes', [])) > 2  # Proxy for cross-functional
            ]),
            'outcomes_shared': len([
                s for s in experiment_stories
                if s.get('why_told') in ['teaching', 'celebrating', 'explaining']
            ])
        }

        # Calculate score (0-1 scale)
        score = 0
        score += min(patterns['grassroots_experiments'] / 10, 0.3)  # Max 0.3
        score += min(patterns['cross_functional'] / 5, 0.2)  # Max 0.2
        score += min(patterns['outcomes_shared'] / 10, 0.3)  # Max 0.3
        score += 0.2 if patterns['grassroots_experiments'] > patterns['executive_experiments'] else 0

        return {
            'score': min(score, 1.0),
            'patterns': patterns,
            'total_experiment_stories': len(experiment_stories),
            'interpretation': self._interpret_experimentation_score(score, patterns)
        }

    def _is_experimentation_story(self, story: Dict[str, Any]) -> bool:
        """Check if a story indicates experimentation."""
        # Check explicit indicator
        if story.get('experimentation_indicator'):
            return True

        # Check story type
        if story.get('type') == 'learning':
            return True

        # Check narrative function
        if story.get('narrative_function') == 'explanation':
            return True

        # Check text for experimentation language
        text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()
        experiment_keywords = [
            'tried', 'experiment', 'test', 'pilot', 'prototype',
            'explore', 'trial', 'attempt'
        ]

        return any(keyword in text for keyword in experiment_keywords)

    def _interpret_experimentation_score(self, score: float, patterns: Dict[str, int]) -> str:
        """Generate interpretation of experimentation score."""
        if score > 0.7:
            return "Strong experimentation culture - grassroots innovation with shared learnings"
        elif score > 0.4:
            return "Moderate experimentation - some bottom-up activity"
        elif patterns['executive_experiments'] > patterns['grassroots_experiments']:
            return "Top-down experimentation - limited grassroots innovation"
        else:
            return "Low experimentation - risk-averse culture"

    def score_failure_framing(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score how AI failures are discussed.

        Innovation culture: "We tried X, learned Y, now trying Z"
        Risk-averse culture: "X failed, that's why we don't do Y"

        Args:
            stories: All AI stories

        Returns:
            Failure framing score and analysis
        """
        failure_stories = [
            s for s in stories
            if s.get('type') == 'failure' or
            s.get('ai_sentiment', 0) < -0.3 or
            s.get('outcome', '').lower() in ['failure', 'negative', 'disappointing']
        ]

        if not failure_stories:
            return {
                'score': 0.5,
                'total_failures': 0,
                'interpretation': 'No failure stories found - could indicate lack of experimentation or lack of psychological safety'
            }

        # Analyze how failures are framed
        learning_framed = [
            s for s in failure_stories
            if self._is_learning_framed(s)
        ]

        warning_framed = [
            s for s in failure_stories
            if self._is_warning_framed(s)
        ]

        # Calculate ratio
        learning_ratio = len(learning_framed) / len(failure_stories) if failure_stories else 0.5

        return {
            'score': learning_ratio,
            'total_failures': len(failure_stories),
            'learning_framed': len(learning_framed),
            'warning_framed': len(warning_framed),
            'interpretation': self._interpret_failure_framing(learning_ratio, len(failure_stories))
        }

    def _is_learning_framed(self, story: Dict[str, Any]) -> bool:
        """Check if failure is framed as learning opportunity."""
        # Check explicit framing
        if story.get('failure_framing') == 'learning':
            return True

        # Check for learning indicators
        lessons = story.get('lessons', [])
        if lessons and len(lessons) > 0:
            return True

        # Check text
        text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()
        learning_keywords = ['learn', 'lesson', 'insight', 'next time', 'improve', 'adjust']

        return any(keyword in text for keyword in learning_keywords)

    def _is_warning_framed(self, story: Dict[str, Any]) -> bool:
        """Check if failure is framed as warning."""
        # Check explicit framing
        if story.get('failure_framing') == 'warning':
            return True

        if story.get('why_told') == 'warning':
            return True

        if story.get('narrative_function') == 'warning':
            return True

        # Check text
        text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()
        warning_keywords = ['avoid', 'never', "don't", 'mistake', 'careful', 'danger']

        return any(keyword in text for keyword in warning_keywords)

    def _interpret_failure_framing(self, learning_ratio: float, total_failures: int) -> str:
        """Generate interpretation of failure framing."""
        if learning_ratio > 0.6:
            return f"High innovation: {total_failures} failures discussed as learning opportunities"
        elif learning_ratio < 0.4:
            return f"Risk averse: {total_failures} failures used as warnings"
        else:
            return f"Mixed: {total_failures} failures with some learning, some caution"

    def score_employee_agency(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score employee agency in narratives.

        High agency: "We built/tried/implemented AI"
        Low agency: "AI was deployed/we were given/management introduced AI"

        Args:
            stories: All AI stories

        Returns:
            Agency score and analysis
        """
        agency_markers = {
            'high': ['we built', 'we created', 'we experimented', 'we tried', 'we implemented', 'we decided'],
            'low': ['was introduced', 'were told', 'management decided', 'given to us', 'deployed on us', 'had to']
        }

        high_agency_count = 0
        low_agency_count = 0

        for story in stories:
            text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()

            if any(marker in text for marker in agency_markers['high']):
                high_agency_count += 1
            if any(marker in text for marker in agency_markers['low']):
                low_agency_count += 1

        total = high_agency_count + low_agency_count
        agency_score = high_agency_count / total if total > 0 else 0.5

        return {
            'score': agency_score,
            'high_agency_stories': high_agency_count,
            'low_agency_stories': low_agency_count,
            'interpretation': self._interpret_agency_score(agency_score)
        }

    def _interpret_agency_score(self, score: float) -> str:
        """Generate interpretation of agency score."""
        if score > 0.6:
            return "High employee agency - innovation indicator"
        elif score < 0.4:
            return "Low employee agency - top-down culture"
        else:
            return "Mixed agency signals"

    def score_iteration_speed(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score how quickly the organization iterates based on narratives.

        Args:
            stories: All AI stories

        Returns:
            Iteration speed score
        """
        # Look for stories about rapid iteration
        rapid_iteration_count = 0
        slow_iteration_count = 0

        for story in stories:
            text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()

            if any(word in text for word in ['quick', 'rapid', 'fast', 'immediate', 'sprint']):
                rapid_iteration_count += 1
            if any(word in text for word in ['slow', 'delayed', 'waiting', 'approval', 'process']):
                slow_iteration_count += 1

        total = rapid_iteration_count + slow_iteration_count
        speed_score = rapid_iteration_count / total if total > 0 else 0.5

        return {
            'score': speed_score,
            'rapid_indicators': rapid_iteration_count,
            'slow_indicators': slow_iteration_count,
            'interpretation': 'Fast iteration culture' if speed_score > 0.6 else 'Slow iteration culture' if speed_score < 0.4 else 'Moderate iteration speed'
        }

    def score_narrative_diversity(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score diversity of narratives.

        More diverse perspectives indicate healthier innovation culture.

        Args:
            stories: All AI stories

        Returns:
            Diversity score
        """
        # Count unique groups telling stories
        unique_groups = set()
        for story in stories:
            dept = story.get('department')
            if dept:
                unique_groups.add(dept)

        # Count unique frames
        unique_frames = set()
        for story in stories:
            frame = story.get('narrative_function')
            if frame:
                unique_frames.add(frame)

        # Diversity score based on number of groups and frames
        group_diversity = min(len(unique_groups) / 8, 1.0)  # Normalize to 8 groups
        frame_diversity = min(len(unique_frames) / 4, 1.0)  # Normalize to 4 frames

        diversity_score = (group_diversity + frame_diversity) / 2

        return {
            'score': diversity_score,
            'unique_groups': len(unique_groups),
            'unique_frames': len(unique_frames),
            'interpretation': 'High narrative diversity - multiple perspectives' if diversity_score > 0.6 else 'Low diversity - limited perspectives'
        }

    def _aggregate_culture_score(self, scores: Dict[str, Dict[str, Any]]) -> float:
        """
        Aggregate dimension scores into overall culture score.

        Args:
            scores: Scores across dimensions

        Returns:
            Overall culture score (0-1)
        """
        weights = {
            'experimentation': 0.3,
            'failure_tolerance': 0.25,
            'agency': 0.2,
            'speed': 0.15,
            'diversity': 0.1
        }

        overall = sum(
            scores[dim]['score'] * weights[dim]
            for dim in scores
            if dim in weights
        )

        return min(overall, 1.0)

    def _extract_key_evidence(
        self,
        stories: List[Dict[str, Any]],
        scores: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Extract key evidence stories for each dimension."""
        evidence = {
            'experimentation': [],
            'failure_tolerance': [],
            'agency': []
        }

        # Get top exemplar stories for each dimension
        experiment_stories = [s for s in stories if self._is_experimentation_story(s)]
        if experiment_stories:
            evidence['experimentation'] = [s['id'] for s in experiment_stories[:3]]

        failure_stories = [s for s in stories if s.get('type') == 'failure']
        if failure_stories:
            evidence['failure_tolerance'] = [s['id'] for s in failure_stories[:3]]

        agency_stories = [s for s in stories if scores['agency']['score'] > 0.6]
        if agency_stories:
            evidence['agency'] = [s['id'] for s in agency_stories[:3]]

        return evidence

    def _classify_culture(self, overall_score: float) -> str:
        """Classify overall culture type based on score."""
        if overall_score > 0.7:
            return "Highly Innovative"
        elif overall_score > 0.5:
            return "Moderately Innovative"
        elif overall_score > 0.3:
            return "Cautiously Conservative"
        else:
            return "Risk Averse"

    def _generate_recommendations(self, scores: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on scores."""
        recommendations = []

        # Experimentation recommendations
        if scores['experimentation']['score'] < 0.5:
            recommendations.append("Encourage bottom-up experimentation with AI - create safe spaces for trials")

        # Failure tolerance recommendations
        if scores['failure_tolerance']['score'] < 0.5:
            recommendations.append("Reframe failures as learning opportunities - celebrate productive failures")

        # Agency recommendations
        if scores['agency']['score'] < 0.5:
            recommendations.append("Empower employees with more agency in AI adoption - reduce top-down mandates")

        # Speed recommendations
        if scores['speed']['score'] < 0.5:
            recommendations.append("Streamline approval processes to enable faster iteration")

        # Diversity recommendations
        if scores['diversity']['score'] < 0.5:
            recommendations.append("Encourage diverse perspectives - ensure all groups have voice in AI discussions")

        if not recommendations:
            recommendations.append("Culture shows good innovation indicators - maintain momentum")

        return recommendations

    def detect_risk_aversion_patterns(self) -> Dict[str, Any]:
        """
        Find evidence of risk-averse culture.

        Returns:
            Risk aversion analysis
        """
        # Get cautionary tales
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
          AND (s.why_told = 'warning' OR s.narrative_function = 'warning' OR s.type = 'failure')
        RETURN s
        ORDER BY s.timestamp DESC
        LIMIT 50
        """

        cautionary_tales = self.client.execute_read_query(query)
        cautionary_stories = [dict(r["s"]) for r in cautionary_tales]

        # Analyze patterns
        patterns = {
            'frequency': len(cautionary_stories),
            'distribution': self._analyze_distribution(cautionary_stories),
            'themes': self._extract_cautionary_themes(cautionary_stories),
            'impact': self._assess_cautionary_impact(cautionary_stories)
        }

        # Check if tales are blocking initiatives
        blocking_effect = self._measure_blocking_effect(cautionary_stories)

        return {
            'patterns': patterns,
            'blocking_effect': blocking_effect,
            'severity': self._assess_risk_aversion_severity(patterns, blocking_effect)
        }

    def _analyze_distribution(self, stories: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze distribution of cautionary tales across groups."""
        group_counts = Counter()

        for story in stories:
            dept = story.get('department', 'Unknown')
            group_counts[dept] += 1

        return dict(group_counts)

    def _extract_cautionary_themes(self, stories: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from cautionary tales."""
        all_themes = []

        for story in stories:
            themes = story.get('primary_themes', [])
            if isinstance(themes, list):
                all_themes.extend(themes)

        theme_counts = Counter(all_themes)
        return [theme for theme, count in theme_counts.most_common(5)]

    def _assess_cautionary_impact(self, stories: List[Dict[str, Any]]) -> str:
        """Assess impact of cautionary tales."""
        if len(stories) > 20:
            return "High - many cautionary tales circulating"
        elif len(stories) > 10:
            return "Moderate - some caution in narratives"
        else:
            return "Low - few cautionary tales"

    def _measure_blocking_effect(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Measure if cautionary tales are blocking initiatives."""
        # Check if stories mention blocked or cancelled initiatives
        blocking_count = 0

        for story in stories:
            text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()
            if any(word in text for word in ['cancelled', 'blocked', 'stopped', 'prevented', 'abandoned']):
                blocking_count += 1

        return {
            'blocking_stories': blocking_count,
            'is_blocking': blocking_count > len(stories) * 0.3,
            'severity': 'High' if blocking_count > 5 else 'Moderate' if blocking_count > 2 else 'Low'
        }

    def _assess_risk_aversion_severity(
        self,
        patterns: Dict[str, Any],
        blocking_effect: Dict[str, Any]
    ) -> str:
        """Assess overall risk aversion severity."""
        frequency = patterns['frequency']
        is_blocking = blocking_effect['is_blocking']

        if frequency > 20 and is_blocking:
            return "CRITICAL - High risk aversion blocking adoption"
        elif frequency > 10 or is_blocking:
            return "SIGNIFICANT - Notable risk aversion present"
        else:
            return "MODERATE - Some caution, manageable"
