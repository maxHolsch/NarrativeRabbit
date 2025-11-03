"""
AI Narrative Sample Data Generator

Generates realistic, compelling AI narrative data that tells a story about
an organization's AI adoption journey. Designed to showcase all analysis
capabilities with authentic patterns and tensions.

The story: A mid-size tech company introducing AI coding assistants and
customer service automation, revealing cultural tensions between innovation
and caution.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
from uuid import uuid4


class AIDataGenerator:
    """
    Generates realistic AI narrative data with authentic organizational tensions.

    Creates a narrative arc:
    1. Initial excitement (leadership announces AI initiatives)
    2. Emerging skepticism (early adopters vs skeptics)
    3. Resistance patterns (cautionary tales spread)
    4. Competing frames (opportunity vs threat)
    5. Current state (mixed readiness, clear gaps)
    """

    def __init__(self):
        """Initialize with base timestamp for timeline."""
        self.base_time = datetime.now() - timedelta(days=180)  # 6 months ago

    def generate_all_data(self) -> Dict[str, Any]:
        """
        Generate complete AI narrative dataset.

        Returns:
            Dict with initiatives, stories, and metadata
        """
        print("🚀 Generating AI Narrative Sample Data...")
        print("=" * 60)

        # Generate initiatives
        initiatives = self.generate_initiatives()
        print(f"✅ Generated {len(initiatives)} AI initiatives")

        # Generate stories for each initiative
        all_stories = []
        for initiative in initiatives:
            stories = self.generate_stories_for_initiative(initiative)
            all_stories.extend(stories)
            print(f"✅ Generated {len(stories)} stories for {initiative['name']}")

        # Generate standalone AI stories
        general_stories = self.generate_general_ai_stories()
        all_stories.extend(general_stories)
        print(f"✅ Generated {len(general_stories)} general AI stories")

        print("=" * 60)
        print(f"📊 Total: {len(initiatives)} initiatives, {len(all_stories)} stories")

        return {
            'initiatives': initiatives,
            'stories': all_stories,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'time_span_days': 180,
                'narrative_arc': 'introduction_to_resistance'
            }
        }

    def generate_initiatives(self) -> List[Dict[str, Any]]:
        """Generate AI initiatives with realistic properties."""

        initiatives = [
            {
                'id': 'ai_copilot_2024',
                'name': 'GitHub Copilot Pilot Program',
                'type': 'tool',
                'official_description': 'AI-powered coding assistant to boost developer productivity by 30% and accelerate feature delivery',
                'stated_goals': [
                    'Increase developer productivity',
                    'Reduce repetitive coding tasks',
                    'Accelerate time-to-market',
                    'Attract top engineering talent'
                ],
                'status': 'active',
                'official_story_ids': ['story_copilot_official'],
                'actual_story_ids': [],  # Will be populated
                'awareness_score': 0.85,
                'sentiment_score': 0.45,  # Mixed sentiment
                'launch_date': (self.base_time + timedelta(days=30)).isoformat()
            },
            {
                'id': 'ai_customer_service_2024',
                'name': 'AI Customer Service Automation',
                'type': 'transformation',
                'official_description': 'Intelligent chatbot to handle 70% of customer inquiries, freeing agents for complex issues',
                'stated_goals': [
                    'Reduce response times',
                    'Scale support without headcount',
                    'Improve customer satisfaction',
                    'Reduce operational costs'
                ],
                'status': 'active',
                'official_story_ids': ['story_cs_official'],
                'actual_story_ids': [],
                'awareness_score': 0.90,
                'sentiment_score': -0.15,  # Negative sentiment
                'launch_date': (self.base_time + timedelta(days=60)).isoformat()
            },
            {
                'id': 'ai_analytics_pilot_2024',
                'name': 'Predictive Analytics Engine',
                'type': 'pilot',
                'official_description': 'ML-powered analytics to predict customer churn and optimize retention strategies',
                'stated_goals': [
                    'Reduce churn by 20%',
                    'Identify at-risk customers proactively',
                    'Optimize retention spend',
                    'Data-driven decision making'
                ],
                'status': 'planned',
                'official_story_ids': ['story_analytics_official'],
                'actual_story_ids': [],
                'awareness_score': 0.40,
                'sentiment_score': 0.65,  # Positive but limited awareness
                'launch_date': (self.base_time + timedelta(days=150)).isoformat()
            }
        ]

        return initiatives

    def generate_stories_for_initiative(self, initiative: Dict) -> List[Dict[str, Any]]:
        """Generate diverse stories about an initiative."""

        initiative_id = initiative['id']

        if initiative_id == 'ai_copilot_2024':
            return self._generate_copilot_stories(initiative)
        elif initiative_id == 'ai_customer_service_2024':
            return self._generate_customer_service_stories(initiative)
        elif initiative_id == 'ai_analytics_pilot_2024':
            return self._generate_analytics_stories(initiative)

        return []

    def _generate_copilot_stories(self, initiative: Dict) -> List[Dict[str, Any]]:
        """Generate stories about GitHub Copilot adoption."""

        stories = []

        # Official story - optimistic framing
        stories.append({
            'id': 'story_copilot_official',
            'content': 'Leadership announced GitHub Copilot to accelerate our development velocity. "This is about empowering our developers," said the CTO. "AI will handle the boilerplate so our team can focus on creative problem-solving and innovation. Early benchmarks show 30% productivity gains. This positions us as a tech-forward company that attracts top talent."',
            'teller_group': 'leadership',
            'teller_role': 'CTO',
            'timestamp': (self.base_time + timedelta(days=30)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.8,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'experimentation',
            'agency_frame': 'opportunity',
            'time_frame': 'future_focused',
            'narrative_function': 'vision',
            'ai_concepts_mentioned': ['github copilot', 'productivity', 'automation', 'developer tools'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Early adopter - enthusiastic
        stories.append({
            'id': 'story_copilot_early_adopter',
            'content': 'I\'ve been using Copilot for three weeks and it\'s genuinely helpful. Yes, you have to review everything it suggests, but for writing tests and boilerplate, it saves real time. I\'m shipping features faster. The trick is knowing when to trust it and when to ignore it. It\'s like having a junior dev who works instantly but needs supervision.',
            'teller_group': 'engineering',
            'teller_role': 'senior_engineer',
            'timestamp': (self.base_time + timedelta(days=45)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.6,
            'ai_sophistication': 'advanced',
            'innovation_signal': 'learning',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'success',
            'ai_concepts_mentioned': ['copilot', 'code generation', 'testing', 'productivity'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Skeptic - quality concerns
        stories.append({
            'id': 'story_copilot_skeptic',
            'content': 'I tried Copilot but turned it off after a week. It was suggesting insecure code patterns that a junior dev wouldn\'t catch. I spent more time reviewing and fixing its suggestions than writing code myself. The 30% productivity claim feels inflated. Maybe for simple CRUD stuff, but for complex logic? It\'s noise. I\'m worried about what happens when junior developers rely on it without understanding the code.',
            'teller_group': 'engineering',
            'teller_role': 'senior_engineer',
            'timestamp': (self.base_time + timedelta(days=60)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.4,
            'ai_sophistication': 'advanced',
            'innovation_signal': 'caution',
            'agency_frame': 'threat',
            'time_frame': 'present_focused',
            'narrative_function': 'warning',
            'ai_concepts_mentioned': ['copilot', 'code quality', 'security', 'code review'],
            'experimentation_indicator': True,
            'failure_framing': 'quality_risk'
        })

        # Mid-level engineer - mixed feelings
        stories.append({
            'id': 'story_copilot_mixed',
            'content': 'Copilot is useful but weird. Sometimes it autocompletes entire functions perfectly. Other times it hallucinates APIs that don\'t exist. I find myself second-guessing my own code now - did I write this or did Copilot? Are we actually getting better at coding or just better at prompting an AI? Not sure how I feel about that.',
            'teller_group': 'engineering',
            'teller_role': 'mid_level_engineer',
            'timestamp': (self.base_time + timedelta(days=75)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.1,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'ambivalence',
            'agency_frame': 'partner',
            'time_frame': 'present_focused',
            'narrative_function': 'exploration',
            'ai_concepts_mentioned': ['copilot', 'autocomplete', 'code generation', 'ai hallucination'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Junior engineer - dependency concern
        stories.append({
            'id': 'story_copilot_junior_concern',
            'content': 'As a junior developer, Copilot feels like both a blessing and a curse. It helps me move fast, but I worry I\'m not learning properly. When Copilot writes a complex regex or a tricky algorithm, I often just accept it without fully understanding. My senior dev said I should "learn without it first," but everyone else is using it. Am I falling behind by not understanding the code I\'m shipping?',
            'teller_group': 'engineering',
            'teller_role': 'junior_engineer',
            'timestamp': (self.base_time + timedelta(days=90)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.2,
            'ai_sophistication': 'basic',
            'innovation_signal': 'concern',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'complication',
            'ai_concepts_mentioned': ['copilot', 'learning', 'skill development', 'dependency'],
            'experimentation_indicator': True,
            'failure_framing': 'skill_erosion'
        })

        # Engineering manager - adoption pressure
        stories.append({
            'id': 'story_copilot_manager_pressure',
            'content': 'Leadership keeps asking why my team isn\'t showing the promised 30% productivity gains with Copilot. But that number came from a cherry-picked study. My team is split - some love it, others find it distracting. I\'m stuck between pushing adoption to hit metrics and letting engineers work however they\'re most effective. The pressure to show ROI is real.',
            'teller_group': 'engineering_management',
            'teller_role': 'engineering_manager',
            'timestamp': (self.base_time + timedelta(days=105)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.3,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'resistance',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'complication',
            'ai_concepts_mentioned': ['copilot', 'productivity metrics', 'roi', 'adoption'],
            'experimentation_indicator': False,
            'failure_framing': 'unrealistic_expectations'
        })

        return stories

    def _generate_customer_service_stories(self, initiative: Dict) -> List[Dict[str, Any]]:
        """Generate stories about customer service AI automation."""

        stories = []

        # Official story - efficiency framing
        stories.append({
            'id': 'story_cs_official',
            'content': 'Our AI customer service chatbot will transform how we support customers. By handling routine inquiries automatically, we free our agents to solve complex problems where human empathy matters most. This isn\'t about replacing people - it\'s about elevating their work. Customers get faster responses, agents get more interesting work, and we scale sustainably.',
            'teller_group': 'leadership',
            'teller_role': 'VP_Customer_Success',
            'timestamp': (self.base_time + timedelta(days=60)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.7,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'strategic',
            'agency_frame': 'opportunity',
            'time_frame': 'future_focused',
            'narrative_function': 'vision',
            'ai_concepts_mentioned': ['chatbot', 'automation', 'customer service', 'ai support'],
            'experimentation_indicator': False,
            'failure_framing': None
        })

        # Customer service agent - job security fear
        stories.append({
            'id': 'story_cs_agent_fear',
            'content': 'They say the AI is here to "help us," but everyone knows what "handling 70% of inquiries" really means. That\'s 70% of the work we do. How many of us will still have jobs in a year? They keep saying "elevating our work" but what they mean is "needing fewer of you." I\'ve been here five years. Now I\'m training the system that might replace me.',
            'teller_group': 'customer_service',
            'teller_role': 'support_agent',
            'timestamp': (self.base_time + timedelta(days=75)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.7,
            'ai_sophistication': 'basic',
            'innovation_signal': 'fear',
            'agency_frame': 'replacement',
            'time_frame': 'future_concerned',
            'narrative_function': 'warning',
            'ai_concepts_mentioned': ['automation', 'job security', 'replacement', 'workforce reduction'],
            'experimentation_indicator': False,
            'failure_framing': 'job_loss'
        })

        # CS Manager - quality degradation
        stories.append({
            'id': 'story_cs_quality_concern',
            'content': 'The chatbot is live and the metrics look good on paper - response times are down, ticket volume is down. But customer satisfaction isn\'t improving. The AI escalates issues poorly, gives technically correct but unhelpful answers, and frustrates people who just want to talk to a human. We\'re optimizing for efficiency at the cost of experience. I hear "just get me to a real person" multiple times daily.',
            'teller_group': 'customer_service_management',
            'teller_role': 'cs_manager',
            'timestamp': (self.base_time + timedelta(days=95)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.5,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'concern',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'complication',
            'ai_concepts_mentioned': ['chatbot', 'customer satisfaction', 'escalation', 'quality'],
            'experimentation_indicator': False,
            'failure_framing': 'quality_degradation'
        })

        # Senior agent - augmentation working
        stories.append({
            'id': 'story_cs_agent_positive',
            'content': 'Honestly? The AI is helpful. It handles password resets and basic questions so I can focus on actual problems. My job is more interesting now - I\'m solving puzzles instead of repeating the same answers fifty times a day. Yes, some colleagues are worried about layoffs, but we\'re understaffed anyway. The AI helps us keep up with volume.',
            'teller_group': 'customer_service',
            'teller_role': 'senior_support_agent',
            'timestamp': (self.base_time + timedelta(days=110)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.5,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'acceptance',
            'agency_frame': 'partner',
            'time_frame': 'present_focused',
            'narrative_function': 'success',
            'ai_concepts_mentioned': ['chatbot', 'augmentation', 'productivity', 'job enrichment'],
            'experimentation_indicator': False,
            'failure_framing': None
        })

        # Customer feedback surfaced by agent
        stories.append({
            'id': 'story_cs_customer_feedback',
            'content': 'I keep getting customer complaints about the chatbot. "It doesn\'t understand my question," "I\'m stuck in a loop," "Why can\'t I just talk to someone?" We\'re measuring ticket deflection as success, but are we measuring customer frustration? One customer told me they almost canceled because they couldn\'t get help. The AI might be efficient, but efficient doesn\'t always mean effective.',
            'teller_group': 'customer_service',
            'teller_role': 'support_agent',
            'timestamp': (self.base_time + timedelta(days=125)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.6,
            'ai_sophistication': 'basic',
            'innovation_signal': 'resistance',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'warning',
            'ai_concepts_mentioned': ['chatbot', 'customer experience', 'frustration', 'effectiveness'],
            'experimentation_indicator': False,
            'failure_framing': 'customer_dissatisfaction'
        })

        return stories

    def _generate_analytics_stories(self, initiative: Dict) -> List[Dict[str, Any]]:
        """Generate stories about predictive analytics pilot."""

        stories = []

        # Official story - data-driven narrative
        stories.append({
            'id': 'story_analytics_official',
            'content': 'Our predictive analytics pilot uses machine learning to identify at-risk customers before they churn. Instead of reacting to cancellations, we\'ll proactively reach out with targeted retention offers. This is the future of customer success - data-driven, personalized, and proactive. Early models show promising accuracy. We\'re piloting with a small segment before full rollout.',
            'teller_group': 'leadership',
            'teller_role': 'VP_Product',
            'timestamp': (self.base_time + timedelta(days=150)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.75,
            'ai_sophistication': 'advanced',
            'innovation_signal': 'experimentation',
            'agency_frame': 'opportunity',
            'time_frame': 'future_focused',
            'narrative_function': 'vision',
            'ai_concepts_mentioned': ['machine learning', 'predictive analytics', 'churn prediction', 'data science'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Data scientist - cautiously optimistic
        stories.append({
            'id': 'story_analytics_data_scientist',
            'content': 'The churn model shows promise but needs more validation. We\'re seeing good precision but recall is lower than we\'d like - we\'re missing some at-risk customers. The bigger challenge is the feedback loop. If we intervene based on predictions, we change the outcome, which makes the model harder to validate. We need careful experiment design, not just deployment.',
            'teller_group': 'data_science',
            'teller_role': 'data_scientist',
            'timestamp': (self.base_time + timedelta(days=165)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.3,
            'ai_sophistication': 'expert',
            'innovation_signal': 'learning',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'exploration',
            'ai_concepts_mentioned': ['machine learning', 'model validation', 'precision recall', 'feedback loop'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Customer success manager - excited but waiting
        stories.append({
            'id': 'story_analytics_csm_waiting',
            'content': 'I\'m excited about predictive analytics - catching churn before it happens would be game-changing. But it\'s still in pilot. Meanwhile, I\'m losing customers to issues I could have addressed if I\'d known earlier. The promise is there, but the timing feels slow. I want to start using these insights now.',
            'teller_group': 'customer_success',
            'teller_role': 'customer_success_manager',
            'timestamp': (self.base_time + timedelta(days=170)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.4,
            'ai_sophistication': 'basic',
            'innovation_signal': 'anticipation',
            'agency_frame': 'opportunity',
            'time_frame': 'future_focused',
            'narrative_function': 'aspiration',
            'ai_concepts_mentioned': ['predictive analytics', 'churn prevention', 'customer insights'],
            'experimentation_indicator': False,
            'failure_framing': None
        })

        return stories

    def generate_general_ai_stories(self) -> List[Dict[str, Any]]:
        """Generate general AI-related stories not tied to specific initiatives."""

        stories = []

        # Past AI failure reference
        stories.append({
            'id': 'story_past_ai_failure',
            'content': 'Remember the "AI-powered recommendation engine" we tried three years ago? Leadership was equally excited then. Promised personalization, increased engagement, higher conversion. Six months later, quietly shelved. The recommendations were random, sometimes offensive. We never talked about why it failed or what we learned. Now we\'re doing AI again, but nobody mentions that project. Are we making the same mistakes?',
            'teller_group': 'product_management',
            'teller_role': 'senior_product_manager',
            'timestamp': (self.base_time + timedelta(days=50)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.55,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'skepticism',
            'agency_frame': 'threat',
            'time_frame': 'past_focused',
            'narrative_function': 'warning',
            'ai_concepts_mentioned': ['ai projects', 'past failures', 'recommendations', 'lessons learned'],
            'experimentation_indicator': False,
            'failure_framing': 'repeated_mistakes'
        })

        # Learning and growth perspective
        stories.append({
            'id': 'story_ai_learning_mindset',
            'content': 'I\'ve been reading about AI and taking courses to understand what\'s possible and what\'s hype. The technology is real, but the deployment is hard. We need to experiment, fail fast, learn, and iterate. My concern is we\'re treating AI like purchasing software - implement and done. But AI needs continuous tuning, feedback, and improvement. Do we have the culture for that kind of learning?',
            'teller_group': 'engineering',
            'teller_role': 'staff_engineer',
            'timestamp': (self.base_time + timedelta(days=80)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.2,
            'ai_sophistication': 'advanced',
            'innovation_signal': 'learning',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'reflection',
            'ai_concepts_mentioned': ['ai implementation', 'continuous improvement', 'learning culture', 'iteration'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Generational divide
        stories.append({
            'id': 'story_ai_generational_divide',
            'content': 'There\'s a clear divide in how people view AI. Younger team members see it as just another tool, like Stack Overflow or IDEs. Older folks, especially those who\'ve been through multiple "next big thing" cycles, are more skeptical. It\'s not about technical ability - it\'s about having seen promises before. Both perspectives are valid, but they\'re talking past each other.',
            'teller_group': 'engineering_management',
            'teller_role': 'director_of_engineering',
            'timestamp': (self.base_time + timedelta(days=100)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.0,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'observation',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'reflection',
            'ai_concepts_mentioned': ['ai adoption', 'generational differences', 'technology cycles', 'skepticism'],
            'experimentation_indicator': False,
            'failure_framing': None
        })

        # Competitive pressure
        stories.append({
            'id': 'story_ai_competitive_pressure',
            'content': 'Competitors are talking about AI constantly - AI features, AI infrastructure, AI-first companies. We need to be in this conversation or we look behind. But are we adopting AI because it solves real problems or because everyone else is? I worry we\'re being reactive instead of strategic. What\'s our actual AI thesis beyond "we need to do something"?',
            'teller_group': 'product_management',
            'teller_role': 'product_manager',
            'timestamp': (self.base_time + timedelta(days=115)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.1,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'pressure',
            'agency_frame': 'requirement',
            'time_frame': 'present_focused',
            'narrative_function': 'complication',
            'ai_concepts_mentioned': ['competitive positioning', 'ai strategy', 'market pressure', 'strategic clarity'],
            'experimentation_indicator': False,
            'failure_framing': None
        })

        # Ethics and responsibility
        stories.append({
            'id': 'story_ai_ethics_concern',
            'content': 'We\'re deploying AI systems that affect customers and employees, but who\'s thinking about ethics? What happens when the churn model is biased against certain customer segments? When the chatbot gives harmful advice? When Copilot suggests vulnerable code? We need governance, not just deployment. Someone should be asking "should we?" not just "can we?"',
            'teller_group': 'engineering',
            'teller_role': 'principal_engineer',
            'timestamp': (self.base_time + timedelta(days=130)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.3,
            'ai_sophistication': 'expert',
            'innovation_signal': 'concern',
            'agency_frame': 'tool',
            'time_frame': 'future_concerned',
            'narrative_function': 'warning',
            'ai_concepts_mentioned': ['ai ethics', 'bias', 'governance', 'responsibility', 'ai safety'],
            'experimentation_indicator': False,
            'failure_framing': 'ethical_risks'
        })

        # Quiet success story
        stories.append({
            'id': 'story_ai_quiet_success',
            'content': 'My team has been using AI for data processing and anomaly detection for months. No fanfare, no announcements. It works well, saves us hours of manual work, and nobody worries about being replaced because it\'s clearly a tool that makes our jobs easier. Maybe the key to successful AI adoption is starting small, proving value quietly, and avoiding the hype cycle.',
            'teller_group': 'data_engineering',
            'teller_role': 'data_engineer',
            'timestamp': (self.base_time + timedelta(days=140)).isoformat(),
            'ai_related': True,
            'ai_sentiment': 0.6,
            'ai_sophistication': 'advanced',
            'innovation_signal': 'pragmatism',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'success',
            'ai_concepts_mentioned': ['ai tools', 'data processing', 'anomaly detection', 'pragmatic adoption'],
            'experimentation_indicator': True,
            'failure_framing': None
        })

        # Leadership misalignment
        stories.append({
            'id': 'story_leadership_mixed_messages',
            'content': 'The CTO says "AI is our future, embrace experimentation." The CFO says "show me ROI in Q2." The CEO says "move fast but don\'t break things." These messages don\'t align. Teams are stuck between innovating boldly and playing it safe. We need leadership to agree on what success looks like before we can actually achieve it.',
            'teller_group': 'engineering_management',
            'teller_role': 'vp_engineering',
            'timestamp': (self.base_time + timedelta(days=120)).isoformat(),
            'ai_related': True,
            'ai_sentiment': -0.4,
            'ai_sophistication': 'intermediate',
            'innovation_signal': 'confusion',
            'agency_frame': 'tool',
            'time_frame': 'present_focused',
            'narrative_function': 'complication',
            'ai_concepts_mentioned': ['leadership alignment', 'strategic clarity', 'mixed messages', 'success criteria'],
            'experimentation_indicator': False,
            'failure_framing': 'misalignment'
        })

        return stories

    def export_to_json(self, data: Dict[str, Any], filepath: str):
        """Export generated data to JSON file."""
        import json

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n💾 Data exported to: {filepath}")

    def create_neo4j_import_script(self, data: Dict[str, Any]) -> str:
        """
        Create Cypher script to import generated data into Neo4j.

        Returns:
            String containing Cypher CREATE statements
        """
        script_lines = [
            "// AI Narrative Sample Data Import Script",
            "// Generated: " + datetime.now().isoformat(),
            "//",
            "// Run this script in Neo4j Browser or via Python driver",
            "",
            "// ========== CREATE AI INITIATIVES ==========",
            ""
        ]

        # Create initiatives
        for initiative in data['initiatives']:
            script_lines.append(
                f"CREATE (i:AIInitiative {{"
                f"id: '{initiative['id']}', "
                f"name: '{initiative['name']}', "
                f"type: '{initiative['type']}', "
                f"official_description: '{initiative['official_description']}', "
                f"status: '{initiative['status']}', "
                f"awareness_score: {initiative['awareness_score']}, "
                f"sentiment_score: {initiative['sentiment_score']}"
                f"}});"
            )

        script_lines.extend(["", "// ========== CREATE STORIES ==========", ""])

        # Create stories
        for story in data['stories']:
            concepts_str = str(story.get('ai_concepts_mentioned', [])).replace("'", '"')
            script_lines.append(
                f"CREATE (s:Story {{"
                f"id: '{story['id']}', "
                f"content: {repr(story['content'])}, "
                f"teller_group: '{story['teller_group']}', "
                f"teller_role: '{story.get('teller_role', '')}', "
                f"timestamp: '{story['timestamp']}', "
                f"ai_related: {str(story.get('ai_related', False)).lower()}, "
                f"ai_sentiment: {story.get('ai_sentiment', 0.0)}, "
                f"ai_sophistication: '{story.get('ai_sophistication', 'basic')}', "
                f"innovation_signal: '{story.get('innovation_signal', '')}', "
                f"agency_frame: '{story.get('agency_frame', '')}', "
                f"time_frame: '{story.get('time_frame', '')}', "
                f"narrative_function: '{story.get('narrative_function', '')}', "
                f"ai_concepts_mentioned: {concepts_str}, "
                f"experimentation_indicator: {str(story.get('experimentation_indicator', False)).lower()}"
                f"}});"
            )

        return "\n".join(script_lines)


def main():
    """Generate and export sample data."""
    generator = AIDataGenerator()

    # Generate all data
    data = generator.generate_all_data()

    # Export to JSON
    json_path = 'ai_narrative_sample_data.json'
    generator.export_to_json(data, json_path)

    # Create Neo4j import script
    cypher_script = generator.create_neo4j_import_script(data)
    script_path = 'ai_narrative_import.cypher'
    with open(script_path, 'w') as f:
        f.write(cypher_script)

    print(f"💾 Cypher script exported to: {script_path}")
    print("\n✅ Sample data generation complete!")
    print("\nNext steps:")
    print("1. Review generated data in JSON file")
    print("2. Run Cypher script in Neo4j to import")
    print("3. Test AI analysis workflows with realistic data")


if __name__ == '__main__':
    main()
