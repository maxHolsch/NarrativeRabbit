"""
Generate synthetic narrative data for demonstration and testing.
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import random
import uuid
from faker import Faker

from ..models import (
    Person, Group, Event, Theme, Decision, Outcome, Value, Story,
    ContentLayer, StructureLayer, ActorLayer, ThemeLayer, ContextLayer, VariationLayer,
    StoryType, NarrativeArc, TellingPurpose
)

fake = Faker()


class NarrativeDataGenerator:
    """Generate realistic synthetic organizational narratives."""

    def __init__(self, seed: int = 42):
        """Initialize the generator with a random seed for reproducibility."""
        random.seed(seed)
        Faker.seed(seed)
        self.fake = Faker()

        # Organizational structure
        self.departments = [
            "Engineering", "Product", "Design", "Sales", "Marketing",
            "Customer Success", "Operations", "Executive"
        ]

        self.roles_by_dept = {
            "Engineering": ["Senior Engineer", "Staff Engineer", "Principal Engineer", "Engineering Manager", "VP Engineering"],
            "Product": ["Product Manager", "Senior PM", "Director of Product", "VP Product"],
            "Design": ["UX Designer", "Senior Designer", "Design Lead", "Head of Design"],
            "Sales": ["Account Executive", "Sales Manager", "VP Sales"],
            "Marketing": ["Marketing Manager", "Content Lead", "VP Marketing"],
            "Customer Success": ["CS Manager", "Head of CS"],
            "Operations": ["Operations Manager", "COO"],
            "Executive": ["CEO", "CTO", "CFO"]
        }

        # Narrative templates
        self.story_templates = self._create_story_templates()

    def _create_story_templates(self) -> List[Dict[str, Any]]:
        """Create templates for different types of stories."""
        return [
            {
                "type": StoryType.CRISIS,
                "name": "The Production Outage",
                "themes": ["reliability", "incident response", "communication"],
                "values": ["transparency", "accountability", "customer-first"],
                "department_frames": {
                    "Engineering": "Technical heroics and quick debugging",
                    "Product": "Customer impact and communication strategy",
                    "Executive": "Crisis management and lessons learned"
                }
            },
            {
                "type": StoryType.SUCCESS,
                "name": "The Big Feature Launch",
                "themes": ["innovation", "collaboration", "execution"],
                "values": ["excellence", "teamwork", "user-centric"],
                "department_frames": {
                    "Engineering": "Technical challenges overcome",
                    "Product": "Market validation and customer delight",
                    "Design": "Design thinking and user research"
                }
            },
            {
                "type": StoryType.DECISION,
                "name": "The Tech Stack Migration",
                "themes": ["technical debt", "modernization", "risk management"],
                "values": ["innovation", "pragmatism", "sustainability"],
                "department_frames": {
                    "Engineering": "Technical improvements and developer experience",
                    "Product": "Feature velocity impact and trade-offs",
                    "Executive": "Strategic investment and ROI"
                }
            },
            {
                "type": StoryType.CONFLICT,
                "name": "The Roadmap Disagreement",
                "themes": ["prioritization", "stakeholder alignment", "communication"],
                "values": ["collaboration", "data-driven", "transparency"],
                "department_frames": {
                    "Engineering": "Technical debt vs features",
                    "Product": "Customer needs vs technical requirements",
                    "Sales": "Revenue impact and competitive positioning"
                }
            },
            {
                "type": StoryType.LEARNING,
                "name": "The Failed Experiment",
                "themes": ["experimentation", "learning", "iteration"],
                "values": ["innovation", "learning culture", "resilience"],
                "department_frames": {
                    "Engineering": "Technical learnings and process improvements",
                    "Product": "Market insights and pivot strategy",
                    "Executive": "Culture of experimentation"
                }
            },
            {
                "type": StoryType.SUCCESS,
                "name": "The Hiring Sprint",
                "themes": ["growth", "culture", "team building"],
                "values": ["excellence", "diversity", "growth mindset"],
                "department_frames": {
                    "Engineering": "Technical bar and team scaling",
                    "Operations": "Process and infrastructure",
                    "Executive": "Strategic talent acquisition"
                }
            }
        ]

    def generate_people(self, count: int = 25) -> List[Person]:
        """Generate realistic people across departments."""
        people = []

        for dept in self.departments:
            roles = self.roles_by_dept[dept]
            dept_count = max(1, count // len(self.departments))

            for i in range(dept_count):
                person = Person(
                    id=f"person_{uuid.uuid4().hex[:8]}",
                    name=self.fake.name(),
                    role=random.choice(roles),
                    department=dept,
                    seniority=random.choice(["Junior", "Mid", "Senior", "Staff", "Principal"]),
                    bio=f"{self.fake.job()} with expertise in {self.fake.bs()}"
                )
                people.append(person)

        return people

    def generate_groups(self) -> List[Group]:
        """Generate organizational groups."""
        groups = []

        # Department groups
        for dept in self.departments:
            group = Group(
                id=f"group_{dept.lower().replace(' ', '_')}",
                name=f"{dept} Team",
                type="department",
                description=f"The {dept} department",
                common_themes=self._get_dept_themes(dept),
                values_emphasized=self._get_dept_values(dept)
            )
            groups.append(group)

        # Cross-functional groups
        cross_functional = [
            ("Leadership", ["Executive", "Engineering", "Product"]),
            ("GTM", ["Sales", "Marketing", "Customer Success"]),
            ("Product Development", ["Engineering", "Product", "Design"])
        ]

        for name, depts in cross_functional:
            group = Group(
                id=f"group_{name.lower().replace(' ', '_')}",
                name=name,
                type="cross-functional",
                description=f"Cross-functional group: {', '.join(depts)}"
            )
            groups.append(group)

        return groups

    def _get_dept_themes(self, dept: str) -> List[str]:
        """Get common themes for a department."""
        themes_map = {
            "Engineering": ["technical excellence", "scalability", "innovation", "reliability"],
            "Product": ["user needs", "market fit", "prioritization", "strategy"],
            "Design": ["user experience", "usability", "aesthetics", "research"],
            "Sales": ["revenue", "customer acquisition", "relationships"],
            "Marketing": ["growth", "brand", "storytelling", "metrics"],
            "Customer Success": ["customer satisfaction", "retention", "relationships"],
            "Operations": ["efficiency", "process", "infrastructure"],
            "Executive": ["strategy", "vision", "leadership", "culture"]
        }
        return themes_map.get(dept, [])

    def _get_dept_values(self, dept: str) -> List[str]:
        """Get values emphasized by a department."""
        values_map = {
            "Engineering": ["quality", "innovation", "technical excellence"],
            "Product": ["customer-centric", "data-driven", "impact"],
            "Design": ["empathy", "simplicity", "beauty"],
            "Sales": ["results", "relationships", "persistence"],
            "Marketing": ["creativity", "metrics", "storytelling"],
            "Customer Success": ["customer-first", "responsiveness", "empathy"],
            "Operations": ["efficiency", "reliability", "optimization"],
            "Executive": ["vision", "leadership", "transparency"]
        }
        return values_map.get(dept, [])

    def generate_themes(self) -> List[Theme]:
        """Generate organizational themes."""
        theme_data = [
            ("Innovation", "Pushing boundaries and trying new things", "growth"),
            ("Reliability", "Building stable, dependable systems", "quality"),
            ("Collaboration", "Working together across teams", "culture"),
            ("Customer-First", "Prioritizing customer needs", "values"),
            ("Speed", "Moving quickly and iterating", "execution"),
            ("Technical Debt", "Managing and addressing code quality", "technical"),
            ("Scaling", "Growing systems and teams", "growth"),
            ("Learning", "Continuous improvement and knowledge sharing", "culture"),
            ("Data-Driven", "Making decisions based on evidence", "process"),
            ("Transparency", "Open communication and honesty", "values")
        ]

        themes = []
        for name, desc, category in theme_data:
            theme = Theme(
                id=f"theme_{name.lower().replace('-', '_')}",
                name=name,
                description=desc,
                category=category
            )
            themes.append(theme)

        return themes

    def generate_values(self) -> List[Value]:
        """Generate organizational values."""
        value_data = [
            ("Integrity", "Acting with honesty and strong moral principles"),
            ("Excellence", "Striving for the highest quality in everything we do"),
            ("Innovation", "Embracing creativity and new ideas"),
            ("Collaboration", "Working together to achieve shared goals"),
            ("Customer-Centric", "Putting customers at the heart of everything"),
            ("Transparency", "Being open and honest in all communications"),
            ("Growth Mindset", "Believing in continuous learning and improvement"),
            ("Accountability", "Taking ownership of our actions and results")
        ]

        values = []
        for name, desc in value_data:
            value = Value(
                id=f"value_{name.lower().replace('-', '_').replace(' ', '_')}",
                name=name,
                description=desc,
                typical_expressions=[
                    f"We demonstrated {name} when...",
                    f"This exemplifies our commitment to {name}",
                    f"{name} was at the core of this decision"
                ]
            )
            values.append(value)

        return values

    def generate_stories(
        self,
        people: List[Person],
        groups: List[Group],
        themes: List[Theme],
        values: List[Value],
        count: int = 30
    ) -> Tuple[List[Story], List[Event], List[Decision]]:
        """Generate complete stories with events and decisions."""
        stories = []
        events = []
        decisions = []

        # Generate stories from templates
        templates_to_generate = count // len(self.story_templates) + 1

        for _ in range(templates_to_generate):
            for template in self.story_templates:
                if len(stories) >= count:
                    break

                story, event, decision = self._generate_story_from_template(
                    template, people, groups, themes, values
                )
                stories.append(story)
                events.append(event)
                if decision:
                    decisions.append(decision)

        return stories[:count], events[:count], decisions

    def _generate_story_from_template(
        self,
        template: Dict[str, Any],
        people: List[Person],
        groups: List[Group],
        themes: List[Theme],
        values: List[Value]
    ) -> Tuple[Story, Event, Decision]:
        """Generate a story from a template with multiple perspectives."""

        story_id = f"story_{uuid.uuid4().hex[:8]}"
        event_id = f"event_{uuid.uuid4().hex[:8]}"
        decision_id = f"decision_{uuid.uuid4().hex[:8]}"

        # Random timestamp within last 2 years
        timestamp = datetime.utcnow() - timedelta(days=random.randint(30, 730))

        # Select protagonists from different departments
        dept_frames = template["department_frames"]
        involved_depts = list(dept_frames.keys())
        protagonists = []
        tellers = []

        for dept in involved_depts:
            dept_people = [p for p in people if p.department == dept]
            if dept_people:
                protagonist = random.choice(dept_people)
                protagonists.append(protagonist.name)
                tellers.append(protagonist)

        # Create the event
        event = Event(
            id=event_id,
            name=template["name"],
            description=f"A significant {template['type'].value} event involving {', '.join(involved_depts)}",
            timestamp=timestamp,
            category=template["type"].value,
            participants=[p.id for p in tellers],
            impact="Significant organizational impact",
            severity=random.randint(3, 5)
        )

        # Create decision if applicable
        decision = None
        if template["type"] in [StoryType.DECISION, StoryType.CRISIS]:
            decision = Decision(
                id=decision_id,
                name=f"Decision point in {template['name']}",
                description="Key decision made during this event",
                timestamp=timestamp + timedelta(hours=random.randint(1, 48)),
                decision_makers=[tellers[0].id] if tellers else [],
                rationale="Based on data, team input, and strategic considerations",
                success=random.choice([True, True, False])  # Bias toward success
            )

        # Generate story content (base version)
        content = self._generate_content(template, protagonists)
        structure = self._generate_structure(template)
        actors = self._generate_actors(protagonists, involved_depts)
        theme_layer = self._generate_theme_layer(template, themes, values)
        context = self._generate_context(template, timestamp, involved_depts[0])

        # Generate variations (different perspectives)
        variations = []
        for dept, frame in dept_frames.items():
            teller = next((p for p in people if p.department == dept), None)
            if teller:
                variation = self._generate_variation(
                    teller, dept, frame, template, timestamp
                )
                variations.append(variation)

        # Create the story
        story = Story(
            id=story_id,
            content=content,
            structure=structure,
            actors=actors,
            themes=theme_layer,
            context=context,
            variations=variations,
            source="synthetic_generation",
            confidence_score=1.0,
            tags=template["themes"]
        )

        return story, event, decision

    def _generate_content(self, template: Dict, protagonists: List[str]) -> ContentLayer:
        """Generate story content layer."""
        summaries = {
            "The Production Outage": f"A critical production outage affected customers for 3 hours. {protagonists[0]} led the incident response, coordinating across teams to identify and fix the root cause. The team implemented new monitoring to prevent future occurrences.",
            "The Big Feature Launch": f"After months of development, {protagonists[0]} and the team successfully launched a major new feature. Initial user feedback was overwhelmingly positive, with 40% adoption in the first week.",
            "The Tech Stack Migration": f"{protagonists[0]} championed a migration to a modern tech stack. Despite initial concerns about timeline impact, the migration improved developer productivity by 30% and reduced infrastructure costs.",
            "The Roadmap Disagreement": f"A heated debate emerged between {protagonists[0]} and stakeholders about roadmap priorities. After several discussions and data analysis, the team aligned on a balanced approach addressing both technical debt and new features.",
            "The Failed Experiment": f"An experimental feature tested by {protagonists[0]}'s team failed to achieve expected results. However, the learnings informed future product decisions and strengthened the experimentation process.",
            "The Hiring Sprint": f"Faced with rapid growth needs, {protagonists[0]} led an intensive hiring sprint. The team hired 15 engineers in 3 months while maintaining the quality bar."
        }

        return ContentLayer(
            summary=summaries.get(template["name"], f"A {template['type'].value} story involving {', '.join(protagonists)}"),
            full_text=f"[Full narrative text would go here. This is a detailed account of {template['name']}...]",
            key_quotes=[
                f"\"{self.fake.catch_phrase()}\" - {protagonists[0] if protagonists else 'Team member'}",
                f"\"The key lesson here is {random.choice(['transparency', 'speed', 'collaboration', 'data-driven decision making'])}.\"",
            ],
            outcome=f"Successfully resolved with valuable learnings and process improvements."
        )

    def _generate_structure(self, template: Dict) -> StructureLayer:
        """Generate story structure layer."""
        arcs = {
            NarrativeArc.SETUP: "Initial situation and context established",
            NarrativeArc.COMPLICATION: "Challenge or problem emerged",
            NarrativeArc.RISING_ACTION: "Team mobilized to address the issue",
            NarrativeArc.CLIMAX: "Critical moment of decision or action",
            NarrativeArc.RESOLUTION: "Problem resolved or decision implemented",
            NarrativeArc.REFLECTION: "Team reflected on learnings and next steps"
        }

        causal_chain = [
            {"cause": "Initial trigger event", "effect": "Team mobilization"},
            {"cause": "Team mobilization", "effect": "Problem identification"},
            {"cause": "Problem identification", "effect": "Solution implementation"},
        ]

        return StructureLayer(
            story_type=template["type"],
            narrative_arc=arcs,
            temporal_sequence=["Day 1: Discovery", "Day 2-3: Analysis", "Day 4-5: Resolution"],
            causal_chain=causal_chain
        )

    def _generate_actors(self, protagonists: List[str], depts: List[str]) -> ActorLayer:
        """Generate actor layer."""
        return ActorLayer(
            protagonists=protagonists,
            stakeholders=protagonists + ["Customers", "Leadership"],
            decision_makers=protagonists[:2] if len(protagonists) >= 2 else protagonists,
            group_affiliations=depts
        )

    def _generate_theme_layer(
        self,
        template: Dict,
        themes: List[Theme],
        values: List[Value]
    ) -> ThemeLayer:
        """Generate theme layer."""
        relevant_themes = [t.name for t in themes if t.name.lower() in [x.lower() for x in template["themes"]]]
        relevant_values = [v.name for v in values if v.name.lower() in [x.lower() for x in template["values"]]]

        lessons = [
            "Clear communication is critical during incidents",
            "Invest in monitoring and observability",
            "Process improvements compound over time",
            "Team collaboration drives better outcomes"
        ]

        return ThemeLayer(
            primary_themes=relevant_themes or template["themes"],
            problems_addressed=["Operational efficiency", "Team alignment", "Process gaps"],
            values_expressed=relevant_values or template["values"],
            lessons_learned=random.sample(lessons, k=2)
        )

    def _generate_context(
        self,
        template: Dict,
        timestamp: datetime,
        dept: str
    ) -> ContextLayer:
        """Generate context layer."""
        return ContextLayer(
            timestamp=timestamp,
            era="Growth Phase" if timestamp > datetime.utcnow() - timedelta(days=365) else "Early Stage",
            department=dept,
            project=f"Q{((timestamp.month-1)//3)+1} Initiative",
            why_told=random.choice([TellingPurpose.TEACHING, TellingPurpose.CELEBRATING, TellingPurpose.WARNING]),
            trigger_events=[template["name"]]
        )

    def _generate_variation(
        self,
        teller: Person,
        dept: str,
        frame: str,
        template: Dict,
        timestamp: datetime
    ) -> VariationLayer:
        """Generate a perspective variation."""

        emphasis_map = {
            "Engineering": ["technical details", "system architecture", "root cause"],
            "Product": ["user impact", "business metrics", "customer feedback"],
            "Design": ["user experience", "design decisions", "usability"],
            "Sales": ["revenue impact", "customer relationships", "competitive advantage"],
            "Executive": ["strategic implications", "organizational learning", "cultural values"]
        }

        downplayed_map = {
            "Engineering": ["business concerns", "political aspects"],
            "Product": ["technical complexity", "implementation details"],
            "Design": ["technical constraints", "business pressures"],
            "Sales": ["technical challenges", "operational details"],
            "Executive": ["technical details", "day-to-day operations"]
        }

        return VariationLayer(
            teller_identity=teller.name,
            teller_role=teller.role,
            teller_department=dept,
            audience=["Team", "All-hands", "Leadership"],
            framing=frame,
            emphasis=emphasis_map.get(dept, ["key decisions", "outcomes"]),
            downplayed=downplayed_map.get(dept, []),
            telling_timestamp=timestamp + timedelta(days=random.randint(1, 90))
        )

    def generate_all(self) -> Dict[str, List]:
        """Generate complete dataset."""
        print("Generating people...")
        people = self.generate_people(25)

        print("Generating groups...")
        groups = self.generate_groups()

        print("Generating themes...")
        themes = self.generate_themes()

        print("Generating values...")
        values = self.generate_values()

        print("Generating stories...")
        stories, events, decisions = self.generate_stories(people, groups, themes, values, count=30)

        print(f"Generated: {len(people)} people, {len(groups)} groups, {len(stories)} stories")

        return {
            "people": people,
            "groups": groups,
            "themes": themes,
            "values": values,
            "stories": stories,
            "events": events,
            "decisions": decisions
        }
