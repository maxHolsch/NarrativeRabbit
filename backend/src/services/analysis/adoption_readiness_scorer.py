"""
AdoptionReadinessScorer - Sub-Agent 5

Scores organizational readiness for AI adoption across 6 dimensions:
1. Narrative Alignment - Group story compatibility
2. Cultural Receptivity - Innovation vs risk-aversion
3. Trust Levels - Trust in leadership and process
4. Learning Orientation - Growth mindset indicators
5. Leadership Coherence - Leadership narrative consistency
6. Coordination Narrative - Cross-group coordination

Also forecasts adoption trajectory based on current narrative patterns.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict
from datetime import datetime, timedelta


class AdoptionReadinessScorer:
    """
    Assesses organizational readiness for AI adoption by analyzing narrative patterns.

    Uses 6 dimensions to create comprehensive readiness score:
    - Narrative Alignment: Are stories compatible across groups?
    - Cultural Receptivity: Is culture innovation-friendly?
    - Trust: Do people trust leadership and process?
    - Learning: Is there growth mindset present?
    - Leadership Coherence: Do leaders tell consistent stories?
    - Coordination: Do groups coordinate well?
    """

    # Dimension weights for overall readiness calculation
    DIMENSION_WEIGHTS = {
        'narrative_alignment': 0.20,
        'cultural_receptivity': 0.20,
        'trust_levels': 0.20,
        'learning_orientation': 0.15,
        'leadership_coherence': 0.15,
        'coordination_narrative': 0.10
    }

    # Trust indicators in stories
    TRUST_SIGNALS = {
        'high': [
            'leadership understands',
            'clear direction',
            'transparent about',
            'listening to us',
            'following through',
            'trust the process',
            'confidence in leadership'
        ],
        'low': [
            'not sure why',
            'no clear plan',
            'not hearing us',
            'another initiative',
            'flavor of the month',
            'hiding information',
            'don\'t trust'
        ]
    }

    # Learning orientation markers
    LEARNING_SIGNALS = {
        'growth': [
            'learning as we go',
            'experimenting with',
            'trying different approaches',
            'feedback welcome',
            'getting better at',
            'still figuring out',
            'improving over time'
        ],
        'fixed': [
            'not my area',
            'not trained for this',
            'beyond my expertise',
            'someone else should',
            'can\'t learn',
            'too old for this',
            'not capable'
        ]
    }

    # Coordination indicators
    COORDINATION_SIGNALS = {
        'strong': [
            'working together',
            'aligned with',
            'coordinating across',
            'shared understanding',
            'consistent approach',
            'integrated effort',
            'cross-team collaboration'
        ],
        'weak': [
            'working in silos',
            'conflicting approaches',
            'different directions',
            'not coordinated',
            'fragmented effort',
            'lack of alignment',
            'isolated teams'
        ]
    }

    def __init__(self, neo4j_client):
        """
        Initialize the AdoptionReadinessScorer.

        Args:
            neo4j_client: Neo4j database client for querying narrative data
        """
        self.neo4j = neo4j_client

    # ==================== MAIN ASSESSMENT METHOD ====================

    def assess_readiness(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive readiness assessment across all 6 dimensions.

        Returns overall readiness score (0-1) with:
        - Dimension-level scores
        - Key evidence for each dimension
        - Readiness classification
        - Detailed recommendations
        - Forecast of adoption trajectory

        Args:
            initiative_id: Optional specific initiative to assess

        Returns:
            Dict with overall_score, dimension_scores, evidence, classification,
            recommendations, and forecast
        """
        stories = self._get_initiative_stories(initiative_id) if initiative_id else self._get_all_ai_stories()

        if not stories:
            return {
                'overall_score': 0.0,
                'dimension_scores': {},
                'classification': 'insufficient_data',
                'interpretation': 'Not enough stories to assess readiness'
            }

        # Score each dimension
        dimension_scores = {
            'narrative_alignment': self.score_narrative_alignment(stories),
            'cultural_receptivity': self.score_cultural_receptivity(stories),
            'trust_levels': self.score_trust_levels(stories),
            'learning_orientation': self.score_learning_orientation(stories),
            'leadership_coherence': self.score_leadership_coherence(stories),
            'coordination_narrative': self.score_coordination_narrative(stories)
        }

        # Calculate weighted overall score
        overall_score = sum(
            dimension_scores[dim]['score'] * self.DIMENSION_WEIGHTS[dim]
            for dim in dimension_scores
        )

        # Get trajectory forecast
        forecast = self.forecast_adoption_trajectory(stories, dimension_scores)

        return {
            'overall_score': round(overall_score, 3),
            'dimension_scores': dimension_scores,
            'classification': self._classify_readiness(overall_score),
            'interpretation': self._interpret_overall_readiness(overall_score, dimension_scores),
            'strengths': self._identify_strengths(dimension_scores),
            'weaknesses': self._identify_weaknesses(dimension_scores),
            'recommendations': self._generate_readiness_recommendations(dimension_scores),
            'forecast': forecast,
            'story_count': len(stories),
            'assessed_at': datetime.now().isoformat()
        }

    # ==================== DIMENSION SCORING METHODS ====================

    def score_narrative_alignment(self, stories: List[Dict]) -> Dict[str, Any]:
        """
        Score how compatible stories are across different groups.

        High alignment = groups telling similar stories about AI
        Low alignment = conflicting or contradictory narratives

        Returns:
            Dict with score, evidence, and interpretation
        """
        # Group stories by teller group
        group_stories = defaultdict(list)
        for story in stories:
            group = self._get_teller_group(story)
            group_stories[group].append(story)

        if len(group_stories) < 2:
            return {
                'score': 0.5,
                'evidence': [],
                'interpretation': 'Not enough groups for alignment assessment'
            }

        # Compare frames, sentiment, and themes across groups
        alignment_scores = []
        evidence = []

        groups = list(group_stories.keys())
        for i, group1 in enumerate(groups):
            for group2 in groups[i+1:]:
                stories1 = group_stories[group1]
                stories2 = group_stories[group2]

                # Frame alignment
                frame_alignment = self._compare_group_frames(stories1, stories2)

                # Sentiment alignment
                sentiment_alignment = self._compare_group_sentiment(stories1, stories2)

                # Theme alignment
                theme_alignment = self._compare_group_themes(stories1, stories2)

                # Aggregate alignment for this pair
                pair_alignment = (frame_alignment + sentiment_alignment + theme_alignment) / 3
                alignment_scores.append(pair_alignment)

                evidence.append({
                    'groups': [group1, group2],
                    'alignment': round(pair_alignment, 3),
                    'frame_alignment': round(frame_alignment, 3),
                    'sentiment_alignment': round(sentiment_alignment, 3),
                    'theme_alignment': round(theme_alignment, 3)
                })

        overall_alignment = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.5

        return {
            'score': round(overall_alignment, 3),
            'evidence': evidence,
            'group_count': len(group_stories),
            'comparison_count': len(evidence),
            'interpretation': self._interpret_narrative_alignment(overall_alignment, evidence)
        }

    def score_cultural_receptivity(self, stories: List[Dict]) -> Dict[str, Any]:
        """
        Score cultural openness to innovation and change.

        Leverages CulturalSignalDetector patterns but focuses on readiness implications.

        Returns:
            Dict with score, evidence, and interpretation
        """
        innovation_indicators = 0
        risk_aversion_indicators = 0
        evidence = []

        for story in stories:
            # Check for innovation signals
            innovation_signals = self._detect_innovation_signals(story)
            if innovation_signals:
                innovation_indicators += len(innovation_signals)
                evidence.append({
                    'story_id': story['id'],
                    'type': 'innovation',
                    'signals': innovation_signals
                })

            # Check for risk aversion signals
            risk_signals = self._detect_risk_aversion_signals(story)
            if risk_signals:
                risk_aversion_indicators += len(risk_signals)
                evidence.append({
                    'story_id': story['id'],
                    'type': 'risk_aversion',
                    'signals': risk_signals
                })

        # Calculate receptivity score
        total_signals = innovation_indicators + risk_aversion_indicators
        if total_signals == 0:
            receptivity_score = 0.5
        else:
            receptivity_score = innovation_indicators / total_signals

        return {
            'score': round(receptivity_score, 3),
            'innovation_indicators': innovation_indicators,
            'risk_aversion_indicators': risk_aversion_indicators,
            'evidence': evidence[:10],  # Top 10 examples
            'interpretation': self._interpret_cultural_receptivity(receptivity_score, innovation_indicators, risk_aversion_indicators)
        }

    def score_trust_levels(self, stories: List[Dict]) -> Dict[str, Any]:
        """
        Score trust in leadership and organizational processes.

        High trust = readiness to follow leadership into AI adoption
        Low trust = skepticism and resistance likely

        Returns:
            Dict with score, evidence, and interpretation
        """
        high_trust_count = 0
        low_trust_count = 0
        evidence = []

        for story in stories:
            content = story.get('content', '').lower()

            # Check for high trust signals
            high_signals = [signal for signal in self.TRUST_SIGNALS['high'] if signal in content]
            if high_signals:
                high_trust_count += len(high_signals)
                evidence.append({
                    'story_id': story['id'],
                    'group': self._get_teller_group(story),
                    'type': 'high_trust',
                    'signals': high_signals
                })

            # Check for low trust signals
            low_signals = [signal for signal in self.TRUST_SIGNALS['low'] if signal in content]
            if low_signals:
                low_trust_count += len(low_signals)
                evidence.append({
                    'story_id': story['id'],
                    'group': self._get_teller_group(story),
                    'type': 'low_trust',
                    'signals': low_signals
                })

        # Calculate trust score
        total_signals = high_trust_count + low_trust_count
        if total_signals == 0:
            trust_score = 0.5
        else:
            trust_score = high_trust_count / total_signals

        return {
            'score': round(trust_score, 3),
            'high_trust_signals': high_trust_count,
            'low_trust_signals': low_trust_count,
            'evidence': evidence[:10],
            'interpretation': self._interpret_trust_levels(trust_score, high_trust_count, low_trust_count)
        }

    def score_learning_orientation(self, stories: List[Dict]) -> Dict[str, Any]:
        """
        Score growth mindset vs. fixed mindset in organization.

        Growth mindset = readiness to learn new AI skills
        Fixed mindset = belief that capabilities are unchangeable

        Returns:
            Dict with score, evidence, and interpretation
        """
        growth_signals = 0
        fixed_signals = 0
        evidence = []

        for story in stories:
            content = story.get('content', '').lower()

            # Check for growth mindset signals
            growth_markers = [signal for signal in self.LEARNING_SIGNALS['growth'] if signal in content]
            if growth_markers:
                growth_signals += len(growth_markers)
                evidence.append({
                    'story_id': story['id'],
                    'group': self._get_teller_group(story),
                    'type': 'growth',
                    'markers': growth_markers
                })

            # Check for fixed mindset signals
            fixed_markers = [signal for signal in self.LEARNING_SIGNALS['fixed'] if signal in content]
            if fixed_markers:
                fixed_signals += len(fixed_markers)
                evidence.append({
                    'story_id': story['id'],
                    'group': self._get_teller_group(story),
                    'type': 'fixed',
                    'markers': fixed_markers
                })

        # Calculate learning orientation score
        total_signals = growth_signals + fixed_signals
        if total_signals == 0:
            learning_score = 0.5
        else:
            learning_score = growth_signals / total_signals

        return {
            'score': round(learning_score, 3),
            'growth_signals': growth_signals,
            'fixed_signals': fixed_signals,
            'evidence': evidence[:10],
            'interpretation': self._interpret_learning_orientation(learning_score, growth_signals, fixed_signals)
        }

    def score_leadership_coherence(self, stories: List[Dict]) -> Dict[str, Any]:
        """
        Score consistency and alignment of leadership narratives.

        High coherence = leaders telling unified story
        Low coherence = conflicting messages from leadership

        Returns:
            Dict with score, evidence, and interpretation
        """
        # Identify leadership stories
        leadership_stories = [s for s in stories if self._is_leadership_story(s)]

        if len(leadership_stories) < 2:
            return {
                'score': 0.5,
                'evidence': [],
                'interpretation': 'Insufficient leadership stories for coherence assessment'
            }

        # Compare frames used by leaders
        frame_consistency = self._measure_frame_consistency(leadership_stories)

        # Compare sentiment alignment
        sentiment_consistency = self._measure_sentiment_consistency(leadership_stories)

        # Compare message themes
        theme_consistency = self._measure_theme_consistency(leadership_stories)

        # Aggregate coherence score
        coherence_score = (frame_consistency + sentiment_consistency + theme_consistency) / 3

        evidence = {
            'leadership_story_count': len(leadership_stories),
            'frame_consistency': round(frame_consistency, 3),
            'sentiment_consistency': round(sentiment_consistency, 3),
            'theme_consistency': round(theme_consistency, 3),
            'sample_stories': [s['id'] for s in leadership_stories[:5]]
        }

        return {
            'score': round(coherence_score, 3),
            'evidence': evidence,
            'interpretation': self._interpret_leadership_coherence(coherence_score, evidence)
        }

    def score_coordination_narrative(self, stories: List[Dict]) -> Dict[str, Any]:
        """
        Score evidence of cross-group coordination in narratives.

        Strong coordination = stories reference collaboration and alignment
        Weak coordination = stories suggest siloed work and fragmentation

        Returns:
            Dict with score, evidence, and interpretation
        """
        strong_signals = 0
        weak_signals = 0
        evidence = []

        for story in stories:
            content = story.get('content', '').lower()

            # Check for strong coordination signals
            strong_markers = [signal for signal in self.COORDINATION_SIGNALS['strong'] if signal in content]
            if strong_markers:
                strong_signals += len(strong_markers)
                evidence.append({
                    'story_id': story['id'],
                    'group': self._get_teller_group(story),
                    'type': 'strong_coordination',
                    'markers': strong_markers
                })

            # Check for weak coordination signals
            weak_markers = [signal for signal in self.COORDINATION_SIGNALS['weak'] if signal in content]
            if weak_markers:
                weak_signals += len(weak_markers)
                evidence.append({
                    'story_id': story['id'],
                    'group': self._get_teller_group(story),
                    'type': 'weak_coordination',
                    'markers': weak_markers
                })

        # Calculate coordination score
        total_signals = strong_signals + weak_signals
        if total_signals == 0:
            coordination_score = 0.5
        else:
            coordination_score = strong_signals / total_signals

        return {
            'score': round(coordination_score, 3),
            'strong_signals': strong_signals,
            'weak_signals': weak_signals,
            'evidence': evidence[:10],
            'interpretation': self._interpret_coordination_narrative(coordination_score, strong_signals, weak_signals)
        }

    # ==================== FORECASTING METHOD ====================

    def forecast_adoption_trajectory(self, stories: List[Dict], dimension_scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forecast likely adoption trajectory based on current narrative patterns.

        Analyzes:
        - Current momentum (story volume and sentiment trends)
        - Dimension trends (improving or declining)
        - Critical barriers (which dimensions are blockers)
        - Likely timeline (fast/moderate/slow/stalled)

        Returns:
            Dict with trajectory prediction, timeline estimate, key factors, and risks
        """
        # Analyze story volume trends
        volume_trend = self._analyze_story_volume_trend(stories)

        # Analyze sentiment trends
        sentiment_trend = self._analyze_sentiment_trend(stories)

        # Identify critical barriers (dimensions below 0.4)
        critical_barriers = [
            dim for dim, data in dimension_scores.items()
            if data['score'] < 0.4
        ]

        # Identify strengths (dimensions above 0.7)
        strengths = [
            dim for dim, data in dimension_scores.items()
            if data['score'] > 0.7
        ]

        # Calculate momentum score
        momentum = self._calculate_momentum(volume_trend, sentiment_trend, dimension_scores)

        # Predict trajectory
        trajectory = self._predict_trajectory(momentum, critical_barriers, strengths)

        return {
            'trajectory': trajectory,
            'momentum_score': round(momentum, 3),
            'volume_trend': volume_trend,
            'sentiment_trend': sentiment_trend,
            'critical_barriers': critical_barriers,
            'strengths': strengths,
            'timeline_estimate': self._estimate_timeline(trajectory, critical_barriers),
            'confidence': self._calculate_forecast_confidence(len(stories)),
            'key_factors': self._identify_key_factors(dimension_scores, critical_barriers, strengths),
            'risks': self._identify_forecast_risks(critical_barriers, momentum)
        }

    # ==================== HELPER METHODS ====================

    def _get_all_ai_stories(self) -> List[Dict]:
        """Fetch all AI-related stories from the graph."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
        RETURN s
        LIMIT 1000
        """
        results = self.neo4j.execute_read_query(query)
        return [record['s'] for record in results]

    def _get_initiative_stories(self, initiative_id: str) -> List[Dict]:
        """Fetch stories related to a specific AI initiative."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
        RETURN s
        LIMIT 500
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return [record['s'] for record in results]

    def _get_teller_group(self, story: Dict) -> str:
        """Extract the teller's group from story metadata."""
        return story.get('teller_group', 'unknown')

    def _compare_group_frames(self, stories1: List[Dict], stories2: List[Dict]) -> float:
        """Compare dominant frames between two groups' stories."""
        frames1 = defaultdict(int)
        frames2 = defaultdict(int)

        for story in stories1:
            frame = story.get('agency_frame', 'unknown')
            frames1[frame] += 1

        for story in stories2:
            frame = story.get('agency_frame', 'unknown')
            frames2[frame] += 1

        # Find dominant frames
        dominant1 = max(frames1, key=frames1.get) if frames1 else None
        dominant2 = max(frames2, key=frames2.get) if frames2 else None

        # Perfect alignment if same dominant frame
        if dominant1 == dominant2:
            return 1.0

        # Partial alignment based on frame distribution overlap
        all_frames = set(frames1.keys()) | set(frames2.keys())
        if not all_frames:
            return 0.5

        overlap = sum(min(frames1.get(f, 0), frames2.get(f, 0)) for f in all_frames)
        total = sum(frames1.values()) + sum(frames2.values())

        return (2 * overlap) / total if total > 0 else 0.5

    def _compare_group_sentiment(self, stories1: List[Dict], stories2: List[Dict]) -> float:
        """Compare sentiment patterns between two groups."""
        sentiments1 = [s.get('ai_sentiment', 0) for s in stories1 if s.get('ai_sentiment') is not None]
        sentiments2 = [s.get('ai_sentiment', 0) for s in stories2 if s.get('ai_sentiment') is not None]

        if not sentiments1 or not sentiments2:
            return 0.5

        avg1 = sum(sentiments1) / len(sentiments1)
        avg2 = sum(sentiments2) / len(sentiments2)

        # Convert difference to alignment score (0 diff = 1.0, max diff of 2 = 0.0)
        diff = abs(avg1 - avg2)
        alignment = 1.0 - (diff / 2.0)

        return max(0.0, min(1.0, alignment))

    def _compare_group_themes(self, stories1: List[Dict], stories2: List[Dict]) -> float:
        """Compare themes/concepts mentioned between two groups."""
        themes1 = set()
        themes2 = set()

        for story in stories1:
            themes1.update(story.get('ai_concepts_mentioned', []))

        for story in stories2:
            themes2.update(story.get('ai_concepts_mentioned', []))

        if not themes1 and not themes2:
            return 0.5

        intersection = themes1 & themes2
        union = themes1 | themes2

        return len(intersection) / len(union) if union else 0.5

    def _detect_innovation_signals(self, story: Dict) -> List[str]:
        """Detect innovation-positive signals in a story."""
        signals = []
        content = story.get('content', '').lower()

        innovation_markers = [
            'experiment', 'try new', 'innovative', 'creative',
            'learning', 'iterate', 'improve', 'opportunity'
        ]

        for marker in innovation_markers:
            if marker in content:
                signals.append(marker)

        return signals

    def _detect_risk_aversion_signals(self, story: Dict) -> List[str]:
        """Detect risk-averse signals in a story."""
        signals = []
        content = story.get('content', '').lower()

        risk_markers = [
            'risky', 'dangerous', 'careful', 'cautious',
            'proven', 'traditional', 'safe', 'avoid'
        ]

        for marker in risk_markers:
            if marker in content:
                signals.append(marker)

        return signals

    def _is_leadership_story(self, story: Dict) -> bool:
        """Determine if a story comes from leadership."""
        group = self._get_teller_group(story)
        leadership_groups = ['leadership', 'executive', 'senior_management', 'c_suite']
        return any(leader_group in group.lower() for leader_group in leadership_groups)

    def _measure_frame_consistency(self, stories: List[Dict]) -> float:
        """Measure consistency of frames used across stories."""
        frames = [s.get('agency_frame', 'unknown') for s in stories]
        if not frames:
            return 0.5

        # Most common frame
        frame_counts = defaultdict(int)
        for frame in frames:
            frame_counts[frame] += 1

        most_common_count = max(frame_counts.values())
        consistency = most_common_count / len(frames)

        return consistency

    def _measure_sentiment_consistency(self, stories: List[Dict]) -> float:
        """Measure consistency of sentiment across stories."""
        sentiments = [s.get('ai_sentiment', 0) for s in stories if s.get('ai_sentiment') is not None]
        if len(sentiments) < 2:
            return 0.5

        # Calculate standard deviation normalized to 0-1 scale
        avg = sum(sentiments) / len(sentiments)
        variance = sum((s - avg) ** 2 for s in sentiments) / len(sentiments)
        std_dev = variance ** 0.5

        # Low std dev = high consistency (max std dev is 1.0 for sentiment range -1 to 1)
        consistency = 1.0 - min(std_dev, 1.0)

        return consistency

    def _measure_theme_consistency(self, stories: List[Dict]) -> float:
        """Measure consistency of themes/concepts across stories."""
        all_themes = []
        for story in stories:
            all_themes.extend(story.get('ai_concepts_mentioned', []))

        if not all_themes:
            return 0.5

        # Count theme frequencies
        theme_counts = defaultdict(int)
        for theme in all_themes:
            theme_counts[theme] += 1

        # Measure how concentrated themes are (high concentration = high consistency)
        total = len(all_themes)
        unique = len(theme_counts)

        # Normalized concentration score
        consistency = 1.0 - (unique / total) if total > 0 else 0.5

        return max(0.0, min(1.0, consistency))

    def _analyze_story_volume_trend(self, stories: List[Dict]) -> str:
        """Analyze whether story volume is increasing, stable, or decreasing."""
        # Group stories by time period (simplified - assumes timestamp field)
        if not stories or 'timestamp' not in stories[0]:
            return 'unknown'

        # Sort by timestamp
        sorted_stories = sorted(stories, key=lambda s: s.get('timestamp', ''))

        # Split into early and late halves
        mid = len(sorted_stories) // 2
        early_count = mid
        late_count = len(sorted_stories) - mid

        # Compare volumes
        if late_count > early_count * 1.2:
            return 'increasing'
        elif late_count < early_count * 0.8:
            return 'decreasing'
        else:
            return 'stable'

    def _analyze_sentiment_trend(self, stories: List[Dict]) -> str:
        """Analyze whether sentiment is improving, stable, or declining."""
        sentiments = [(s.get('timestamp', ''), s.get('ai_sentiment', 0))
                     for s in stories if s.get('ai_sentiment') is not None]

        if len(sentiments) < 4:
            return 'unknown'

        # Sort by timestamp
        sentiments.sort(key=lambda x: x[0])

        # Compare early vs late sentiment
        mid = len(sentiments) // 2
        early_avg = sum(s[1] for s in sentiments[:mid]) / mid
        late_avg = sum(s[1] for s in sentiments[mid:]) / (len(sentiments) - mid)

        if late_avg > early_avg + 0.1:
            return 'improving'
        elif late_avg < early_avg - 0.1:
            return 'declining'
        else:
            return 'stable'

    def _calculate_momentum(self, volume_trend: str, sentiment_trend: str,
                           dimension_scores: Dict[str, Any]) -> float:
        """Calculate overall momentum score based on trends."""
        momentum = 0.5  # Base momentum

        # Volume trend contribution
        if volume_trend == 'increasing':
            momentum += 0.15
        elif volume_trend == 'decreasing':
            momentum -= 0.15

        # Sentiment trend contribution
        if sentiment_trend == 'improving':
            momentum += 0.20
        elif sentiment_trend == 'declining':
            momentum -= 0.20

        # Dimension scores contribution (average)
        avg_dimension = sum(d['score'] for d in dimension_scores.values()) / len(dimension_scores)
        momentum += (avg_dimension - 0.5) * 0.3

        return max(0.0, min(1.0, momentum))

    def _predict_trajectory(self, momentum: float, critical_barriers: List[str],
                           strengths: List[str]) -> str:
        """Predict adoption trajectory based on momentum and barriers."""
        if len(critical_barriers) >= 3:
            return 'stalled'
        elif len(critical_barriers) >= 2:
            return 'slow'
        elif momentum > 0.7 and len(strengths) >= 3:
            return 'accelerating'
        elif momentum > 0.6:
            return 'steady'
        elif momentum > 0.4:
            return 'moderate'
        else:
            return 'at_risk'

    def _estimate_timeline(self, trajectory: str, critical_barriers: List[str]) -> str:
        """Estimate timeline to full adoption based on trajectory."""
        timeline_map = {
            'accelerating': '3-6 months',
            'steady': '6-12 months',
            'moderate': '12-18 months',
            'slow': '18-24 months',
            'at_risk': '24+ months or may not succeed',
            'stalled': 'Indefinite - intervention required'
        }
        return timeline_map.get(trajectory, 'unknown')

    def _calculate_forecast_confidence(self, story_count: int) -> str:
        """Calculate confidence level in forecast based on data volume."""
        if story_count >= 100:
            return 'high'
        elif story_count >= 50:
            return 'medium'
        elif story_count >= 20:
            return 'low'
        else:
            return 'very_low'

    def _identify_key_factors(self, dimension_scores: Dict[str, Any],
                            critical_barriers: List[str], strengths: List[str]) -> List[str]:
        """Identify key factors influencing trajectory."""
        factors = []

        if strengths:
            factors.append(f"Strong {', '.join(strengths)} provide foundation")

        if critical_barriers:
            factors.append(f"Critical barriers in {', '.join(critical_barriers)} must be addressed")

        # Find dimensions near tipping point (0.45-0.55)
        tipping_point = [
            dim for dim, data in dimension_scores.items()
            if 0.45 <= data['score'] <= 0.55
        ]
        if tipping_point:
            factors.append(f"{', '.join(tipping_point)} at tipping point - small changes can shift trajectory")

        return factors

    def _identify_forecast_risks(self, critical_barriers: List[str], momentum: float) -> List[str]:
        """Identify risks that could derail adoption."""
        risks = []

        if 'trust_levels' in critical_barriers:
            risks.append("Low trust could trigger active resistance if not addressed")

        if 'leadership_coherence' in critical_barriers:
            risks.append("Inconsistent leadership messaging creates confusion and delays")

        if 'coordination_narrative' in critical_barriers:
            risks.append("Poor coordination may lead to fragmented implementation and wasted effort")

        if momentum < 0.3:
            risks.append("Very low momentum - initiative may lose visibility and support")

        if not risks:
            risks.append("No critical risks identified - maintain current trajectory")

        return risks

    # ==================== INTERPRETATION METHODS ====================

    def _classify_readiness(self, overall_score: float) -> str:
        """Classify overall readiness level."""
        if overall_score >= 0.75:
            return 'highly_ready'
        elif overall_score >= 0.60:
            return 'ready'
        elif overall_score >= 0.45:
            return 'moderately_ready'
        elif overall_score >= 0.30:
            return 'limited_readiness'
        else:
            return 'not_ready'

    def _interpret_overall_readiness(self, overall_score: float,
                                    dimension_scores: Dict[str, Any]) -> str:
        """Generate human-readable interpretation of overall readiness."""
        classification = self._classify_readiness(overall_score)

        interpretations = {
            'highly_ready': "Organization shows strong readiness across all dimensions. Conditions are favorable for successful AI adoption.",
            'ready': "Organization is ready for AI adoption with some areas needing attention. Proceed with monitoring of weaker dimensions.",
            'moderately_ready': "Organization has mixed readiness. Address critical gaps before full-scale rollout to improve success probability.",
            'limited_readiness': "Organization faces significant readiness challenges. Targeted interventions required before proceeding.",
            'not_ready': "Organization is not ready for AI adoption. Fundamental cultural or structural issues must be addressed first."
        }

        return interpretations.get(classification, 'Unable to determine readiness')

    def _identify_strengths(self, dimension_scores: Dict[str, Any]) -> List[str]:
        """Identify readiness strengths (dimensions > 0.7)."""
        return [dim for dim, data in dimension_scores.items() if data['score'] > 0.7]

    def _identify_weaknesses(self, dimension_scores: Dict[str, Any]) -> List[str]:
        """Identify readiness weaknesses (dimensions < 0.4)."""
        return [dim for dim, data in dimension_scores.items() if data['score'] < 0.4]

    def _generate_readiness_recommendations(self, dimension_scores: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on dimension scores."""
        recommendations = []

        for dim, data in dimension_scores.items():
            score = data['score']

            if score < 0.4:
                recommendations.append(self._get_dimension_recommendation(dim, 'critical'))
            elif score < 0.6:
                recommendations.append(self._get_dimension_recommendation(dim, 'moderate'))

        if not recommendations:
            recommendations.append("All dimensions show adequate readiness. Focus on maintaining momentum and addressing any emerging issues quickly.")

        return recommendations

    def _get_dimension_recommendation(self, dimension: str, severity: str) -> str:
        """Get specific recommendation for a dimension based on severity."""
        recommendations = {
            'narrative_alignment': {
                'critical': "CRITICAL: Facilitate cross-group dialogue to align narratives. Create shared experiences and common language.",
                'moderate': "Improve narrative alignment through shared storytelling sessions and cross-functional teams."
            },
            'cultural_receptivity': {
                'critical': "CRITICAL: Address risk-averse culture through small wins, pilot projects, and celebration of learning.",
                'moderate': "Enhance innovation culture by showcasing successful experiments and reducing fear of failure."
            },
            'trust_levels': {
                'critical': "CRITICAL: Rebuild trust through transparency, consistent communication, and demonstrating follow-through on commitments.",
                'moderate': "Improve trust by increasing leadership visibility and creating feedback loops."
            },
            'learning_orientation': {
                'critical': "CRITICAL: Shift to growth mindset through training, mentorship, and rewarding learning behaviors.",
                'moderate': "Strengthen learning culture with skill development opportunities and knowledge sharing."
            },
            'leadership_coherence': {
                'critical': "CRITICAL: Align leadership messaging immediately. Create unified talking points and coordinated communication plan.",
                'moderate': "Improve leadership alignment through regular coordination meetings and shared messaging framework."
            },
            'coordination_narrative': {
                'critical': "CRITICAL: Establish cross-functional coordination mechanisms and shared goals to break down silos.",
                'moderate': "Enhance coordination through regular cross-team meetings and shared success metrics."
            }
        }

        return recommendations.get(dimension, {}).get(severity, f"Address {dimension} issues")

    def _interpret_narrative_alignment(self, score: float, evidence: List[Dict]) -> str:
        """Interpret narrative alignment score."""
        if score >= 0.7:
            return "Strong narrative alignment across groups. Stories are compatible and mutually reinforcing."
        elif score >= 0.5:
            return "Moderate alignment with some inconsistencies. Groups generally agree but with different emphases."
        elif score >= 0.3:
            return "Weak alignment. Groups telling different stories about AI with potential conflicts."
        else:
            return "Poor alignment. Conflicting narratives across groups indicate fundamental disagreements."

    def _interpret_cultural_receptivity(self, score: float, innovation: int, risk: int) -> str:
        """Interpret cultural receptivity score."""
        if score >= 0.7:
            return f"Strong innovation culture ({innovation} innovation signals vs {risk} risk signals). Organization embraces change."
        elif score >= 0.5:
            return f"Balanced culture ({innovation} innovation vs {risk} risk signals). Some openness with reasonable caution."
        elif score >= 0.3:
            return f"Risk-averse tendency ({innovation} innovation vs {risk} risk signals). Caution outweighs experimentation."
        else:
            return f"Highly risk-averse culture ({innovation} innovation vs {risk} risk signals). Significant barrier to AI adoption."

    def _interpret_trust_levels(self, score: float, high: int, low: int) -> str:
        """Interpret trust levels score."""
        if score >= 0.7:
            return f"High trust in leadership ({high} positive vs {low} negative signals). Strong foundation for change."
        elif score >= 0.5:
            return f"Moderate trust ({high} positive vs {low} negative signals). Leadership credibility is adequate but fragile."
        elif score >= 0.3:
            return f"Low trust ({high} positive vs {low} negative signals). Skepticism toward leadership decisions."
        else:
            return f"Very low trust ({high} positive vs {low} negative signals). Major credibility issues must be addressed."

    def _interpret_learning_orientation(self, score: float, growth: int, fixed: int) -> str:
        """Interpret learning orientation score."""
        if score >= 0.7:
            return f"Strong growth mindset ({growth} growth vs {fixed} fixed signals). Organization ready to learn new skills."
        elif score >= 0.5:
            return f"Mixed mindset ({growth} growth vs {fixed} fixed signals). Some learning resistance exists."
        elif score >= 0.3:
            return f"Fixed mindset tendency ({growth} growth vs {fixed} fixed signals). Belief that capabilities are unchangeable."
        else:
            return f"Strong fixed mindset ({growth} growth vs {fixed} fixed signals). Major barrier to skill development."

    def _interpret_leadership_coherence(self, score: float, evidence: Dict) -> str:
        """Interpret leadership coherence score."""
        if score >= 0.7:
            return f"High leadership coherence ({evidence['leadership_story_count']} stories analyzed). Leaders deliver consistent message."
        elif score >= 0.5:
            return f"Moderate coherence ({evidence['leadership_story_count']} stories). Some inconsistency in leadership messaging."
        elif score >= 0.3:
            return f"Low coherence ({evidence['leadership_story_count']} stories). Leaders sending mixed messages."
        else:
            return f"Poor coherence ({evidence['leadership_story_count']} stories). Leadership narratives are contradictory."

    def _interpret_coordination_narrative(self, score: float, strong: int, weak: int) -> str:
        """Interpret coordination narrative score."""
        if score >= 0.7:
            return f"Strong coordination signals ({strong} positive vs {weak} negative). Stories indicate effective collaboration."
        elif score >= 0.5:
            return f"Moderate coordination ({strong} positive vs {weak} negative). Some collaboration with room for improvement."
        elif score >= 0.3:
            return f"Weak coordination ({strong} positive vs {weak} negative). Stories suggest siloed work."
        else:
            return f"Very weak coordination ({strong} positive vs {weak} negative). Fragmented effort across organization."
