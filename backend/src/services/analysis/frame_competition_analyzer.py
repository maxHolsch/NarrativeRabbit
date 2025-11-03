"""
Frame Competition Analyzer - Sub-Agent for AI Narrative Intelligence System.

Maps competing frames about AI across groups and identifies frame conflicts.
Shows how different narratives compete for dominance.
"""
from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import Counter, defaultdict

from ...db import neo4j_client
from ...models.ai_entities import FrameCompetition, FrameType

logger = logging.getLogger(__name__)


class FrameCompetitionAnalyzer:
    """
    Analyzes competing frames about AI and shows how they conflict.

    Identifies:
    - All frames being used to describe AI
    - Who uses each frame
    - How frames compete and conflict
    - Dominant frames by group
    """

    def __init__(self):
        """Initialize the frame competition analyzer."""
        self.client = neo4j_client

    def map_competing_frames(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Identify all frames being used to describe AI and how they compete.

        Args:
            initiative_id: Optional initiative to filter by

        Returns:
            Complete frame landscape with competitions
        """
        # Get all AI-related stories
        if initiative_id:
            stories = self._get_initiative_stories(initiative_id)
        else:
            stories = self._get_all_ai_stories()

        # Extract frames from each story
        frame_map = defaultdict(lambda: {
            'groups': set(),
            'stories': [],
            'sentiments': [],
            'outcomes': [],
            'story_count': 0
        })

        for story in stories:
            frame = self._identify_dominant_frame(story)
            group = self._get_teller_group(story)

            frame_map[frame]['groups'].add(group)
            frame_map[frame]['stories'].append(story['id'])
            frame_map[frame]['sentiments'].append(story.get('ai_sentiment', 0))
            frame_map[frame]['outcomes'].append(story.get('outcome', ''))
            frame_map[frame]['story_count'] += 1

        # Convert sets to lists for JSON serialization
        for frame_data in frame_map.values():
            frame_data['groups'] = list(frame_data['groups'])

        # Identify competitions
        competitions = self._identify_frame_conflicts(frame_map)

        # Get dominant frame by group
        dominant_by_group = self._group_dominant_frames(stories)

        return {
            'frames': dict(frame_map),
            'competitions': competitions,
            'dominant_frame_by_group': dominant_by_group,
            'synthesis': self._synthesize_frame_landscape(frame_map, competitions)
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

    def _get_initiative_stories(self, initiative_id: str) -> List[Dict[str, Any]]:
        """Get stories about a specific initiative."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})<-[:DESCRIBES_AI]-(s:Story)
        RETURN s
        ORDER BY s.timestamp DESC
        """

        results = self.client.execute_read_query(query, {"initiative_id": initiative_id})
        return [dict(r["s"]) for r in results]

    def _identify_dominant_frame(self, story: Dict[str, Any]) -> str:
        """
        Identify the dominant narrative frame in a story.

        Frames: opportunity, threat, tool, replacement, partnership, experiment, mandate

        Args:
            story: Story data

        Returns:
            Frame type
        """
        # Check explicit frame first
        narrative_function = story.get('narrative_function')
        if narrative_function:
            return narrative_function

        # Infer from agency frame
        agency = story.get('agency_frame')
        if agency == 'partnership':
            return 'partner'
        elif agency == 'ai_in_control':
            return 'replacement'
        elif agency == 'human_in_control':
            return 'tool'

        # Infer from sentiment and text
        sentiment = story.get('ai_sentiment', 0)
        text = (story.get('summary', '') + ' ' + story.get('full_text', '')).lower()

        # Pattern matching for frames
        if any(word in text for word in ['experiment', 'trial', 'pilot', 'test']):
            return 'experiment'
        elif any(word in text for word in ['must', 'mandate', 'requirement', 'required']):
            return 'mandate'
        elif any(word in text for word in ['replace', 'eliminate', 'instead of']):
            return 'replacement'
        elif any(word in text for word in ['partner', 'collaboration', 'together']):
            return 'partner'
        elif any(word in text for word in ['tool', 'assistant', 'help', 'support']):
            return 'tool'
        elif any(word in text for word in ['threat', 'risk', 'danger', 'worried']):
            return 'threat'
        elif any(word in text for word in ['opportunity', 'advantage', 'benefit', 'potential']):
            return 'opportunity'

        # Default based on sentiment
        if sentiment > 0.5:
            return 'opportunity'
        elif sentiment < -0.5:
            return 'threat'
        else:
            return 'neutral'

    def _get_teller_group(self, story: Dict[str, Any]) -> str:
        """
        Get the group of the story teller.

        Args:
            story: Story data

        Returns:
            Group name
        """
        # Try to get from department
        department = story.get('department')
        if department:
            return department

        # Query for teller's group
        query = """
        MATCH (p:Person)-[:TELLS]->(s:Story {id: $story_id})
        MATCH (p)-[:BELONGS_TO]->(g:Group)
        RETURN g.name as group_name
        LIMIT 1
        """

        results = self.client.execute_read_query(query, {"story_id": story['id']})
        if results:
            return results[0]['group_name']

        return 'Unknown'

    def _identify_frame_conflicts(self, frame_map: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find frames that directly conflict.

        Args:
            frame_map: Map of frames to their data

        Returns:
            List of frame conflicts
        """
        # Define opposing frame types
        frame_oppositions = [
            ('opportunity', 'threat'),
            ('tool', 'replacement'),
            ('partnership', 'replacement'),
            ('experiment', 'mandate'),
            ('partner', 'threat')
        ]

        conflicts = []
        frames = list(frame_map.keys())

        for i, frame1 in enumerate(frames):
            for frame2 in frames[i+1:]:
                # Check if frames are opposing
                if self._are_opposing_frames(frame1, frame2, frame_oppositions):
                    data1 = frame_map[frame1]
                    data2 = frame_map[frame2]

                    conflicts.append({
                        'frame_a': frame1,
                        'frame_b': frame2,
                        'groups_a': data1['groups'],
                        'groups_b': data2['groups'],
                        'conflict_type': self._classify_conflict_type(frame1, frame2),
                        'impact': self._assess_conflict_impact(data1, data2),
                        'story_count_a': data1['story_count'],
                        'story_count_b': data2['story_count']
                    })

        # Sort by impact
        conflicts.sort(key=lambda x: x['impact'], reverse=True)

        return conflicts

    def _are_opposing_frames(
        self,
        frame1: str,
        frame2: str,
        oppositions: List[Tuple[str, str]]
    ) -> bool:
        """Check if two frames are in opposition."""
        for pair in oppositions:
            if (frame1 in pair and frame2 in pair) and frame1 != frame2:
                return True
        return False

    def _classify_conflict_type(self, frame1: str, frame2: str) -> str:
        """Classify the type of frame conflict."""
        if ('opportunity' in [frame1, frame2] and 'threat' in [frame1, frame2]):
            return 'fundamental_opposition'
        elif ('tool' in [frame1, frame2] and 'replacement' in [frame1, frame2]):
            return 'agency_conflict'
        elif ('experiment' in [frame1, frame2] and 'mandate' in [frame1, frame2]):
            return 'commitment_conflict'
        else:
            return 'perspective_difference'

    def _assess_conflict_impact(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> float:
        """
        Assess the impact of a frame conflict.

        Higher impact when:
        - More stories in conflict
        - More groups involved
        - Greater sentiment divergence

        Args:
            data1: First frame data
            data2: Second frame data

        Returns:
            Impact score (0-1)
        """
        # Story count factor
        story_count = data1['story_count'] + data2['story_count']
        story_factor = min(story_count / 50, 1.0)  # Normalize to 0-1

        # Group count factor
        unique_groups = set(data1['groups']) | set(data2['groups'])
        group_factor = min(len(unique_groups) / 10, 1.0)  # Normalize to 0-1

        # Sentiment divergence
        avg_sent1 = sum(data1['sentiments']) / len(data1['sentiments']) if data1['sentiments'] else 0
        avg_sent2 = sum(data2['sentiments']) / len(data2['sentiments']) if data2['sentiments'] else 0
        sentiment_divergence = abs(avg_sent1 - avg_sent2)

        # Weighted impact score
        impact = (story_factor * 0.4 + group_factor * 0.3 + sentiment_divergence * 0.3)

        return min(impact, 1.0)

    def _group_dominant_frames(self, stories: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Determine dominant frame for each group.

        Args:
            stories: All AI stories

        Returns:
            Dominant frames by group
        """
        group_frames = defaultdict(lambda: Counter())

        for story in stories:
            frame = self._identify_dominant_frame(story)
            group = self._get_teller_group(story)
            group_frames[group][frame] += 1

        # Get dominant frame for each group
        result = {}
        for group, frame_counts in group_frames.items():
            most_common = frame_counts.most_common(1)
            if most_common:
                dominant_frame, count = most_common[0]
                result[group] = {
                    'dominant_frame': dominant_frame,
                    'frequency': count,
                    'all_frames': dict(frame_counts),
                    'diversity': len(frame_counts)  # How many different frames this group uses
                }

        return result

    def analyze_group_frame_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze how different groups systematically frame AI.

        Returns:
            Group framing patterns
        """
        query = """
        MATCH (g:Group)<-[:BELONGS_TO]-(p:Person)
        MATCH (p)-[:TELLS]->(s:Story)
        WHERE s.ai_related = true
        OPTIONAL MATCH (s)-[:USES_FRAME]->(f:NarrativeFrame)
        RETURN g.name as group,
               f.frame_type as frame,
               s.ai_sentiment as sentiment,
               count(s) as frequency
        ORDER BY group, frequency DESC
        """

        results = self.client.execute_read_query(query)

        # Group by group
        group_profiles = defaultdict(lambda: {
            'primary_frames': [],
            'typical_valence': [],
            'frame_diversity': 0,
            'total_stories': 0
        })

        for row in results:
            group = row['group']
            if row['frame']:
                group_profiles[group]['primary_frames'].append({
                    'frame': row['frame'],
                    'frequency': row['frequency']
                })
            if row['sentiment'] is not None:
                group_profiles[group]['typical_valence'].append(row['sentiment'])
            group_profiles[group]['total_stories'] += row['frequency']

        # Calculate derived metrics
        for group, profile in group_profiles.items():
            # Frame diversity
            profile['frame_diversity'] = len(profile['primary_frames'])

            # Average sentiment
            if profile['typical_valence']:
                profile['avg_sentiment'] = sum(profile['typical_valence']) / len(profile['typical_valence'])
            else:
                profile['avg_sentiment'] = 0

            # Interpretation
            profile['interpretation'] = self._interpret_group_pattern(profile)

        return dict(group_profiles)

    def _interpret_group_pattern(self, profile: Dict[str, Any]) -> str:
        """Generate interpretation of a group's framing pattern."""
        avg_sentiment = profile.get('avg_sentiment', 0)
        diversity = profile.get('frame_diversity', 0)
        primary = profile.get('primary_frames', [])

        if not primary:
            return "Limited AI narrative activity"

        dominant_frame = primary[0]['frame'] if primary else 'unknown'

        if avg_sentiment > 0.5 and dominant_frame == 'opportunity':
            return "Enthusiastically embracing AI as opportunity"
        elif avg_sentiment < -0.5 and dominant_frame == 'threat':
            return "Highly skeptical, viewing AI as threat"
        elif diversity > 3:
            return "Multiple perspectives, no dominant frame - indicates evolving understanding"
        elif dominant_frame == 'tool':
            return "Pragmatic view - AI as tool to augment work"
        elif dominant_frame == 'replacement':
            return "Concerned about automation replacing roles"
        else:
            return f"Primary frame: {dominant_frame}, sentiment: {'positive' if avg_sentiment > 0 else 'negative'}"

    def find_narrative_common_ground(self, frame_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find what competing narratives actually agree on.

        Args:
            frame_map: Map of frames to data

        Returns:
            Common ground analysis
        """
        # Extract core beliefs from each frame
        all_stories = []
        for frame_data in frame_map.values():
            all_stories.extend(frame_data['stories'])

        # Get stories
        if not all_stories:
            return {'shared_beliefs': [], 'shared_values': [], 'shared_concerns': []}

        query = """
        MATCH (s:Story)
        WHERE s.id IN $story_ids
        OPTIONAL MATCH (s)-[:EXEMPLIFIES]->(v:Value)
        OPTIONAL MATCH (s)-[:EXEMPLIFIES]->(t:Theme)
        RETURN s.id as story_id,
               collect(DISTINCT v.name) as values,
               collect(DISTINCT t.name) as themes
        """

        results = self.client.execute_read_query(query, {"story_ids": all_stories[:100]})  # Limit for performance

        # Aggregate across all stories
        all_values = []
        all_themes = []

        for row in results:
            if row['values']:
                all_values.extend(row['values'])
            if row['themes']:
                all_themes.extend(row['themes'])

        # Find most common (these are shared)
        value_counts = Counter(all_values)
        theme_counts = Counter(all_themes)

        # Shared elements appear in >50% of frames
        threshold = len(frame_map) * 0.5

        shared_values = [v for v, count in value_counts.items() if count >= threshold]
        shared_themes = [t for t, count in theme_counts.items() if count >= threshold]

        return {
            'shared_values': shared_values,
            'shared_themes': shared_themes,
            'shared_concerns': self._identify_shared_concerns(results),
            'bridging_themes': self._identify_bridging_themes(shared_values, shared_themes)
        }

    def _identify_shared_concerns(self, story_data: List[Dict[str, Any]]) -> List[str]:
        """Identify concerns shared across different frames."""
        # Common concerns in AI narratives
        common_concerns = [
            'job security',
            'training needs',
            'ethical implications',
            'data privacy',
            'reliability',
            'transparency'
        ]

        # This is a simplified version - in production, would use more sophisticated NLP
        return ['training needs', 'reliability']  # Placeholder

    def _identify_bridging_themes(self, values: List[str], themes: List[str]) -> List[str]:
        """Identify themes that can bridge competing frames."""
        bridging = []

        # Themes that appear in multiple contexts can bridge
        potential_bridges = ['innovation', 'quality', 'efficiency', 'collaboration']

        for bridge in potential_bridges:
            if bridge in values or bridge in themes:
                bridging.append(bridge)

        return bridging

    def _synthesize_frame_landscape(
        self,
        frame_map: Dict[str, Dict[str, Any]],
        competitions: List[Dict[str, Any]]
    ) -> str:
        """
        Synthesize overall frame landscape.

        Args:
            frame_map: All frames
            competitions: Frame conflicts

        Returns:
            Summary interpretation
        """
        total_frames = len(frame_map)
        total_conflicts = len(competitions)

        if total_conflicts == 0:
            return f"Unified narrative landscape with {total_frames} frames showing alignment"
        elif total_conflicts > 3:
            return f"Highly fragmented narrative landscape with {total_conflicts} major conflicts across {total_frames} frames"
        else:
            return f"Moderate frame competition with {total_conflicts} conflicts. Some alignment possible."

    def design_unified_narrative(
        self,
        conflicts: List[Dict[str, Any]],
        common_ground: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Design a unified narrative that bridges competing frames.

        Args:
            conflicts: Frame conflicts
            common_ground: Shared elements

        Returns:
            Unified narrative framework
        """
        # Core message based on common ground
        core_message = self._craft_core_message(common_ground)

        # Acknowledgment clauses for each conflicting perspective
        acknowledgments = {}
        for conflict in conflicts:
            frame_a = conflict['frame_a']
            frame_b = conflict['frame_b']
            acknowledgments[frame_a] = self._craft_acknowledgment(frame_a, conflict)
            acknowledgments[frame_b] = self._craft_acknowledgment(frame_b, conflict)

        # Bridging stories that work across frames
        bridging_stories = self._identify_bridging_stories(common_ground)

        # Reframing language
        reframing = {}
        for conflict in conflicts:
            reframing[f"{conflict['frame_a']}_vs_{conflict['frame_b']}"] = self._suggest_reframe(conflict)

        return {
            'core_message': core_message,
            'acknowledgment_clauses': acknowledgments,
            'bridging_stories': bridging_stories,
            'reframing_language': reframing,
            'vision_narrative': self._craft_vision_narrative(common_ground)
        }

    def _craft_core_message(self, common_ground: Dict[str, Any]) -> str:
        """Craft core message based on common ground."""
        shared_values = common_ground.get('shared_values', [])
        shared_themes = common_ground.get('shared_themes', [])

        if shared_values and shared_themes:
            return f"We're united in our commitment to {', '.join(shared_values[:2])} while navigating {', '.join(shared_themes[:2])}"
        else:
            return "We're exploring AI together, learning as we go"

    def _craft_acknowledgment(self, frame: str, conflict: Dict[str, Any]) -> str:
        """Craft acknowledgment clause for a frame."""
        acknowledgments = {
            'threat': "We understand concerns about how AI might change roles and responsibilities",
            'opportunity': "We recognize the potential for AI to enhance our capabilities",
            'tool': "We see AI as something we can learn to use effectively",
            'replacement': "We acknowledge anxiety about automation",
            'experiment': "We appreciate the importance of testing carefully",
            'mandate': "We hear the need for clear direction and commitment"
        }

        return acknowledgments.get(frame, f"We acknowledge the {frame} perspective")

    def _identify_bridging_stories(self, common_ground: Dict[str, Any]) -> List[str]:
        """Identify stories that can bridge different frames."""
        # Query for stories that touch on shared themes
        shared_themes = common_ground.get('shared_themes', [])

        if not shared_themes:
            return []

        query = """
        MATCH (s:Story)-[:EXEMPLIFIES]->(t:Theme)
        WHERE t.name IN $themes
          AND s.ai_related = true
        WITH s, count(t) as theme_count
        WHERE theme_count >= 2
        RETURN s.id as story_id, s.summary as summary
        LIMIT 5
        """

        results = self.client.execute_read_query(query, {"themes": shared_themes})
        return [r['story_id'] for r in results]

    def _suggest_reframe(self, conflict: Dict[str, Any]) -> str:
        """Suggest reframing for a conflict."""
        frame_a = conflict['frame_a']
        frame_b = conflict['frame_b']

        reframes = {
            ('opportunity', 'threat'): "AI as a transition we navigate together, with both opportunities and challenges",
            ('tool', 'replacement'): "AI augments human capabilities rather than replacing them",
            ('experiment', 'mandate'): "Committed exploration - we're serious about AI while remaining adaptive"
        }

        for key, reframe in reframes.items():
            if frame_a in key and frame_b in key:
                return reframe

        return f"Balance between {frame_a} and {frame_b} perspectives"

    def _craft_vision_narrative(self, common_ground: Dict[str, Any]) -> str:
        """Craft vision narrative based on common ground."""
        values = common_ground.get('shared_values', [])

        if values:
            return f"Our vision: Leveraging AI to amplify {values[0]} while staying true to our core values"
        else:
            return "Our vision: Thoughtful AI adoption that enhances human capability"
