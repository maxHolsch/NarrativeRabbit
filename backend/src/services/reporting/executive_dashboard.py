"""
Executive Dashboard Service

Creates executive-friendly dashboards with clear insights, risk signals,
and actionable recommendations. Designed for quick understanding and
decision-making.

Key principles:
- Visual clarity over data density
- Risk signals stand out
- Recommendations are specific and prioritized
- Evidence is one click away
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from ..ai_narrative_intelligence_agent import AInarrativeIntelligenceAgent


class ExecutiveDashboard:
    """
    Generate executive dashboards that tell the story clearly.

    Focuses on:
    - What's the situation? (Current state)
    - What's at risk? (Risk signals)
    - What should we do? (Prioritized actions)
    """

    def __init__(self, ai_agent: AInarrativeIntelligenceAgent):
        """Initialize with AI agent."""
        self.agent = ai_agent

    def generate_dashboard(self, initiative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate executive dashboard with key insights.

        Returns dashboard optimized for executive understanding:
        - At-a-glance health metrics
        - Clear risk signals with severity
        - Top 3 recommended actions
        - Supporting evidence available on demand
        """
        # Run comprehensive analysis
        full_analysis = self.agent.run_comprehensive_analysis(initiative_id)

        # Extract key metrics
        health_metrics = self._extract_health_metrics(full_analysis)

        # Identify critical risks
        risk_signals = self._identify_risk_signals(full_analysis)

        # Prioritize actions
        priority_actions = self._prioritize_actions(full_analysis)

        # Create narrative summary
        executive_summary = self._create_executive_narrative(
            health_metrics, risk_signals, priority_actions
        )

        # Generate quick wins
        quick_wins = self._identify_quick_wins(full_analysis)

        return {
            'generated_at': datetime.now().isoformat(),
            'initiative_id': initiative_id,
            'executive_summary': executive_summary,
            'health_metrics': health_metrics,
            'risk_signals': risk_signals,
            'priority_actions': priority_actions,
            'quick_wins': quick_wins,
            'detailed_analyses': full_analysis['detailed_analyses'],
            'action_plan': full_analysis['action_plan']
        }

    def _extract_health_metrics(self, analysis: Dict) -> Dict[str, Any]:
        """
        Extract key health metrics with visual indicators.

        Returns metrics optimized for dashboard display.
        """
        q2 = analysis['detailed_analyses']['entrepreneurial_culture']
        readiness = q2.get('overall_score', 0)

        # Calculate overall health score (0-100)
        health_score = int(readiness * 100)

        # Determine health status
        if health_score >= 75:
            status = 'healthy'
            status_emoji = '✅'
            status_color = 'green'
        elif health_score >= 60:
            status = 'caution'
            status_emoji = '⚠️'
            status_color = 'yellow'
        elif health_score >= 45:
            status = 'at_risk'
            status_emoji = '🔶'
            status_color = 'orange'
        else:
            status = 'critical'
            status_emoji = '🚨'
            status_color = 'red'

        # Get culture type
        culture_type = q2.get('culture_type', 'unknown')

        # Get narrative alignment
        q1 = analysis['detailed_analyses']['team_differences']
        alignment_score = q1['vocabulary_gaps']['alignment_score']
        alignment_pct = int(alignment_score * 100)

        # Get risk aversion level
        q4 = analysis['detailed_analyses']['risk_aversion']
        risk_score = q4.get('risk_aversion_score', 0)
        risk_level = q4.get('classification', 'unknown')

        return {
            'overall_health': {
                'score': health_score,
                'status': status,
                'emoji': status_emoji,
                'color': status_color,
                'label': self._health_label(health_score)
            },
            'culture': {
                'type': culture_type,
                'emoji': self._culture_emoji(culture_type),
                'description': self._culture_description(culture_type)
            },
            'alignment': {
                'score': alignment_pct,
                'status': 'strong' if alignment_pct >= 70 else 'weak' if alignment_pct < 50 else 'moderate',
                'description': f"{alignment_pct}% narrative alignment across teams"
            },
            'risk_posture': {
                'level': risk_level,
                'score': int(risk_score * 100),
                'emoji': '🛡️' if risk_score < 0.5 else '⚠️',
                'description': self._risk_description(risk_level)
            }
        }

    def _identify_risk_signals(self, analysis: Dict) -> List[Dict[str, Any]]:
        """
        Identify and prioritize risk signals.

        Returns risks sorted by severity with clear actions.
        """
        risks = []

        # Check culture readiness
        q2 = analysis['detailed_analyses']['entrepreneurial_culture']
        if q2['overall_score'] < 0.5:
            risks.append({
                'severity': 'high',
                'category': 'culture',
                'title': 'Low Innovation Readiness',
                'description': f"Culture type: {q2['culture_type']}. Organization shows limited readiness for AI adoption.",
                'impact': 'Slow adoption, resistance patterns, initiative failures',
                'recommended_action': 'Launch pilot programs to build confidence through small wins',
                'evidence_link': 'entrepreneurial_culture'
            })

        # Check narrative fragmentation
        q1 = analysis['detailed_analyses']['team_differences']
        if q1['vocabulary_gaps']['alignment_score'] < 0.4:
            risks.append({
                'severity': 'high',
                'category': 'alignment',
                'title': 'Severe Narrative Fragmentation',
                'description': 'Teams are telling fundamentally different stories about AI initiatives.',
                'impact': 'Confused priorities, wasted effort, initiative conflicts',
                'recommended_action': 'Facilitate cross-team storytelling sessions to develop shared language',
                'evidence_link': 'team_differences'
            })

        # Check risk aversion
        q4 = analysis['detailed_analyses']['risk_aversion']
        if q4['risk_aversion_score'] > 0.7:
            risks.append({
                'severity': 'critical',
                'category': 'resistance',
                'title': 'High Risk Aversion Blocking Adoption',
                'description': f"{len(q4.get('hotspots', []))} resistance hotspots identified.",
                'impact': 'Initiatives stall, innovation slows, competitive disadvantage',
                'recommended_action': 'Address root causes in resistant groups before expanding initiatives',
                'evidence_link': 'risk_aversion'
            })

        # Check trust levels
        readiness = analysis['detailed_analyses'].get('entrepreneurial_culture', {})
        # Note: In full implementation, would extract from readiness scorer

        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        risks.sort(key=lambda x: severity_order.get(x['severity'], 4))

        return risks[:5]  # Top 5 risks

    def _prioritize_actions(self, analysis: Dict) -> List[Dict[str, Any]]:
        """
        Prioritize recommended actions.

        Returns top 3-5 actions with clear owners and timelines.
        """
        action_plan = analysis.get('action_plan', {})

        prioritized = []

        # Immediate actions (0-30 days)
        immediate = action_plan.get('immediate', {}).get('actions', [])
        for action in immediate[:2]:  # Top 2 immediate
            prioritized.append({
                'priority': 'immediate',
                'timeline': '0-30 days',
                'action': action,
                'why_now': 'Critical blocker or high-impact opportunity',
                'suggested_owner': self._suggest_owner(action),
                'success_metric': self._suggest_metric(action)
            })

        # Short-term actions (1-3 months)
        short_term = action_plan.get('short_term', {}).get('actions', [])
        for action in short_term[:2]:  # Top 2 short-term
            prioritized.append({
                'priority': 'short_term',
                'timeline': '1-3 months',
                'action': action,
                'why_now': 'Addresses structural issues',
                'suggested_owner': self._suggest_owner(action),
                'success_metric': self._suggest_metric(action)
            })

        # Long-term action (top 1)
        long_term = action_plan.get('long_term', {}).get('actions', [])
        if long_term:
            prioritized.append({
                'priority': 'long_term',
                'timeline': '3-6 months',
                'action': long_term[0],
                'why_now': 'Strategic foundation building',
                'suggested_owner': self._suggest_owner(long_term[0]),
                'success_metric': self._suggest_metric(long_term[0])
            })

        return prioritized

    def _create_executive_narrative(self, health_metrics: Dict,
                                   risk_signals: List[Dict],
                                   actions: List[Dict]) -> str:
        """
        Create a 3-paragraph executive narrative.

        Structure:
        1. Current situation
        2. Key challenges
        3. Recommended path forward
        """
        # Paragraph 1: Current situation
        health = health_metrics['overall_health']
        culture = health_metrics['culture']
        alignment = health_metrics['alignment']

        situation = (
            f"Our AI adoption readiness is currently {health['label']} ({health['score']}/100), "
            f"with a {culture['description']} organizational culture. "
            f"Narrative alignment across teams is {alignment['status']} at {alignment['score']}%."
        )

        # Paragraph 2: Key challenges
        if risk_signals:
            top_risk = risk_signals[0]
            challenges = (
                f"The primary challenge is {top_risk['title'].lower()}: {top_risk['description']} "
                f"This creates {top_risk['impact'].lower()}. "
            )

            if len(risk_signals) > 1:
                additional = ", ".join([r['title'] for r in risk_signals[1:3]])
                challenges += f"Additional concerns include {additional}."
        else:
            challenges = "No critical challenges identified. Focus on maintaining momentum."

        # Paragraph 3: Path forward
        if actions:
            immediate_actions = [a['action'] for a in actions if a['priority'] == 'immediate']
            if immediate_actions:
                path_forward = (
                    f"Immediate priority: {immediate_actions[0]} "
                    f"This addresses the most critical blocker and can show results within 30 days. "
                    f"Following this, focus on {actions[1]['action'].lower() if len(actions) > 1 else 'sustaining momentum'}."
                )
            else:
                path_forward = f"Recommended path: {actions[0]['action']} over the next {actions[0]['timeline']}."
        else:
            path_forward = "Continue current trajectory with regular monitoring."

        return f"{situation}\n\n{challenges}\n\n{path_forward}"

    def _identify_quick_wins(self, analysis: Dict) -> List[Dict[str, Any]]:
        """
        Identify quick wins - high impact, low effort actions.

        Returns 2-3 quick wins that can build momentum.
        """
        quick_wins = []

        # Check for easy alignment opportunities
        q1 = analysis['detailed_analyses']['team_differences']
        if q1['vocabulary_gaps']['shared']:
            quick_wins.append({
                'title': 'Amplify Shared Language',
                'description': 'Teams already share common AI terminology. Reinforce this in communications.',
                'effort': 'low',
                'impact': 'medium',
                'timeline': '1-2 weeks',
                'how': 'Create talking points using shared terms. Distribute to managers.'
            })

        # Check for successful patterns
        q2 = analysis['detailed_analyses']['entrepreneurial_culture']
        if q2.get('strengths', []):
            strength = q2['strengths'][0] if q2['strengths'] else None
            if strength:
                quick_wins.append({
                    'title': f'Leverage {strength.replace("_", " ").title()} Strength',
                    'description': f'Your organization excels at {strength}. Showcase success stories.',
                    'effort': 'low',
                    'impact': 'high',
                    'timeline': '2-3 weeks',
                    'how': 'Collect and share 3-5 success stories highlighting this strength.'
                })

        # Add storytelling session as always-valuable quick win
        quick_wins.append({
            'title': 'Cross-Team Storytelling Session',
            'description': 'Bring teams together to share AI experiences and build common understanding.',
            'effort': 'low',
            'impact': 'high',
            'timeline': '1 week',
            'how': 'Schedule 90-min session. Each team shares 1-2 stories. Facilitate finding common themes.'
        })

        return quick_wins[:3]

    # Helper methods for labeling and descriptions

    def _health_label(self, score: int) -> str:
        if score >= 75:
            return "strong and ready"
        elif score >= 60:
            return "moderately ready with gaps"
        elif score >= 45:
            return "at risk, intervention needed"
        else:
            return "critical, major intervention required"

    def _culture_emoji(self, culture_type: str) -> str:
        emoji_map = {
            'entrepreneurial': '🚀',
            'balanced': '⚖️',
            'cautious': '🛡️',
            'risk_averse': '⚠️'
        }
        return emoji_map.get(culture_type, '❓')

    def _culture_description(self, culture_type: str) -> str:
        desc_map = {
            'entrepreneurial': 'innovation-embracing',
            'balanced': 'balanced risk/innovation',
            'cautious': 'cautiously innovative',
            'risk_averse': 'risk-averse'
        }
        return desc_map.get(culture_type, 'unknown culture type')

    def _risk_description(self, risk_level: str) -> str:
        desc_map = {
            'highly_risk_averse': 'Very high resistance to change',
            'moderately_risk_averse': 'Moderate caution around new initiatives',
            'balanced': 'Balanced approach to risk',
            'risk_tolerant': 'Comfortable with innovation risk'
        }
        return desc_map.get(risk_level, 'Unknown risk posture')

    def _suggest_owner(self, action: str) -> str:
        """Suggest appropriate owner based on action content."""
        action_lower = action.lower()

        if 'trust' in action_lower or 'leadership' in action_lower:
            return 'Executive Team'
        elif 'training' in action_lower or 'skill' in action_lower:
            return 'Learning & Development'
        elif 'communication' in action_lower or 'storytelling' in action_lower:
            return 'Internal Communications'
        elif 'technical' in action_lower or 'implementation' in action_lower:
            return 'Engineering Leadership'
        elif 'pilot' in action_lower or 'experiment' in action_lower:
            return 'Innovation Team'
        else:
            return 'Cross-Functional Team'

    def _suggest_metric(self, action: str) -> str:
        """Suggest success metric based on action content."""
        action_lower = action.lower()

        if 'alignment' in action_lower or 'narrative' in action_lower:
            return 'Narrative alignment score increases to >0.7'
        elif 'trust' in action_lower:
            return 'Trust signals in stories increase by 30%'
        elif 'resistance' in action_lower:
            return 'Resistance hotspots reduce by 50%'
        elif 'pilot' in action_lower:
            return 'Pilot shows positive outcomes in 80% of cases'
        elif 'training' in action_lower:
            return '90% of target audience completes training'
        else:
            return 'Stakeholder satisfaction survey shows improvement'


class DetailedReport:
    """
    Generate detailed analytical reports.

    For managers and analysts who need:
    - Deep dives into specific issues
    - Evidence trails
    - Group-by-group breakdowns
    - Intervention strategies
    """

    def __init__(self, ai_agent: AInarrativeIntelligenceAgent):
        """Initialize with AI agent."""
        self.agent = ai_agent

    def generate_team_report(self, group: str) -> Dict[str, Any]:
        """
        Generate team-specific analysis report.

        Deep dive into how a specific team is experiencing AI adoption.
        """
        # Get resistance patterns for this group
        resistance = self.agent.resistance_mapper.map_resistance_landscape()
        group_resistance = next(
            (h for h in resistance.get('hotspots', []) if h['group'] == group),
            None
        )

        # Get root causes
        root_causes = self.agent.resistance_mapper.infer_root_causes(group)

        # Get group's stories and sentiment
        group_stories = self.agent.neo4j.execute_read_query(
            """
            MATCH (s:Story {teller_group: $group})
            WHERE s.ai_related = true
            RETURN s
            ORDER BY s.timestamp DESC
            LIMIT 50
            """,
            {'group': group}
        )

        # Calculate sentiment trends
        sentiments = [s['s'].get('ai_sentiment', 0) for s in group_stories if s['s'].get('ai_sentiment') is not None]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

        # Identify dominant frame
        frames = [s['s'].get('agency_frame') for s in group_stories]
        dominant_frame = max(set(frames), key=frames.count) if frames else 'unknown'

        return {
            'group': group,
            'overview': {
                'story_count': len(group_stories),
                'average_sentiment': round(avg_sentiment, 2),
                'dominant_frame': dominant_frame,
                'resistance_level': group_resistance['resistance_score'] if group_resistance else 0
            },
            'resistance_analysis': group_resistance,
            'root_causes': root_causes,
            'recommended_interventions': self._design_interventions(
                group, group_resistance, root_causes
            ),
            'example_stories': [
                {
                    'content': s['s']['content'][:200] + '...',
                    'sentiment': s['s'].get('ai_sentiment'),
                    'frame': s['s'].get('agency_frame')
                }
                for s in group_stories[:3]
            ]
        }

    def generate_initiative_report(self, initiative_id: str) -> Dict[str, Any]:
        """
        Generate initiative-specific report.

        Complete analysis of a single AI initiative.
        """
        # Run all analyses for this initiative
        gaps = self.agent.gap_analyzer.analyze_official_vs_actual(initiative_id)
        frames = self.agent.frame_analyzer.map_competing_frames(initiative_id)
        readiness = self.agent.readiness_scorer.assess_readiness(initiative_id)
        unified_story = self.agent.answer_question_3(initiative_id)

        return {
            'initiative_id': initiative_id,
            'executive_summary': self._create_initiative_summary(
                gaps, frames, readiness
            ),
            'narrative_gaps': gaps,
            'competing_frames': frames,
            'adoption_readiness': readiness,
            'unified_story_design': unified_story,
            'recommendations': self._create_initiative_recommendations(
                gaps, frames, readiness
            )
        }

    def _design_interventions(self, group: str, resistance: Optional[Dict],
                             root_causes: Dict) -> List[Dict[str, Any]]:
        """Design group-specific interventions."""
        interventions = []

        if not resistance or not root_causes:
            return interventions

        # Get primary cause
        primary_cause_name = root_causes.get('primary_cause', ('unknown', {}))[0]

        # Design intervention based on root cause
        intervention_map = {
            'past_failures': {
                'approach': 'Acknowledge & Learn',
                'actions': [
                    'Host retrospective on past AI initiative',
                    'Document lessons learned publicly',
                    'Show how current approach addresses past issues'
                ],
                'timeline': '4-6 weeks'
            },
            'threat_perception': {
                'approach': 'Reframe & Reassure',
                'actions': [
                    'Share success stories from similar roles',
                    'Provide clear career development paths with AI',
                    'Pilot program showing augmentation not replacement'
                ],
                'timeline': '2-3 months'
            },
            'resource_issues': {
                'approach': 'Resource & Support',
                'actions': [
                    'Allocate dedicated time for AI learning',
                    'Provide training and mentorship',
                    'Reduce other responsibilities during transition'
                ],
                'timeline': '1-2 months'
            },
            'value_misalignment': {
                'approach': 'Connect & Align',
                'actions': [
                    'Facilitate dialogue on values and AI',
                    'Show how AI supports team\'s core values',
                    'Co-design ethical guidelines for AI use'
                ],
                'timeline': '6-8 weeks'
            },
            'knowledge_gap': {
                'approach': 'Educate & Build Skills',
                'actions': [
                    'Tailored training program for group',
                    'Hands-on workshops with real examples',
                    'Peer learning groups and office hours'
                ],
                'timeline': '2-3 months'
            }
        }

        intervention = intervention_map.get(primary_cause_name, {
            'approach': 'Custom Approach Needed',
            'actions': ['Conduct deeper investigation', 'Design tailored intervention'],
            'timeline': 'TBD'
        })

        interventions.append({
            'target_group': group,
            'root_cause': primary_cause_name,
            **intervention,
            'success_indicators': [
                f"Resistance score for {group} drops below 0.4",
                'Positive sentiment in stories increases by 30%',
                'Group references AI initiatives constructively'
            ]
        })

        return interventions

    def _create_initiative_summary(self, gaps: Dict, frames: Dict,
                                   readiness: Dict) -> str:
        """Create executive summary for initiative."""
        gap_severity = gaps.get('gap_severity', {}).get('overall_severity', 'UNKNOWN')
        frame_count = len(frames.get('frames', {}))
        readiness_score = readiness.get('overall_score', 0)

        return (
            f"Initiative shows {gap_severity.lower()} narrative gaps between official and actual stories, "
            f"with {frame_count} competing frames in use. "
            f"Overall adoption readiness is {int(readiness_score * 100)}/100, "
            f"classified as {readiness.get('classification', 'unknown')}."
        )

    def _create_initiative_recommendations(self, gaps: Dict, frames: Dict,
                                          readiness: Dict) -> List[str]:
        """Create initiative-specific recommendations."""
        recommendations = []

        # Based on gap severity
        if gaps.get('gap_severity', {}).get('overall_severity') in ['CRITICAL', 'SIGNIFICANT']:
            recommendations.append(
                "URGENT: Address narrative gaps through cross-team alignment sessions"
            )

        # Based on frame competition
        if len(frames.get('frames', {})) > 3:
            recommendations.append(
                "High frame diversity indicates need for unified messaging strategy"
            )

        # Based on readiness
        if readiness.get('overall_score', 0) < 0.5:
            recommendations.append(
                "Low readiness score suggests slowing rollout to build foundation"
            )

        return recommendations
