"""
AI Narrative Intelligence Agent - Main Orchestrator

Coordinates 5 sub-agents to answer strategic questions about AI adoption:
1. NarrativeGapAnalyzer - Compares official vs actual narratives
2. FrameCompetitionAnalyzer - Maps competing frames
3. CulturalSignalDetector - Detects innovation culture
4. ResistanceMapper - Identifies adoption barriers
5. AdoptionReadinessScorer - Scores organizational readiness

Implements 5 strategic question workflows:
- Q1: How do different teams talk about AI differently?
- Q2: Do we have an entrepreneurial culture?
- Q3: Can you design a unified story?
- Q4: Are we risk-averse?
- Q5: Why does language vary by context?
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from .analysis.narrative_gap_analyzer import NarrativeGapAnalyzer
from .analysis.frame_competition_analyzer import FrameCompetitionAnalyzer
from .analysis.cultural_signal_detector import CulturalSignalDetector
from .analysis.resistance_mapper import ResistanceMapper
from .analysis.adoption_readiness_scorer import AdoptionReadinessScorer


class AInarrativeIntelligenceAgent:
    """
    Main orchestrator for AI narrative intelligence analysis.

    Coordinates sub-agents to provide comprehensive insights about organizational
    AI adoption readiness, cultural patterns, and narrative dynamics.
    """

    def __init__(self, neo4j_client):
        """
        Initialize the AI Narrative Intelligence Agent with all sub-agents.

        Args:
            neo4j_client: Neo4j database client for querying narrative data
        """
        self.neo4j = neo4j_client

        # Initialize all sub-agents
        # Note: Most use global neo4j_client, but AdoptionReadinessScorer needs it passed in
        self.gap_analyzer = NarrativeGapAnalyzer()
        self.frame_analyzer = FrameCompetitionAnalyzer()
        self.culture_detector = CulturalSignalDetector()
        self.resistance_mapper = ResistanceMapper()
        self.readiness_scorer = AdoptionReadinessScorer(neo4j_client)

    # ==================== STRATEGIC QUESTION WORKFLOWS ====================

    def answer_question_1(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Q1: How do different teams/departments talk about AI differently?

        Reveals:
        - Vocabulary gaps (official vs employee terms)
        - Frame differences (opportunity vs threat)
        - Sentiment variations across groups
        - Sophistication levels

        Workflow:
        1. Use NarrativeGapAnalyzer to compare official vs actual stories
        2. Use FrameCompetitionAnalyzer to map frame usage by group
        3. Synthesize into executive summary

        Args:
            initiative_id: Optional specific initiative to analyze

        Returns:
            Dict with vocabulary_gaps, frame_differences, sentiment_map,
            group_patterns, and recommendations
        """
        # Step 1: Analyze narrative gaps
        gap_analysis = self.gap_analyzer.analyze_official_vs_actual(initiative_id)

        # Step 2: Map frame competition by group
        frame_map = self.frame_analyzer.map_competing_frames(initiative_id)
        group_frames = frame_map.get('dominant_frame_by_group', {})

        # Step 3: Get group-level sentiment patterns
        group_sentiment = self._analyze_group_sentiment(initiative_id)

        # Step 4: Identify sophistication gaps
        sophistication_gaps = self._analyze_sophistication_by_group(initiative_id)

        # Step 5: Synthesize findings
        synthesis = self._synthesize_q1_findings(
            gap_analysis, group_frames, group_sentiment, sophistication_gaps
        )

        return {
            'question': 'How do different teams talk about AI differently?',
            'vocabulary_gaps': gap_analysis['dimensions']['vocabulary'],
            'frame_differences': group_frames,
            'sentiment_map': group_sentiment,
            'sophistication_gaps': sophistication_gaps,
            'key_insights': synthesis['insights'],
            'implications': synthesis['implications'],
            'recommendations': synthesis['recommendations'],
            'analyzed_at': datetime.now().isoformat()
        }

    def answer_question_2(self) -> Dict[str, Any]:
        """
        Q2: Do we have an entrepreneurial culture that supports AI?

        Measures:
        - Innovation vs risk-aversion signals
        - Experimentation indicators
        - Failure tolerance
        - Employee agency
        - Iteration speed

        Workflow:
        1. Use CulturalSignalDetector to assess innovation culture
        2. Use ResistanceMapper to identify blockers
        3. Use AdoptionReadinessScorer for learning orientation
        4. Synthesize into culture profile

        Returns:
            Dict with culture_score, dimensions, evidence, classification,
            and recommendations
        """
        # Step 1: Assess innovation culture
        culture_assessment = self.culture_detector.assess_innovation_culture()

        # Step 2: Identify resistance patterns (inverse of entrepreneurial culture)
        resistance_landscape = self.resistance_mapper.map_resistance_landscape()

        # Step 3: Check learning orientation
        readiness = self.readiness_scorer.assess_readiness()
        learning_score = readiness['dimension_scores']['learning_orientation']

        # Step 4: Synthesize into culture profile
        culture_profile = self._synthesize_q2_findings(
            culture_assessment, resistance_landscape, learning_score
        )

        return {
            'question': 'Do we have an entrepreneurial culture?',
            'overall_score': culture_assessment['overall_score'],
            'culture_type': culture_assessment['culture_type'],
            'dimension_scores': culture_assessment['dimension_scores'],
            'resistance_patterns': resistance_landscape['hotspots'],
            'learning_orientation': learning_score,
            'classification': culture_profile['classification'],
            'strengths': culture_profile['strengths'],
            'weaknesses': culture_profile['weaknesses'],
            'evidence': culture_profile['evidence'],
            'recommendations': culture_profile['recommendations'],
            'analyzed_at': datetime.now().isoformat()
        }

    def answer_question_3(self, initiative_id: str) -> Dict[str, Any]:
        """
        Q3: Can you design a unified story that bridges different groups?

        Creates:
        - Analysis of current narrative fragmentation
        - Common ground across groups
        - Unified narrative design
        - Messaging strategy

        Workflow:
        1. Use FrameCompetitionAnalyzer to identify conflicts
        2. Find common ground across competing narratives
        3. Design unified story that bridges gaps
        4. Create messaging strategy

        Args:
            initiative_id: Specific initiative to create unified story for

        Returns:
            Dict with current_state, common_ground, unified_story,
            messaging_strategy, and implementation_plan
        """
        # Step 1: Analyze current fragmentation
        frame_conflicts = self.frame_analyzer.identify_frame_conflicts(initiative_id)

        # Step 2: Find common ground
        common_ground = self.frame_analyzer.find_narrative_common_ground(initiative_id)

        # Step 3: Design unified narrative
        unified_design = self.frame_analyzer.design_unified_narrative(initiative_id)

        # Step 4: Create implementation strategy
        implementation = self._create_unified_story_implementation(
            frame_conflicts, common_ground, unified_design
        )

        return {
            'question': 'Can you design a unified story?',
            'current_fragmentation': {
                'conflict_count': len(frame_conflicts),
                'competing_frames': frame_conflicts,
                'conflict_severity': self._assess_conflict_severity(frame_conflicts)
            },
            'common_ground': common_ground,
            'unified_story': unified_design,
            'messaging_strategy': implementation['messaging'],
            'rollout_plan': implementation['rollout'],
            'success_metrics': implementation['metrics'],
            'recommendations': implementation['recommendations'],
            'analyzed_at': datetime.now().isoformat()
        }

    def answer_question_4(self) -> Dict[str, Any]:
        """
        Q4: Are we risk-averse, and where does that show up?

        Identifies:
        - Risk-aversion patterns and locations
        - Root causes (past failures, threat perception, etc.)
        - Impact on adoption
        - Intervention strategies

        Workflow:
        1. Use CulturalSignalDetector to find risk-aversion patterns
        2. Use ResistanceMapper to identify resistance hotspots
        3. Infer root causes
        4. Design interventions

        Returns:
            Dict with risk_aversion_score, patterns, locations, root_causes,
            impact_assessment, and interventions
        """
        # Step 1: Detect risk-aversion patterns
        risk_patterns = self.culture_detector.detect_risk_aversion_patterns()

        # Step 2: Map resistance landscape
        resistance_landscape = self.resistance_mapper.map_resistance_landscape()

        # Step 3: Identify hotspots and infer causes
        hotspots_with_causes = []
        for hotspot in resistance_landscape['hotspots']:
            group = hotspot['group']
            causes = self.resistance_mapper.infer_root_causes(group)
            hotspots_with_causes.append({
                'group': group,
                'resistance_score': hotspot['resistance_score'],
                'patterns': hotspot['patterns'],
                'root_causes': causes['all_causes'],
                'primary_cause': causes['primary_cause']
            })

        # Step 4: Assess impact on adoption
        readiness = self.readiness_scorer.assess_readiness()
        impact = self._assess_risk_aversion_impact(risk_patterns, resistance_landscape, readiness)

        # Step 5: Design interventions
        interventions = self._design_risk_interventions(hotspots_with_causes, impact)

        return {
            'question': 'Are we risk-averse?',
            'risk_aversion_score': risk_patterns['overall_severity'],
            'classification': self._classify_risk_culture(risk_patterns['overall_severity']),
            'patterns': risk_patterns['patterns'],
            'hotspots': hotspots_with_causes,
            'impact_assessment': impact,
            'root_causes_summary': self._summarize_root_causes(hotspots_with_causes),
            'interventions': interventions,
            'recommendations': self._generate_q4_recommendations(hotspots_with_causes, impact),
            'analyzed_at': datetime.now().isoformat()
        }

    def answer_question_5(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Q5: Why does language vary by context? (leadership vs team, official vs actual)

        Explains:
        - Context-driven language differences
        - Audience adaptation patterns
        - Strategic vs tactical framing
        - Trust and transparency indicators

        Workflow:
        1. Use NarrativeGapAnalyzer to identify vocabulary shifts
        2. Use FrameCompetitionAnalyzer to map frame variations
        3. Analyze context patterns (formal vs informal, leadership vs team)
        4. Infer underlying reasons

        Args:
            initiative_id: Optional specific initiative to analyze

        Returns:
            Dict with context_patterns, language_variations, underlying_reasons,
            and implications
        """
        # Step 1: Analyze narrative gaps by context
        gap_analysis = self.gap_analyzer.analyze_official_vs_actual(initiative_id)

        # Step 2: Identify frame usage by role/context
        frame_map = self.frame_analyzer.map_competing_frames(initiative_id)

        # Step 3: Analyze trust levels (affects transparency)
        readiness = self.readiness_scorer.assess_readiness()
        trust_levels = readiness['dimension_scores']['trust_levels']

        # Step 4: Detect sophistication gaps
        sophistication_patterns = self._analyze_sophistication_patterns(initiative_id)

        # Step 5: Infer reasons for variation
        reasons = self._infer_language_variation_reasons(
            gap_analysis, frame_map, trust_levels, sophistication_patterns
        )

        # Step 6: Assess implications
        implications = self._assess_language_variation_implications(reasons)

        return {
            'question': 'Why does language vary by context?',
            'context_patterns': {
                'official_vs_actual': gap_analysis['gap_severity'],
                'leadership_vs_team': self._compare_leadership_team_language(frame_map),
                'formal_vs_informal': sophistication_patterns
            },
            'language_variations': {
                'vocabulary': gap_analysis['dimensions']['vocabulary'],
                'framing': gap_analysis['dimensions']['framing'],
                'emphasis': gap_analysis['dimensions']['emphasis']
            },
            'underlying_reasons': reasons,
            'trust_factor': {
                'score': trust_levels['score'],
                'interpretation': trust_levels['interpretation']
            },
            'implications': implications,
            'recommendations': self._generate_q5_recommendations(reasons, implications),
            'analyzed_at': datetime.now().isoformat()
        }

    # ==================== COMPREHENSIVE ANALYSIS ====================

    def run_comprehensive_analysis(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Run all 5 strategic question workflows and generate executive dashboard.

        Provides complete picture of:
        - Narrative landscape
        - Cultural readiness
        - Adoption barriers
        - Strategic recommendations

        Args:
            initiative_id: Optional specific initiative to analyze

        Returns:
            Dict with all question answers, executive summary, and action plan
        """
        # Run all question workflows
        q1_result = self.answer_question_1(initiative_id)
        q2_result = self.answer_question_2()
        q3_result = self.answer_question_3(initiative_id) if initiative_id else None
        q4_result = self.answer_question_4()
        q5_result = self.answer_question_5(initiative_id)

        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            q1_result, q2_result, q3_result, q4_result, q5_result
        )

        # Create action plan
        action_plan = self._create_action_plan(
            q1_result, q2_result, q3_result, q4_result, q5_result
        )

        return {
            'executive_summary': executive_summary,
            'detailed_analyses': {
                'team_differences': q1_result,
                'entrepreneurial_culture': q2_result,
                'unified_story': q3_result,
                'risk_aversion': q4_result,
                'language_context': q5_result
            },
            'action_plan': action_plan,
            'analyzed_at': datetime.now().isoformat(),
            'initiative_id': initiative_id
        }

    # ==================== HELPER METHODS ====================

    def _analyze_group_sentiment(self, initiative_id: Optional[str]) -> Dict[str, float]:
        """Analyze sentiment patterns by group."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
        """ + (f" AND (s)-[:DESCRIBES_AI]->(:AIInitiative {{id: '{initiative_id}'}})" if initiative_id else "") + """
        RETURN s.teller_group as group,
               avg(s.ai_sentiment) as avg_sentiment,
               count(s) as story_count
        """
        results = self.neo4j.execute_read_query(query)

        sentiment_map = {}
        for record in results:
            group = record['group'] or 'unknown'
            sentiment_map[group] = {
                'average_sentiment': round(record['avg_sentiment'] or 0.0, 3),
                'story_count': record['story_count']
            }

        return sentiment_map

    def _analyze_sophistication_by_group(self, initiative_id: Optional[str]) -> Dict[str, Any]:
        """Analyze AI sophistication levels by group."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
        """ + (f" AND (s)-[:DESCRIBES_AI]->(:AIInitiative {{id: '{initiative_id}'}})" if initiative_id else "") + """
        RETURN s.teller_group as group,
               s.ai_sophistication as sophistication,
               count(s) as count
        """
        results = self.neo4j.execute_read_query(query)

        group_sophistication = {}
        for record in results:
            group = record['group'] or 'unknown'
            sophistication = record['sophistication']

            if group not in group_sophistication:
                group_sophistication[group] = {
                    'basic': 0, 'intermediate': 0, 'advanced': 0, 'expert': 0
                }

            if sophistication in group_sophistication[group]:
                group_sophistication[group][sophistication] = record['count']

        return group_sophistication

    def _synthesize_q1_findings(self, gap_analysis: Dict, group_frames: Dict,
                                group_sentiment: Dict, sophistication: Dict) -> Dict[str, Any]:
        """Synthesize findings for Question 1."""
        insights = []

        # Vocabulary insights
        vocab_gap = gap_analysis['dimensions']['vocabulary']
        if vocab_gap['sophistication_gap'] > 0.3:
            insights.append(f"Significant vocabulary gap: Official messaging uses terms like {vocab_gap['official_only'][:3]} "
                          f"while employees use {vocab_gap['employee_only'][:3]}")

        # Frame insights
        frame_diversity = len(set(group_frames.values()))
        if frame_diversity > 3:
            insights.append(f"High frame diversity: {frame_diversity} different frames across groups indicates lack of unified narrative")

        # Sentiment insights
        sentiment_range = max(s['average_sentiment'] for s in group_sentiment.values()) - \
                         min(s['average_sentiment'] for s in group_sentiment.values())
        if sentiment_range > 0.5:
            insights.append(f"Large sentiment variation (range: {sentiment_range:.2f}) suggests different groups have very different experiences")

        implications = self._derive_q1_implications(insights)
        recommendations = self._generate_q1_recommendations(gap_analysis, group_frames)

        return {
            'insights': insights,
            'implications': implications,
            'recommendations': recommendations
        }

    def _derive_q1_implications(self, insights: List[str]) -> List[str]:
        """Derive business implications from Q1 insights."""
        implications = []

        if any('vocabulary gap' in i for i in insights):
            implications.append("Vocabulary gaps may indicate that official messaging is not resonating with employees")

        if any('frame diversity' in i for i in insights):
            implications.append("Lack of unified narrative creates confusion and reduces adoption momentum")

        if any('sentiment variation' in i for i in insights):
            implications.append("Different experiences across groups suggest inconsistent implementation or support")

        return implications

    def _generate_q1_recommendations(self, gap_analysis: Dict, group_frames: Dict) -> List[str]:
        """Generate recommendations for Q1."""
        recommendations = []

        # Address vocabulary gaps
        vocab_alignment = gap_analysis['dimensions']['vocabulary']['alignment_score']
        if vocab_alignment < 0.5:
            recommendations.append("Create shared vocabulary through storytelling sessions and cross-functional workshops")

        # Address frame conflicts
        if len(set(group_frames.values())) > 3:
            recommendations.append("Facilitate dialogue between groups to develop unified narrative frame")

        recommendations.append("Use employee language in official communications to increase resonance")

        return recommendations

    def _synthesize_q2_findings(self, culture: Dict, resistance: Dict, learning: Dict) -> Dict[str, Any]:
        """Synthesize findings for Question 2."""
        # Determine classification
        innovation_score = culture['overall_score']
        if innovation_score >= 0.7:
            classification = 'entrepreneurial'
        elif innovation_score >= 0.5:
            classification = 'balanced'
        elif innovation_score >= 0.3:
            classification = 'cautious'
        else:
            classification = 'risk_averse'

        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []

        for dim, score_data in culture['dimension_scores'].items():
            if score_data['score'] > 0.7:
                strengths.append(dim)
            elif score_data['score'] < 0.4:
                weaknesses.append(dim)

        # Collect evidence
        evidence = {
            'innovation_indicators': culture['dimension_scores']['experimentation']['score'],
            'failure_tolerance': culture['dimension_scores']['failure_tolerance']['score'],
            'resistance_hotspots': len(resistance['hotspots']),
            'learning_orientation': learning['score']
        }

        # Generate recommendations
        recommendations = []
        if classification in ['cautious', 'risk_averse']:
            recommendations.append("Launch small pilot projects to build confidence through quick wins")
            recommendations.append("Create psychological safety for experimentation and failure")

        if learning['score'] < 0.5:
            recommendations.append("Invest in skill development and training programs")

        return {
            'classification': classification,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'evidence': evidence,
            'recommendations': recommendations
        }

    def _create_unified_story_implementation(self, conflicts: List[Dict],
                                            common_ground: Dict, design: Dict) -> Dict[str, Any]:
        """Create implementation plan for unified story."""
        # Messaging strategy
        messaging = {
            'core_message': design.get('unified_frame', 'AI as collaborative tool'),
            'key_themes': design.get('shared_themes', []),
            'audience_adaptations': self._create_audience_adaptations(design)
        }

        # Rollout plan
        rollout = {
            'phase_1': 'Test unified story with pilot groups',
            'phase_2': 'Gather feedback and refine messaging',
            'phase_3': 'Launch organization-wide through multiple channels',
            'phase_4': 'Monitor adoption and adjust as needed'
        }

        # Success metrics
        metrics = {
            'narrative_alignment': 'Increase alignment score from current to >0.7',
            'frame_consistency': 'Reduce competing frames from ' + str(len(conflicts)) + ' to <2',
            'employee_adoption': 'Track usage of unified language in stories'
        }

        # Recommendations
        recommendations = [
            "Use storytelling formats (not policy docs) to introduce unified narrative",
            "Train leaders to consistently use unified frame in communications",
            "Create templates and examples that embody unified story"
        ]

        return {
            'messaging': messaging,
            'rollout': rollout,
            'metrics': metrics,
            'recommendations': recommendations
        }

    def _create_audience_adaptations(self, design: Dict) -> Dict[str, str]:
        """Create audience-specific adaptations of unified story."""
        return {
            'technical_teams': 'Emphasize practical applications and skill development',
            'leadership': 'Highlight strategic benefits and competitive advantage',
            'customer_facing': 'Focus on customer experience improvements',
            'operations': 'Stress efficiency gains and process improvements'
        }

    def _assess_conflict_severity(self, conflicts: List[Dict]) -> str:
        """Assess severity of frame conflicts."""
        if not conflicts:
            return 'low'

        # Count high-impact conflicts
        high_impact = sum(1 for c in conflicts if c.get('impact', '') == 'high')

        if high_impact >= 2:
            return 'high'
        elif high_impact >= 1 or len(conflicts) >= 3:
            return 'medium'
        else:
            return 'low'

    def _assess_risk_aversion_impact(self, risk_patterns: Dict,
                                    resistance: Dict, readiness: Dict) -> Dict[str, Any]:
        """Assess impact of risk aversion on adoption."""
        # Calculate impact score
        risk_severity = risk_patterns['overall_severity']
        resistance_severity = resistance['overall_severity']
        readiness_score = readiness['overall_score']

        impact_score = (risk_severity + resistance_severity) / 2
        adoption_probability = readiness_score * (1 - impact_score)

        return {
            'impact_score': round(impact_score, 3),
            'adoption_probability': round(adoption_probability, 3),
            'classification': self._classify_impact(impact_score),
            'affected_groups': [h['group'] for h in resistance['hotspots']],
            'implications': self._derive_risk_implications(impact_score, adoption_probability)
        }

    def _classify_impact(self, impact_score: float) -> str:
        """Classify impact severity."""
        if impact_score >= 0.7:
            return 'critical'
        elif impact_score >= 0.5:
            return 'high'
        elif impact_score >= 0.3:
            return 'moderate'
        else:
            return 'low'

    def _derive_risk_implications(self, impact: float, adoption_prob: float) -> List[str]:
        """Derive implications of risk aversion."""
        implications = []

        if impact >= 0.7:
            implications.append("Risk aversion is a critical barrier to adoption")

        if adoption_prob < 0.5:
            implications.append("Current adoption probability is below 50% - intervention required")

        implications.append("Risk-averse culture will slow adoption and limit experimentation")

        return implications

    def _design_risk_interventions(self, hotspots: List[Dict], impact: Dict) -> List[Dict]:
        """Design interventions for risk-averse groups."""
        interventions = []

        for hotspot in hotspots:
            group = hotspot['group']
            primary_cause = hotspot['primary_cause'][0]

            intervention = {
                'target_group': group,
                'primary_cause': primary_cause,
                'intervention': self._get_intervention_for_cause(primary_cause),
                'timeline': '3-6 months',
                'success_metric': f'Reduce resistance score in {group} below 0.4'
            }
            interventions.append(intervention)

        return interventions

    def _get_intervention_for_cause(self, cause: str) -> str:
        """Get recommended intervention for root cause."""
        interventions = {
            'past_failures': 'Address past failures directly, show what was learned, demonstrate changes',
            'threat_perception': 'Reframe AI from threat to tool, emphasize human augmentation not replacement',
            'resource_issues': 'Provide adequate time, training, and support resources',
            'value_misalignment': 'Connect AI initiative to organizational values and mission',
            'knowledge_gap': 'Invest in education, skill development, and hands-on experience'
        }
        return interventions.get(cause, 'Design targeted intervention based on root cause analysis')

    def _summarize_root_causes(self, hotspots: List[Dict]) -> Dict[str, int]:
        """Summarize root causes across all hotspots."""
        cause_counts = {}

        for hotspot in hotspots:
            primary_cause = hotspot['primary_cause'][0]
            cause_counts[primary_cause] = cause_counts.get(primary_cause, 0) + 1

        return cause_counts

    def _generate_q4_recommendations(self, hotspots: List[Dict], impact: Dict) -> List[str]:
        """Generate recommendations for Q4."""
        recommendations = []

        if impact['classification'] in ['critical', 'high']:
            recommendations.append("URGENT: Risk aversion is blocking adoption - immediate intervention required")

        # Most common root cause
        cause_counts = self._summarize_root_causes(hotspots)
        if cause_counts:
            most_common = max(cause_counts, key=cause_counts.get)
            recommendations.append(f"Focus on addressing {most_common} which affects {cause_counts[most_common]} groups")

        recommendations.append("Create safe spaces for experimentation with low stakes")
        recommendations.append("Celebrate learning from failures to shift culture")

        return recommendations

    def _analyze_sophistication_patterns(self, initiative_id: Optional[str]) -> Dict[str, Any]:
        """Analyze sophistication patterns across contexts."""
        sophistication_by_group = self._analyze_sophistication_by_group(initiative_id)

        # Identify patterns
        patterns = {
            'high_sophistication_groups': [],
            'low_sophistication_groups': [],
            'gap_size': 0.0
        }

        for group, levels in sophistication_by_group.items():
            total = sum(levels.values())
            if total == 0:
                continue

            advanced_pct = (levels.get('advanced', 0) + levels.get('expert', 0)) / total
            if advanced_pct > 0.5:
                patterns['high_sophistication_groups'].append(group)
            elif advanced_pct < 0.2:
                patterns['low_sophistication_groups'].append(group)

        # Calculate gap
        if patterns['high_sophistication_groups'] and patterns['low_sophistication_groups']:
            patterns['gap_size'] = 0.7  # Significant gap exists

        return patterns

    def _infer_language_variation_reasons(self, gap_analysis: Dict, frame_map: Dict,
                                         trust_levels: Dict, sophistication: Dict) -> List[Dict]:
        """Infer reasons for language variation."""
        reasons = []

        # Reason 1: Audience adaptation
        if gap_analysis['gap_severity'] in ['moderate', 'high']:
            reasons.append({
                'reason': 'audience_adaptation',
                'explanation': 'Leadership adapts language for different audiences',
                'evidence': 'Vocabulary and framing differences between official and employee stories'
            })

        # Reason 2: Trust and transparency
        if trust_levels['score'] < 0.5:
            reasons.append({
                'reason': 'low_trust',
                'explanation': 'Low trust leads to guarded official communication',
                'evidence': f"Trust score of {trust_levels['score']} indicates credibility issues"
            })

        # Reason 3: Knowledge gaps
        if sophistication['gap_size'] > 0.5:
            reasons.append({
                'reason': 'knowledge_gaps',
                'explanation': 'Different groups have different levels of AI understanding',
                'evidence': f"Sophistication gaps between {sophistication['high_sophistication_groups']} and {sophistication['low_sophistication_groups']}"
            })

        # Reason 4: Strategic vs tactical focus
        reasons.append({
            'reason': 'strategic_vs_tactical',
            'explanation': 'Leadership focuses on strategy while teams focus on tactical execution',
            'evidence': 'Different emphasis patterns in official vs employee narratives'
        })

        return reasons

    def _assess_language_variation_implications(self, reasons: List[Dict]) -> List[str]:
        """Assess implications of language variation."""
        implications = []

        for reason in reasons:
            if reason['reason'] == 'audience_adaptation':
                implications.append("Natural and acceptable if intentional and strategic")
            elif reason['reason'] == 'low_trust':
                implications.append("Language gaps may indicate deeper trust and transparency issues")
            elif reason['reason'] == 'knowledge_gaps':
                implications.append("Training and education needed to bring groups to similar understanding")
            elif reason['reason'] == 'strategic_vs_tactical':
                implications.append("Need to better connect strategic vision to tactical execution")

        return implications

    def _generate_q5_recommendations(self, reasons: List[Dict], implications: List[str]) -> List[str]:
        """Generate recommendations for Q5."""
        recommendations = []

        for reason in reasons:
            if reason['reason'] == 'low_trust':
                recommendations.append("Build trust through transparency and consistent follow-through")
            elif reason['reason'] == 'knowledge_gaps':
                recommendations.append("Provide training to elevate understanding across all groups")
            elif reason['reason'] == 'strategic_vs_tactical':
                recommendations.append("Create explicit connections between strategic goals and tactical work")

        recommendations.append("Acknowledge and explain intentional language adaptations to build understanding")

        return recommendations

    def _compare_leadership_team_language(self, frame_map: Dict) -> Dict[str, Any]:
        """Compare language patterns between leadership and teams."""
        leadership_frames = {}
        team_frames = {}

        for group, frame in frame_map.get('dominant_frame_by_group', {}).items():
            if 'leadership' in group.lower() or 'executive' in group.lower():
                leadership_frames[group] = frame
            else:
                team_frames[group] = frame

        return {
            'leadership_frames': leadership_frames,
            'team_frames': team_frames,
            'alignment': self._calculate_frame_alignment(leadership_frames, team_frames)
        }

    def _calculate_frame_alignment(self, frames1: Dict, frames2: Dict) -> float:
        """Calculate alignment between two sets of frames."""
        if not frames1 or not frames2:
            return 0.5

        # Count matching frames
        matches = sum(1 for f1 in frames1.values() for f2 in frames2.values() if f1 == f2)
        total_comparisons = len(frames1) * len(frames2)

        return matches / total_comparisons if total_comparisons > 0 else 0.5

    def _classify_risk_culture(self, severity: float) -> str:
        """Classify organizational risk culture."""
        if severity >= 0.7:
            return 'highly_risk_averse'
        elif severity >= 0.5:
            return 'moderately_risk_averse'
        elif severity >= 0.3:
            return 'balanced'
        else:
            return 'risk_tolerant'

    def _generate_executive_summary(self, q1: Dict, q2: Dict, q3: Optional[Dict],
                                   q4: Dict, q5: Dict) -> Dict[str, Any]:
        """Generate executive summary from all analyses."""
        # Key findings
        key_findings = [
            f"Narrative alignment: {q1['vocabulary_gaps']['alignment_score']:.2f}",
            f"Culture type: {q2['culture_type']}",
            f"Risk aversion: {q4['classification']}",
            f"Overall readiness: {q2.get('overall_score', 0):.2f}"
        ]

        # Critical issues
        critical_issues = []
        if q2['overall_score'] < 0.5:
            critical_issues.append("Low overall readiness score requires intervention")
        if q4['risk_aversion_score'] > 0.7:
            critical_issues.append("High risk aversion is blocking adoption")
        if q1['vocabulary_gaps']['alignment_score'] < 0.4:
            critical_issues.append("Severe narrative fragmentation across groups")

        # Top recommendations
        top_recommendations = []
        if critical_issues:
            top_recommendations.extend([
                "Address critical barriers before full-scale rollout",
                "Focus interventions on groups with highest resistance",
                "Build trust and transparency through consistent communication"
            ])
        else:
            top_recommendations.extend([
                "Proceed with rollout while monitoring weak dimensions",
                "Leverage strengths to build momentum",
                "Maintain alignment through ongoing narrative coordination"
            ])

        return {
            'key_findings': key_findings,
            'critical_issues': critical_issues if critical_issues else ['No critical issues identified'],
            'top_recommendations': top_recommendations,
            'overall_assessment': self._overall_assessment(q1, q2, q4)
        }

    def _overall_assessment(self, q1: Dict, q2: Dict, q4: Dict) -> str:
        """Provide overall assessment."""
        readiness = q2.get('overall_score', 0)
        risk = q4['risk_aversion_score']

        if readiness >= 0.7 and risk < 0.4:
            return "Organization is well-positioned for successful AI adoption. Proceed with confidence."
        elif readiness >= 0.5 and risk < 0.6:
            return "Organization shows moderate readiness. Address identified gaps before full rollout."
        else:
            return "Organization faces significant adoption challenges. Fundamental interventions required."

    def _create_action_plan(self, q1: Dict, q2: Dict, q3: Optional[Dict],
                           q4: Dict, q5: Dict) -> Dict[str, Any]:
        """Create comprehensive action plan."""
        # Prioritize actions based on severity
        immediate_actions = []
        short_term_actions = []
        long_term_actions = []

        # From Q4 (risk aversion)
        if q4['risk_aversion_score'] > 0.7:
            immediate_actions.extend(q4['recommendations'][:2])

        # From Q2 (culture)
        if q2['overall_score'] < 0.5:
            immediate_actions.extend(q2['recommendations'][:2])

        # From Q1 (alignment)
        if q1['vocabulary_gaps']['alignment_score'] < 0.5:
            short_term_actions.extend(q1['recommendations'])

        # From Q3 (unified story)
        if q3:
            short_term_actions.append("Develop and launch unified narrative")

        # From Q5 (language context)
        long_term_actions.extend(q5['recommendations'])

        return {
            'immediate': {
                'timeline': '0-30 days',
                'actions': immediate_actions[:3]
            },
            'short_term': {
                'timeline': '1-3 months',
                'actions': short_term_actions[:5]
            },
            'long_term': {
                'timeline': '3-6 months',
                'actions': long_term_actions[:3]
            }
        }
