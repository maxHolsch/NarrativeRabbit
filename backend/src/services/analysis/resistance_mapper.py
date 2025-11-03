"""
Resistance Mapper - Sub-Agent for AI Narrative Intelligence System.

Maps resistance patterns across the organization and identifies root causes.
Shows where and why AI adoption is stalling.
"""
from typing import List, Dict, Any, Optional, Set, Tuple
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
    - Root causes of resistance
    - Whether resistance is spreading through narrative contagion
    - Blocking effects on initiatives
    """

    # Define resistance patterns with markers
    RESISTANCE_PATTERNS = {
        'passive': {
            'markers': ['waiting to see', 'not prioritized', 'when we have time', 'eventually', 'someday'],
            'severity': 'low',
            'description': 'Passive resistance - delaying without active opposition'
        },
        'skeptical': {
            'markers': ['not convinced', 'needs proof', "where's the evidence", 'show me', 'prove it'],
            'severity': 'medium',
            'description': 'Skeptical resistance - requires evidence before buy-in'
        },
        'active': {
            'markers': ["won't work here", 'tried before', 'fundamentally flawed', 'waste of time', 'wrong approach'],
            'severity': 'high',
            'description': 'Active resistance - direct opposition'
        },
        'fearful': {
            'markers': ['worried about', 'concerned that', 'might lose', 'afraid', 'anxious', 'threatened'],
            'severity': 'high',
            'description': 'Fearful resistance - anxiety-driven opposition'
        }
    }

    def __init__(self):
        """Initialize the resistance mapper."""
        self.client = neo4j_client

    def map_resistance_landscape(self) -> Dict[str, Any]:
        """
        Map resistance across all groups.

        Returns:
            Complete resistance landscape with hotspots and patterns
        """
        # Get all groups
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

        # Identify resistance hotspots
        hotspots = self._identify_hotspots(resistance_map)

        # Find common patterns across groups
        common_patterns = self._find_common_patterns(resistance_map)

        # Analyze if resistance is spreading
        network_effects = self.analyze_resistance_spread(resistance_map)

        return {
            'by_group': resistance_map,
            'hotspots': hotspots,
            'common_patterns': common_patterns,
            'network_effects': network_effects,
            'overall_severity': self._assess_overall_severity(resistance_map),
            'recommendations': self._generate_landscape_recommendations(resistance_map, hotspots)
        }

    def _get_all_groups(self) -> List[str]:
        """Get all group names from the graph."""
        query = """
        MATCH (g:Group)
        RETURN g.name as name
        ORDER BY name
        """
        results = self.client.execute_read_query(query)
        return [r['name'] for r in results]

    def _calculate_resistance_score(self, group: str) -> float:
        """
        Calculate overall resistance score for a group (0-1 scale).

        Higher score = more resistance

        Args:
            group: Group name

        Returns:
            Resistance score
        """
        group_stories = self._get_group_ai_stories(group)

        if not group_stories:
            return 0.5  # Neutral if no data

        # Count resistance indicators
        resistance_count = 0
        support_count = 0

        for story in group_stories:
            sentiment = story.get('ai_sentiment', 0)
            text = story.get('summary', '').lower()

            # Resistance indicators
            if sentiment < -0.2:
                resistance_count += 1
            if story.get('narrative_function') == 'warning':
                resistance_count += 1
            if any(self._has_resistance_marker(text, pattern['markers'])
                   for pattern in self.RESISTANCE_PATTERNS.values()):
                resistance_count += 1

            # Support indicators
            if sentiment > 0.2:
                support_count += 1
            if story.get('experimentation_indicator'):
                support_count += 1

        total = resistance_count + support_count
        resistance_score = resistance_count / total if total > 0 else 0.5

        return min(resistance_score, 1.0)

    def _has_resistance_marker(self, text: str, markers: List[str]) -> bool:
        """Check if text contains any resistance markers."""
        return any(marker in text for marker in markers)

    def _get_group_ai_stories(self, group: str) -> List[Dict[str, Any]]:
        """Get AI-related stories from a specific group."""
        query = """
        MATCH (g:Group {name: $group})<-[:BELONGS_TO]-(p:Person)-[:TELLS]->(s:Story)
        WHERE s.ai_related = true
        RETURN s
        ORDER BY s.timestamp DESC
        LIMIT 50
        """
        results = self.client.execute_read_query(query, {"group": group})
        return [dict(r["s"]) for r in results]

    def identify_resistance_patterns(self, group: str) -> List[Dict[str, Any]]:
        """
        Identify specific resistance patterns in a group.

        Args:
            group: Group name

        Returns:
            List of detected resistance patterns with evidence
        """
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
                    'description': pattern_def['description'],
                    'frequency': len(matches),
                    'percentage': len(matches) / len(group_stories) if group_stories else 0,
                    'examples': [
                        {
                            'story_id': s['id'],
                            'summary': s.get('summary', '')[:100]
                        }
                        for s in matches[:3]
                    ]
                })

        # Sort by frequency
        detected_patterns.sort(key=lambda x: x['frequency'], reverse=True)

        return detected_patterns

    def infer_root_causes(self, group: str) -> Dict[str, Any]:
        """
        Infer root causes of resistance in a group.

        Possible causes:
        - Past failed initiatives (broken trust)
        - Threat to expertise/role (job security)
        - Resource constraints (lack of capacity)
        - Value misalignment (doesn't fit culture)
        - Lack of understanding (knowledge gap)
        - Political dynamics (power struggles)

        Args:
            group: Group name

        Returns:
            Root cause analysis with evidence
        """
        group_stories = self._get_group_ai_stories(group)

        # Analyze for different root causes
        causes = {
            'past_failures': self._detect_past_failure_references(group_stories),
            'threat_perception': self._detect_threat_narratives(group_stories),
            'resource_issues': self._detect_resource_concerns(group_stories),
            'value_misalignment': self._detect_value_conflicts(group_stories),
            'knowledge_gap': self._detect_understanding_issues(group_stories)
        }

        # Rank by evidence strength
        ranked_causes = sorted(
            [(cause, data) for cause, data in causes.items() if data['evidence_count'] > 0],
            key=lambda x: x[1]['evidence_count'],
            reverse=True
        )

        # Extract causal chains from stories
        causal_chains = self._extract_causal_chains(group_stories)

        return {
            'primary_cause': ranked_causes[0] if ranked_causes else ('unknown', {'evidence_count': 0}),
            'all_causes': dict(ranked_causes),
            'causal_chains': causal_chains,
            'interpretation': self._interpret_root_causes(ranked_causes)
        }

    def _detect_past_failure_references(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect references to past failed initiatives."""
        failure_keywords = ['last time', 'before', 'tried that', 'failed', 'didn\'t work', 'previous']

        evidence = [
            s for s in stories
            if any(keyword in s.get('summary', '').lower() for keyword in failure_keywords)
        ]

        return {
            'evidence_count': len(evidence),
            'evidence_stories': [s['id'] for s in evidence[:3]],
            'description': 'Past failed initiatives creating skepticism'
        }

    def _detect_threat_narratives(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect threat perception to jobs/roles."""
        threat_keywords = ['job', 'role', 'replace', 'eliminate', 'redundant', 'obsolete', 'threatened']

        evidence = [
            s for s in stories
            if any(keyword in s.get('summary', '').lower() for keyword in threat_keywords)
            or s.get('ai_sentiment', 0) < -0.3
        ]

        return {
            'evidence_count': len(evidence),
            'evidence_stories': [s['id'] for s in evidence[:3]],
            'description': 'Perception that AI threatens jobs or expertise'
        }

    def _detect_resource_concerns(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect resource constraint concerns."""
        resource_keywords = ['time', 'budget', 'resources', 'capacity', 'bandwidth', 'overloaded']

        evidence = [
            s for s in stories
            if any(keyword in s.get('summary', '').lower() for keyword in resource_keywords)
        ]

        return {
            'evidence_count': len(evidence),
            'evidence_stories': [s['id'] for s in evidence[:3]],
            'description': 'Concerns about lacking resources for AI adoption'
        }

    def _detect_value_conflicts(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect value misalignment concerns."""
        value_keywords = ['values', 'culture', 'not us', 'doesn\'t fit', 'wrong for', 'against']

        evidence = [
            s for s in stories
            if any(keyword in s.get('summary', '').lower() for keyword in value_keywords)
        ]

        return {
            'evidence_count': len(evidence),
            'evidence_stories': [s['id'] for s in evidence[:3]],
            'description': 'AI perceived as misaligned with organizational values'
        }

    def _detect_understanding_issues(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect lack of understanding."""
        understanding_keywords = ['don\'t understand', 'unclear', 'confusing', 'no idea', 'what is']

        evidence = [
            s for s in stories
            if any(keyword in s.get('summary', '').lower() for keyword in understanding_keywords)
            or s.get('ai_sophistication') == 'novice'
        ]

        return {
            'evidence_count': len(evidence),
            'evidence_stories': [s['id'] for s in evidence[:3]],
            'description': 'Lack of understanding about AI and its applications'
        }

    def _extract_causal_chains(self, stories: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract causal chains from stories (simplified version)."""
        chains = []

        for story in stories[:5]:  # Top 5 stories
            # Look for causal language in summaries
            text = story.get('summary', '')
            if any(word in text.lower() for word in ['because', 'so', 'therefore', 'led to', 'caused']):
                chains.append({
                    'story_id': story['id'],
                    'chain': text
                })

        return chains

    def _interpret_root_causes(self, ranked_causes: List[Tuple[str, Dict]]) -> str:
        """Generate interpretation of root causes."""
        if not ranked_causes:
            return "No clear resistance patterns detected"

        primary_cause, primary_data = ranked_causes[0]

        interpretations = {
            'past_failures': "Resistance rooted in past failed initiatives - trust needs rebuilding",
            'threat_perception': "Resistance driven by job security concerns - needs clear communication about role evolution",
            'resource_issues': "Resistance due to capacity constraints - needs resource allocation and support",
            'value_misalignment': "Resistance from perceived cultural misfit - needs values-based framing",
            'knowledge_gap': "Resistance from lack of understanding - needs education and training"
        }

        base_interpretation = interpretations.get(primary_cause, "Resistance cause unclear")

        if len(ranked_causes) > 1:
            secondary = ranked_causes[1][0]
            return f"{base_interpretation}. Secondary factor: {secondary}"

        return base_interpretation

    def _get_resistance_narratives(self, group: str) -> List[Dict[str, Any]]:
        """Get representative resistance narratives from a group."""
        group_stories = self._get_group_ai_stories(group)

        # Filter for resistance stories
        resistance_stories = [
            s for s in group_stories
            if s.get('ai_sentiment', 0) < 0
            or s.get('narrative_function') == 'warning'
        ]

        return [
            {
                'story_id': s['id'],
                'summary': s.get('summary', '')[:150],
                'sentiment': s.get('ai_sentiment', 0)
            }
            for s in resistance_stories[:5]
        ]

    def _suggest_interventions(self, group: str) -> List[str]:
        """Suggest interventions for a group's resistance."""
        patterns = self.identify_resistance_patterns(group)
        root_causes = self.infer_root_causes(group)

        interventions = []

        # Pattern-based interventions
        pattern_names = [p['pattern'] for p in patterns]

        if 'fearful' in pattern_names:
            interventions.append("Address job security concerns explicitly - provide role evolution roadmap")
        if 'skeptical' in pattern_names:
            interventions.append("Provide concrete evidence and success stories from similar organizations")
        if 'active' in pattern_names:
            interventions.append("Engage resisters as advisors - understand and address specific concerns")
        if 'passive' in pattern_names:
            interventions.append("Create urgency through competitive positioning or strategic importance")

        # Root cause-based interventions
        primary_cause = root_causes['primary_cause'][0]

        if primary_cause == 'past_failures':
            interventions.append("Acknowledge past failures and explain what's different this time")
        elif primary_cause == 'knowledge_gap':
            interventions.append("Implement comprehensive training program with hands-on practice")
        elif primary_cause == 'resource_issues':
            interventions.append("Allocate dedicated time and resources for AI adoption activities")

        return interventions if interventions else ["Monitor and reassess - no immediate intervention needed"]

    def analyze_resistance_spread(self, resistance_map: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze if resistance is spreading through narrative contagion.

        Checks for:
        - Cross-group story references
        - Influential cautionary tales
        - Spread velocity

        Args:
            resistance_map: Optional resistance map to enhance analysis

        Returns:
            Resistance spread analysis
        """
        # Find stories that reference other stories (narrative contagion)
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
        ORDER BY references DESC
        """

        cross_references = self.client.execute_read_query(query)

        if not cross_references:
            return {
                'is_spreading': False,
                'contagion_network': {},
                'influential_stories': [],
                'spread_velocity': 0,
                'interpretation': 'No evidence of narrative contagion'
            }

        # Build contagion network
        contagion_network = self._build_narrative_network(cross_references)

        # Identify influential cautionary tales
        influential_stories = self._identify_influential_stories(cross_references)

        # Calculate spread velocity
        spread_velocity = self._calculate_spread_velocity(cross_references)

        # Check if spreading
        is_spreading = len(cross_references) > 5 or spread_velocity > 0.5

        return {
            'is_spreading': is_spreading,
            'contagion_network': contagion_network,
            'influential_stories': influential_stories,
            'spread_velocity': spread_velocity,
            'cross_group_references': len(cross_references),
            'interpretation': self._interpret_spread(is_spreading, spread_velocity, influential_stories)
        }

    def _build_narrative_network(self, cross_references: List[Dict]) -> Dict[str, Any]:
        """Build network representation of narrative spread."""
        network = defaultdict(lambda: {'cited_by': [], 'cites': [], 'influence': 0})

        for ref in cross_references:
            source = ref['source_group']
            citing = ref['citing_group']
            count = ref['references']

            network[source]['cited_by'].append(citing)
            network[source]['influence'] += count
            network[citing]['cites'].append(source)

        return dict(network)

    def _identify_influential_stories(self, cross_references: List[Dict]) -> List[Dict[str, Any]]:
        """Identify most influential cautionary tales."""
        story_influence = Counter()

        for ref in cross_references:
            story_influence[ref['source_story']] += ref['references']

        # Get top 5 most influential
        top_stories = story_influence.most_common(5)

        return [
            {
                'story_id': story_id,
                'reference_count': count,
                'influence_score': count / sum(story_influence.values()) if story_influence else 0
            }
            for story_id, count in top_stories
        ]

    def _calculate_spread_velocity(self, cross_references: List[Dict]) -> float:
        """
        Calculate how fast resistance is spreading.

        Returns value 0-1 where higher = faster spread
        """
        if not cross_references:
            return 0.0

        # Simple heuristic: number of cross-group references normalized
        reference_count = len(cross_references)
        velocity = min(reference_count / 10, 1.0)  # Normalize to 0-1

        return velocity

    def _interpret_spread(self, is_spreading: bool, velocity: float, influential: List[Dict]) -> str:
        """Generate interpretation of resistance spread."""
        if not is_spreading:
            return "Resistance appears isolated to specific groups - low contagion risk"

        if velocity > 0.7:
            return "ALERT: Resistance spreading rapidly across groups through influential cautionary tales"
        elif velocity > 0.4:
            return "Moderate spread: Cautionary tales crossing group boundaries"
        else:
            return "Some narrative contagion detected - monitor for acceleration"

    def _identify_hotspots(self, resistance_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify groups with highest resistance."""
        hotspots = []

        for group, data in resistance_map.items():
            score = data['resistance_score']
            if score > 0.6:  # High resistance threshold
                hotspots.append({
                    'group': group,
                    'resistance_score': score,
                    'severity': 'HIGH' if score > 0.8 else 'MODERATE',
                    'patterns': [p['pattern'] for p in data['patterns']],
                    'primary_cause': data['root_causes']['primary_cause'][0]
                })

        # Sort by resistance score
        hotspots.sort(key=lambda x: x['resistance_score'], reverse=True)

        return hotspots

    def _find_common_patterns(self, resistance_map: Dict[str, Any]) -> Dict[str, Any]:
        """Find resistance patterns common across groups."""
        pattern_counts = Counter()
        pattern_groups = defaultdict(list)

        for group, data in resistance_map.items():
            for pattern in data['patterns']:
                pattern_name = pattern['pattern']
                pattern_counts[pattern_name] += 1
                pattern_groups[pattern_name].append(group)

        # Patterns appearing in multiple groups
        common = {
            pattern: {
                'frequency': count,
                'groups': pattern_groups[pattern],
                'prevalence': count / len(resistance_map) if resistance_map else 0
            }
            for pattern, count in pattern_counts.items()
            if count > 1
        }

        return common

    def _assess_overall_severity(self, resistance_map: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall organizational resistance severity."""
        if not resistance_map:
            return {'level': 'UNKNOWN', 'score': 0.5}

        scores = [data['resistance_score'] for data in resistance_map.values()]
        avg_score = sum(scores) / len(scores)

        high_resistance_groups = sum(1 for score in scores if score > 0.6)
        total_groups = len(scores)

        if avg_score > 0.7 or high_resistance_groups > total_groups * 0.5:
            level = 'CRITICAL'
        elif avg_score > 0.5 or high_resistance_groups > total_groups * 0.3:
            level = 'SIGNIFICANT'
        elif avg_score > 0.3:
            level = 'MODERATE'
        else:
            level = 'LOW'

        return {
            'level': level,
            'score': avg_score,
            'high_resistance_groups': high_resistance_groups,
            'total_groups': total_groups,
            'interpretation': self._interpret_overall_severity(level, avg_score)
        }

    def _interpret_overall_severity(self, level: str, score: float) -> str:
        """Generate interpretation of overall severity."""
        interpretations = {
            'CRITICAL': f"Critical resistance levels (score: {score:.2f}) - immediate intervention required across organization",
            'SIGNIFICANT': f"Significant resistance (score: {score:.2f}) - targeted interventions needed in multiple groups",
            'MODERATE': f"Moderate resistance (score: {score:.2f}) - manageable with proper change management",
            'LOW': f"Low resistance (score: {score:.2f}) - favorable conditions for AI adoption"
        }
        return interpretations.get(level, f"Resistance level: {level}")

    def _generate_landscape_recommendations(
        self,
        resistance_map: Dict[str, Any],
        hotspots: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate landscape-level recommendations."""
        recommendations = []

        # Hotspot recommendations
        if hotspots:
            top_hotspot = hotspots[0]
            recommendations.append(
                f"PRIORITY: Address resistance in {top_hotspot['group']} (score: {top_hotspot['resistance_score']:.2f}) "
                f"due to {top_hotspot['primary_cause']}"
            )

        # Common pattern recommendations
        if len(hotspots) > 3:
            recommendations.append(
                "Widespread resistance detected - consider organization-wide change management program"
            )

        # Add generic best practices
        recommendations.extend([
            "Establish clear communication channels for concerns and feedback",
            "Create success stories to counter cautionary tales",
            "Provide psychological safety for experimentation and learning"
        ])

        return recommendations[:5]  # Top 5 recommendations

    def measure_blocking_effect(self, cautionary_tales: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Measure if cautionary tales are blocking AI initiatives.

        Args:
            cautionary_tales: Optional list of cautionary tale stories

        Returns:
            Blocking effect analysis
        """
        if cautionary_tales is None:
            # Get cautionary tales from graph
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true
              AND (s.why_told = 'warning' OR s.narrative_function = 'warning')
            RETURN s
            LIMIT 50
            """
            results = self.client.execute_read_query(query)
            cautionary_tales = [dict(r["s"]) for r in results]

        if not cautionary_tales:
            return {
                'blocking_stories': 0,
                'is_blocking': False,
                'severity': 'NONE'
            }

        # Check for blocking language
        blocking_keywords = ['cancelled', 'blocked', 'stopped', 'prevented', 'abandoned', 'shelved']

        blocking_stories = [
            s for s in cautionary_tales
            if any(keyword in s.get('summary', '').lower() for keyword in blocking_keywords)
        ]

        blocking_count = len(blocking_stories)
        total_count = len(cautionary_tales)

        is_blocking = blocking_count > total_count * 0.3

        if blocking_count > 5:
            severity = 'HIGH'
        elif blocking_count > 2:
            severity = 'MODERATE'
        else:
            severity = 'LOW'

        return {
            'blocking_stories': blocking_count,
            'total_cautionary_tales': total_count,
            'blocking_percentage': blocking_count / total_count if total_count > 0 else 0,
            'is_blocking': is_blocking,
            'severity': severity,
            'examples': [s['id'] for s in blocking_stories[:3]],
            'interpretation': self._interpret_blocking_effect(is_blocking, severity, blocking_count)
        }

    def _interpret_blocking_effect(self, is_blocking: bool, severity: str, count: int) -> str:
        """Generate interpretation of blocking effect."""
        if not is_blocking:
            return f"Limited blocking effect - {count} cautionary tales mention blocking but not widespread"

        if severity == 'HIGH':
            return f"CRITICAL: {count} stories describe blocked/cancelled initiatives - cautionary tales actively preventing adoption"
        elif severity == 'MODERATE':
            return f"Moderate blocking effect - {count} stories mention blocked initiatives"
        else:
            return f"Some blocking indicators present - {count} stories mention resistance effects"
