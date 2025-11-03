"""
Narrative Gap Analyzer - Sub-Agent for AI Narrative Intelligence System.

Identifies disconnects between official messaging and actual employee stories.
Detects gaps in vocabulary, framing, emphasis, sentiment, and beliefs.
"""
from typing import List, Dict, Any, Optional, Set
import logging
from collections import Counter

from ...db import neo4j_client
from ...models.ai_entities import NarrativeGap

logger = logging.getLogger(__name__)


class NarrativeGapAnalyzer:
    """
    Analyzes gaps between official narratives and actual employee stories.

    Detects disconnects in:
    - Vocabulary (what words are used)
    - Framing (how AI is positioned)
    - Emphasis (what's highlighted vs downplayed)
    - Sentiment (emotional valence)
    - Beliefs (underlying assumptions)
    """

    def __init__(self):
        """Initialize the narrative gap analyzer."""
        self.client = neo4j_client

    def analyze_official_vs_actual(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Compare official narrative to employee narratives.

        Args:
            initiative_id: Optional specific initiative to analyze. If None, analyzes all AI stories.

        Returns:
            Dictionary with gap analysis across multiple dimensions
        """
        # Step 1: Get official narrative
        official_story = self.get_official_narrative(initiative_id)

        # Step 2: Get employee stories
        employee_stories = self.get_employee_narratives(initiative_id)

        if not official_story and not employee_stories:
            return {
                "error": "No stories found for analysis",
                "initiative_id": initiative_id
            }

        # Step 3: Compare across dimensions
        gaps = {
            'language_gap': self.compare_vocabulary(official_story, employee_stories),
            'framing_gap': self.compare_frames(official_story, employee_stories),
            'emphasis_gap': self.compare_emphasis(official_story, employee_stories),
            'emotion_gap': self.compare_sentiment(official_story, employee_stories),
            'belief_gap': self.compare_beliefs(official_story, employee_stories)
        }

        # Step 4: Calculate overall severity
        severity = self.detect_gap_severity(gaps)

        return {
            "initiative_id": initiative_id,
            "official_story": official_story,
            "employee_story_count": len(employee_stories),
            "gaps": gaps,
            "severity": severity,
            "interpretation": self._generate_interpretation(gaps, severity)
        }

    def get_official_narrative(self, initiative_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the official/leadership narrative about AI.

        Args:
            initiative_id: Optional initiative ID to filter by

        Returns:
            Official story data or None
        """
        if initiative_id:
            query = """
            MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_OFFICIAL_STORY]->(s:Story)
            RETURN s
            LIMIT 1
            """
            params = {"initiative_id": initiative_id}
        else:
            # Get most recent official AI story
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true
              AND (s.source = 'official' OR s.source = 'leadership' OR s.source = 'announcement')
            RETURN s
            ORDER BY s.timestamp DESC
            LIMIT 1
            """
            params = {}

        results = self.client.execute_read_query(query, params)

        if results:
            return dict(results[0]["s"])
        return None

    def get_employee_narratives(self, initiative_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get employee stories about AI.

        Args:
            initiative_id: Optional initiative ID to filter by

        Returns:
            List of employee stories
        """
        if initiative_id:
            query = """
            MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
            RETURN s
            LIMIT 50
            """
            params = {"initiative_id": initiative_id}
        else:
            # Get recent employee AI stories
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true
              AND s.source <> 'official'
              AND s.source <> 'leadership'
              AND s.source <> 'announcement'
            RETURN s
            ORDER BY s.timestamp DESC
            LIMIT 50
            """
            params = {}

        results = self.client.execute_read_query(query, params)
        return [dict(r["s"]) for r in results]

    def compare_vocabulary(
        self,
        official_story: Optional[Dict[str, Any]],
        employee_stories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare vocabulary between official and employee narratives.

        Identifies:
        - Terms used only by leadership
        - Terms used only by employees
        - Shared vocabulary
        - Sophistication gap

        Args:
            official_story: Official narrative
            employee_stories: Employee narratives

        Returns:
            Vocabulary gap analysis
        """
        # Extract AI terms from official story
        official_terms = self._extract_ai_terms(official_story) if official_story else set()

        # Extract AI terms from employee stories
        employee_terms = set()
        for story in employee_stories:
            employee_terms.update(self._extract_ai_terms(story))

        # Calculate gaps
        official_only = official_terms - employee_terms
        employee_only = employee_terms - official_terms
        shared = official_terms & employee_terms

        # Measure sophistication gap
        sophistication_gap = self._measure_sophistication_diff(official_terms, employee_terms)

        return {
            'official_only': list(official_only),
            'employee_only': list(employee_only),
            'shared': list(shared),
            'sophistication_gap': sophistication_gap,
            'alignment_score': len(shared) / max(len(official_terms | employee_terms), 1),
            'interpretation': self._interpret_vocabulary_gap(official_only, employee_only, sophistication_gap)
        }

    def _extract_ai_terms(self, story: Dict[str, Any]) -> Set[str]:
        """
        Extract AI-related terms from a story.

        Args:
            story: Story data

        Returns:
            Set of AI terms
        """
        if not story:
            return set()

        # Get AI concepts mentioned
        ai_concepts = story.get('ai_concepts_mentioned', [])
        if isinstance(ai_concepts, list):
            terms = set(ai_concepts)
        else:
            terms = set()

        # Extract from text using common AI keywords
        text = story.get('summary', '') + ' ' + story.get('full_text', '')
        text_lower = text.lower()

        ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml',
            'automation', 'bot', 'copilot', 'assistant', 'algorithm',
            'neural network', 'deep learning', 'llm', 'gpt',
            'automated', 'intelligent', 'smart', 'cognitive'
        ]

        for keyword in ai_keywords:
            if keyword in text_lower:
                terms.add(keyword)

        return terms

    def _measure_sophistication_diff(
        self,
        official_terms: Set[str],
        employee_terms: Set[str]
    ) -> float:
        """
        Measure sophistication difference between vocabularies.

        Technical/formal terms indicate higher sophistication.

        Args:
            official_terms: Official vocabulary
            employee_terms: Employee vocabulary

        Returns:
            Sophistication difference score (0-1)
        """
        technical_terms = {
            'machine learning', 'neural network', 'deep learning',
            'algorithm', 'model', 'training', 'inference',
            'natural language processing', 'computer vision'
        }

        official_technical = len(official_terms & technical_terms)
        employee_technical = len(employee_terms & technical_terms)

        official_score = official_technical / max(len(official_terms), 1)
        employee_score = employee_technical / max(len(employee_terms), 1)

        return abs(official_score - employee_score)

    def _interpret_vocabulary_gap(
        self,
        official_only: Set[str],
        employee_only: Set[str],
        sophistication_gap: float
    ) -> str:
        """Generate interpretation of vocabulary gap."""
        if sophistication_gap > 0.5:
            return "Large sophistication gap - leadership uses technical terms, employees use colloquial language"
        elif len(official_only) > 5 and len(employee_only) > 5:
            return "Completely different vocabularies - suggests lack of shared understanding"
        elif len(official_only) > len(employee_only) * 2:
            return "Leadership vocabulary not adopted by employees"
        elif len(employee_only) > len(official_only) * 2:
            return "Employees have developed their own terminology"
        else:
            return "Moderate vocabulary alignment with some divergence"

    def compare_frames(
        self,
        official_story: Optional[Dict[str, Any]],
        employee_stories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare how AI is framed differently.

        Identifies:
        - Official framing (opportunity/tool/transformation)
        - Employee framing (threat/burden/experiment)
        - Frame alignment score

        Args:
            official_story: Official narrative
            employee_stories: Employee narratives

        Returns:
            Framing gap analysis
        """
        # Get official frame
        official_frame = self._extract_narrative_frame(official_story) if official_story else "unknown"

        # Get employee frames
        employee_frames = [self._extract_narrative_frame(story) for story in employee_stories]
        frame_counts = Counter(employee_frames)

        # Calculate alignment
        dominant_employee_frame = frame_counts.most_common(1)[0][0] if frame_counts else "unknown"
        alignment_score = frame_counts.get(official_frame, 0) / max(len(employee_stories), 1)

        # Identify conflicts
        conflicting_frames = self._identify_frame_conflicts(official_frame, dominant_employee_frame)

        return {
            'official_frame': official_frame,
            'dominant_employee_frames': dict(frame_counts.most_common(3)),
            'alignment_score': alignment_score,
            'conflicting': conflicting_frames,
            'interpretation': self._interpret_frame_gap(official_frame, dominant_employee_frame, alignment_score)
        }

    def _extract_narrative_frame(self, story: Dict[str, Any]) -> str:
        """
        Extract the narrative frame from a story.

        Frames: opportunity, threat, tool, replacement, partnership, experiment, mandate

        Args:
            story: Story data

        Returns:
            Frame type
        """
        if not story:
            return "unknown"

        # Check for explicit frame in narrative_function
        narrative_function = story.get('narrative_function')
        if narrative_function:
            return narrative_function

        # Infer from sentiment and language
        sentiment = story.get('ai_sentiment', 0)
        text = story.get('summary', '').lower()

        # Opportunity indicators
        if any(word in text for word in ['opportunity', 'advantage', 'growth', 'innovation']):
            return "opportunity"

        # Threat indicators
        if any(word in text for word in ['threat', 'risk', 'replace', 'worried', 'concerned']):
            return "threat"

        # Tool indicators
        if any(word in text for word in ['tool', 'assistant', 'copilot', 'help']):
            return "tool"

        # Based on sentiment
        if sentiment > 0.5:
            return "opportunity"
        elif sentiment < -0.5:
            return "threat"
        else:
            return "neutral"

    def _identify_frame_conflicts(self, frame_a: str, frame_b: str) -> bool:
        """
        Check if two frames are in conflict.

        Args:
            frame_a: First frame
            frame_b: Second frame

        Returns:
            True if frames conflict
        """
        opposing_pairs = [
            ('opportunity', 'threat'),
            ('tool', 'replacement'),
            ('partnership', 'replacement'),
            ('experiment', 'mandate')
        ]

        for pair in opposing_pairs:
            if (frame_a in pair and frame_b in pair) and frame_a != frame_b:
                return True

        return False

    def _interpret_frame_gap(self, official_frame: str, employee_frame: str, alignment: float) -> str:
        """Generate interpretation of frame gap."""
        if alignment > 0.7:
            return "Strong frame alignment - employees echo official framing"
        elif self._identify_frame_conflicts(official_frame, employee_frame):
            return f"Conflicting frames - leadership frames as '{official_frame}', employees see '{employee_frame}'"
        elif alignment < 0.3:
            return "Low frame alignment - different narratives competing"
        else:
            return "Moderate frame alignment with some divergence"

    def compare_emphasis(
        self,
        official_story: Optional[Dict[str, Any]],
        employee_stories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare what aspects get emphasized differently.

        Args:
            official_story: Official narrative
            employee_stories: Employee narratives

        Returns:
            Emphasis gap analysis
        """
        # Extract emphasis from official story
        official_emphasis = self._extract_emphasis_points(official_story) if official_story else set()

        # Aggregate employee emphasis
        employee_emphasis = set()
        for story in employee_stories:
            employee_emphasis.update(self._extract_emphasis_points(story))

        # Find gaps
        official_only = official_emphasis - employee_emphasis
        employee_only = employee_emphasis - official_emphasis

        return {
            'official_priorities': list(official_emphasis),
            'employee_priorities': list(employee_emphasis),
            'what_execs_ignore': list(employee_only),
            'what_employees_ignore': list(official_only),
            'interpretation': self._interpret_emphasis_gap(official_only, employee_only)
        }

    def _extract_emphasis_points(self, story: Dict[str, Any]) -> Set[str]:
        """Extract what a story emphasizes."""
        if not story:
            return set()

        emphasis = set()

        # Check themes
        themes = story.get('primary_themes', [])
        if isinstance(themes, list):
            emphasis.update(themes)

        # Common emphasis categories
        text = story.get('summary', '').lower()

        if any(word in text for word in ['efficiency', 'productivity', 'faster']):
            emphasis.add('efficiency')
        if any(word in text for word in ['quality', 'better', 'improved']):
            emphasis.add('quality')
        if any(word in text for word in ['cost', 'saving', 'budget']):
            emphasis.add('cost savings')
        if any(word in text for word in ['workload', 'burden', 'more work']):
            emphasis.add('workload impact')
        if any(word in text for word in ['job', 'role', 'position']):
            emphasis.add('job impact')

        return emphasis

    def _interpret_emphasis_gap(self, official_only: Set[str], employee_only: Set[str]) -> str:
        """Generate interpretation of emphasis gap."""
        if 'workload impact' in employee_only and 'efficiency' in official_only:
            return "Execs emphasize efficiency gains, employees worry about increased workload"
        elif 'job impact' in employee_only:
            return "Employees concerned about job impact - leadership not addressing this"
        elif len(employee_only) > len(official_only):
            return "Employees prioritizing concerns not mentioned in official messaging"
        else:
            return "Different emphasis patterns - some disconnect in priorities"

    def compare_sentiment(
        self,
        official_story: Optional[Dict[str, Any]],
        employee_stories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare sentiment between official and employee narratives.

        Args:
            official_story: Official narrative
            employee_stories: Employee narratives

        Returns:
            Sentiment gap analysis
        """
        official_sentiment = official_story.get('ai_sentiment', 0) if official_story else 0

        employee_sentiments = [
            story.get('ai_sentiment', 0)
            for story in employee_stories
            if story.get('ai_sentiment') is not None
        ]

        if not employee_sentiments:
            avg_employee_sentiment = 0
        else:
            avg_employee_sentiment = sum(employee_sentiments) / len(employee_sentiments)

        sentiment_gap = abs(official_sentiment - avg_employee_sentiment)

        return {
            'official_sentiment': official_sentiment,
            'employee_sentiment': avg_employee_sentiment,
            'sentiment_gap': sentiment_gap,
            'interpretation': self._interpret_sentiment_gap(official_sentiment, avg_employee_sentiment, sentiment_gap)
        }

    def _interpret_sentiment_gap(self, official: float, employee: float, gap: float) -> str:
        """Generate interpretation of sentiment gap."""
        if gap < 0.2:
            return "Sentiment alignment - similar emotional response"
        elif official > 0.5 and employee < -0.2:
            return "Major disconnect - leadership enthusiastic, employees negative"
        elif official > 0 and employee < official - 0.4:
            return "Executive optimism not shared by employees"
        elif employee < 0 and official > 0:
            return "Employee concerns not reflected in official messaging"
        else:
            return "Moderate sentiment divergence"

    def compare_beliefs(
        self,
        official_story: Optional[Dict[str, Any]],
        employee_stories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare underlying beliefs and assumptions.

        Args:
            official_story: Official narrative
            employee_stories: Employee narratives

        Returns:
            Belief gap analysis
        """
        # Extract beliefs from agency frames
        official_agency = official_story.get('agency_frame') if official_story else None
        employee_agencies = [s.get('agency_frame') for s in employee_stories if s.get('agency_frame')]

        agency_counts = Counter(employee_agencies)
        dominant_employee_agency = agency_counts.most_common(1)[0][0] if agency_counts else None

        # Check innovation signals
        official_innovation = official_story.get('innovation_signal') if official_story else None
        employee_innovations = [s.get('innovation_signal') for s in employee_stories if s.get('innovation_signal')]
        innovation_counts = Counter(employee_innovations)

        return {
            'official_agency_belief': official_agency,
            'employee_agency_beliefs': dict(agency_counts),
            'official_innovation_belief': official_innovation,
            'employee_innovation_beliefs': dict(innovation_counts),
            'interpretation': self._interpret_belief_gap(official_agency, dominant_employee_agency)
        }

    def _interpret_belief_gap(self, official_agency: Optional[str], employee_agency: Optional[str]) -> str:
        """Generate interpretation of belief gap."""
        if official_agency == 'human_in_control' and employee_agency == 'ai_in_control':
            return "Belief mismatch - leadership sees human control, employees feel AI is taking over"
        elif official_agency == 'partnership' and employee_agency == 'ai_in_control':
            return "Leadership frames as partnership, employees feel disempowered"
        elif official_agency and employee_agency and official_agency != employee_agency:
            return f"Different belief systems - leadership: {official_agency}, employees: {employee_agency}"
        else:
            return "Belief systems not clearly divergent"

    def detect_gap_severity(self, gaps: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess overall severity of gaps.

        Args:
            gaps: Gap analysis results

        Returns:
            Severity assessment
        """
        severity_indicators = {
            'critical': [],
            'significant': [],
            'minor': []
        }

        # Vocabulary gap severity
        vocab_alignment = gaps['language_gap'].get('alignment_score', 0)
        if vocab_alignment < 0.3:
            severity_indicators['critical'].append('Completely different vocabulary')
        elif vocab_alignment < 0.6:
            severity_indicators['significant'].append('Limited vocabulary overlap')

        # Frame gap severity
        frame_alignment = gaps['framing_gap'].get('alignment_score', 0)
        if gaps['framing_gap'].get('conflicting', False):
            severity_indicators['critical'].append('Opposing narrative frames')
        elif frame_alignment < 0.4:
            severity_indicators['significant'].append('Low frame alignment')

        # Sentiment gap severity
        sentiment_gap = gaps['emotion_gap'].get('sentiment_gap', 0)
        if sentiment_gap > 0.8:
            severity_indicators['critical'].append('Extreme sentiment divergence')
        elif sentiment_gap > 0.5:
            severity_indicators['significant'].append('Significant sentiment gap')

        # Calculate overall severity score
        critical_count = len(severity_indicators['critical'])
        significant_count = len(severity_indicators['significant'])
        severity_score = (critical_count * 1.0 + significant_count * 0.5) / 3.0

        if severity_score > 0.7:
            overall = "CRITICAL"
        elif severity_score > 0.4:
            overall = "SIGNIFICANT"
        else:
            overall = "MINOR"

        return {
            'overall_severity': overall,
            'severity_score': severity_score,
            'indicators': severity_indicators,
            'recommendation': self._generate_severity_recommendation(overall, severity_indicators)
        }

    def _generate_severity_recommendation(self, severity: str, indicators: Dict[str, List[str]]) -> str:
        """Generate recommendation based on severity."""
        if severity == "CRITICAL":
            return "IMMEDIATE ACTION REQUIRED: Major gaps threaten AI adoption. Recommend leadership workshop to align messaging."
        elif severity == "SIGNIFICANT":
            return "ACTION RECOMMENDED: Notable gaps exist. Consider targeted communication to address employee concerns."
        else:
            return "MONITORING SUGGESTED: Minor gaps are manageable but worth tracking."

    def _generate_interpretation(self, gaps: Dict[str, Any], severity: Dict[str, Any]) -> str:
        """Generate overall interpretation of gaps."""
        interpretations = []

        for gap_type, gap_data in gaps.items():
            if 'interpretation' in gap_data:
                interpretations.append(f"{gap_type}: {gap_data['interpretation']}")

        summary = f"Overall severity: {severity['overall_severity']}. "
        summary += " | ".join(interpretations)

        return summary
