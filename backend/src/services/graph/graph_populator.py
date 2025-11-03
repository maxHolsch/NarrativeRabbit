"""
Service for populating the Neo4j graph database with narrative data.
"""
from typing import List, Dict, Any
import logging

from ...db import neo4j_client
from ...models import (
    Person, Group, Event, Theme, Decision, Outcome, Value, Story,
    RelationshipType
)

logger = logging.getLogger(__name__)


class GraphPopulator:
    """Populate Neo4j graph with narrative data."""

    def __init__(self):
        """Initialize the graph populator."""
        self.client = neo4j_client

    def populate_all(self, data: Dict[str, List]) -> None:
        """
        Populate graph with all data.

        Args:
            data: Dictionary containing lists of entities
        """
        logger.info("Starting graph population...")

        # Clear existing data
        self.client.clear_database()

        # Create indexes
        self.client.create_indexes()

        # Create nodes
        self._create_people(data.get("people", []))
        self._create_groups(data.get("groups", []))
        self._create_themes(data.get("themes", []))
        self._create_values(data.get("values", []))
        self._create_events(data.get("events", []))
        self._create_decisions(data.get("decisions", []))
        self._create_stories(data.get("stories", []))

        # Create relationships
        self._create_relationships(data)

        logger.info("Graph population complete!")

        # Print stats
        stats = self.client.get_database_stats()
        logger.info(f"Database stats: {stats}")

    def _create_people(self, people: List[Person]) -> None:
        """Create Person nodes."""
        logger.info(f"Creating {len(people)} Person nodes...")

        for person in people:
            query = """
            CREATE (p:Person)
            SET p = $props
            """
            self.client.execute_write_query(
                query,
                {"props": person.to_graph_node()}
            )

    def _create_groups(self, groups: List[Group]) -> None:
        """Create Group nodes."""
        logger.info(f"Creating {len(groups)} Group nodes...")

        for group in groups:
            query = """
            CREATE (g:Group)
            SET g = $props
            """
            self.client.execute_write_query(
                query,
                {"props": group.to_graph_node()}
            )

    def _create_themes(self, themes: List[Theme]) -> None:
        """Create Theme nodes."""
        logger.info(f"Creating {len(themes)} Theme nodes...")

        for theme in themes:
            query = """
            CREATE (t:Theme)
            SET t = $props
            """
            self.client.execute_write_query(
                query,
                {"props": theme.to_graph_node()}
            )

    def _create_values(self, values: List[Value]) -> None:
        """Create Value nodes."""
        logger.info(f"Creating {len(values)} Value nodes...")

        for value in values:
            query = """
            CREATE (v:Value)
            SET v = $props
            """
            self.client.execute_write_query(
                query,
                {"props": value.to_graph_node()}
            )

    def _create_events(self, events: List[Event]) -> None:
        """Create Event nodes."""
        logger.info(f"Creating {len(events)} Event nodes...")

        for event in events:
            query = """
            CREATE (e:Event)
            SET e = $props
            """
            self.client.execute_write_query(
                query,
                {"props": event.to_graph_node()}
            )

    def _create_decisions(self, decisions: List[Decision]) -> None:
        """Create Decision nodes."""
        logger.info(f"Creating {len(decisions)} Decision nodes...")

        for decision in decisions:
            query = """
            CREATE (d:Decision)
            SET d = $props
            """
            self.client.execute_write_query(
                query,
                {"props": decision.to_graph_node()}
            )

    def _create_stories(self, stories: List[Story]) -> None:
        """Create Story nodes."""
        logger.info(f"Creating {len(stories)} Story nodes...")

        for story in stories:
            query = """
            CREATE (s:Story)
            SET s = $props
            """
            self.client.execute_write_query(
                query,
                {"props": story.to_graph_node()}
            )

    def _create_relationships(self, data: Dict[str, List]) -> None:
        """Create all relationships between nodes."""
        logger.info("Creating relationships...")

        stories = data.get("stories", [])
        people = data.get("people", [])
        groups = data.get("groups", [])
        events = data.get("events", [])

        # Create person-to-group relationships (BELONGS_TO)
        self._create_person_group_relationships(people, groups)

        # Create story relationships
        for story in stories:
            # Story -> Event (ABOUT)
            self._create_story_event_relationships(story, events)

            # Person -> Story (TELLS)
            self._create_person_story_relationships(story, people)

            # Story -> Person (INVOLVES)
            self._create_story_actor_relationships(story)

            # Story -> Theme (EXEMPLIFIES)
            self._create_story_theme_relationships(story)

            # Story -> Value (EXEMPLIFIES)
            self._create_story_value_relationships(story)

    def _create_person_group_relationships(
        self,
        people: List[Person],
        groups: List[Group]
    ) -> None:
        """Create BELONGS_TO relationships between people and groups."""
        logger.info("Creating Person -> Group relationships...")

        # Create department relationships
        for person in people:
            # Find the department group
            group_id = f"group_{person.department.lower().replace(' ', '_')}"

            query = """
            MATCH (p:Person {id: $person_id})
            MATCH (g:Group {id: $group_id})
            CREATE (p)-[:BELONGS_TO]->(g)
            """
            self.client.execute_write_query(
                query,
                {"person_id": person.id, "group_id": group_id}
            )

    def _create_story_event_relationships(
        self,
        story: Story,
        events: List[Event]
    ) -> None:
        """Create ABOUT relationships between stories and events."""
        # Find matching event by name
        for event in events:
            if event.name in story.context.trigger_events:
                query = """
                MATCH (s:Story {id: $story_id})
                MATCH (e:Event {id: $event_id})
                CREATE (s)-[:ABOUT]->(e)
                """
                self.client.execute_write_query(
                    query,
                    {"story_id": story.id, "event_id": event.id}
                )

    def _create_person_story_relationships(
        self,
        story: Story,
        people: List[Person]
    ) -> None:
        """Create TELLS relationships between people and stories."""
        # Each variation represents a telling
        for variation in story.variations:
            # Find the person by name
            teller = next((p for p in people if p.name == variation.teller_identity), None)

            if teller:
                query = """
                MATCH (p:Person {id: $person_id})
                MATCH (s:Story {id: $story_id})
                CREATE (p)-[:TELLS {
                    when: $when,
                    context: $context,
                    audience: $audience,
                    framing: $framing
                }]->(s)
                """
                self.client.execute_write_query(
                    query,
                    {
                        "person_id": teller.id,
                        "story_id": story.id,
                        "when": variation.telling_timestamp.isoformat(),
                        "context": story.context.why_told.value,
                        "audience": variation.audience,
                        "framing": variation.framing
                    }
                )

    def _create_story_actor_relationships(self, story: Story) -> None:
        """Create INVOLVES relationships between stories and actors."""
        # Protagonists
        for protagonist_name in story.actors.protagonists:
            query = """
            MATCH (s:Story {id: $story_id})
            MATCH (p:Person {name: $name})
            CREATE (s)-[:INVOLVES {role: 'protagonist'}]->(p)
            """
            self.client.execute_write_query(
                query,
                {"story_id": story.id, "name": protagonist_name}
            )

        # Decision makers
        for dm_name in story.actors.decision_makers:
            query = """
            MATCH (s:Story {id: $story_id})
            MATCH (p:Person {name: $name})
            MERGE (s)-[:INVOLVES {role: 'decision_maker'}]->(p)
            """
            self.client.execute_write_query(
                query,
                {"story_id": story.id, "name": dm_name}
            )

    def _create_story_theme_relationships(self, story: Story) -> None:
        """Create EXEMPLIFIES relationships between stories and themes."""
        for theme_name in story.themes.primary_themes:
            query = """
            MATCH (s:Story {id: $story_id})
            MATCH (t:Theme)
            WHERE toLower(t.name) = toLower($theme_name)
            CREATE (s)-[:EXEMPLIFIES]->(t)
            """
            try:
                self.client.execute_write_query(
                    query,
                    {"story_id": story.id, "theme_name": theme_name}
                )
            except Exception as e:
                logger.warning(f"Could not link story to theme '{theme_name}': {e}")

    def _create_story_value_relationships(self, story: Story) -> None:
        """Create EXEMPLIFIES relationships between stories and values."""
        for value_name in story.themes.values_expressed:
            query = """
            MATCH (s:Story {id: $story_id})
            MATCH (v:Value)
            WHERE toLower(v.name) = toLower($value_name)
            CREATE (s)-[:EXEMPLIFIES]->(v)
            """
            try:
                self.client.execute_write_query(
                    query,
                    {"story_id": story.id, "value_name": value_name}
                )
            except Exception as e:
                logger.warning(f"Could not link story to value '{value_name}': {e}")

    def create_causal_relationships(self, story: Story) -> None:
        """Create LED_TO relationships for causal chains."""
        if not story.structure.causal_chain:
            return

        # For each link in the causal chain, create relationships between events
        for link in story.structure.causal_chain:
            cause = link.get("cause", "")
            effect = link.get("effect", "")

            if cause and effect:
                # This would require Event nodes for each step
                # For now, we'll store this in the story structure
                pass

    def create_story_similarity_relationships(self) -> None:
        """Create ECHOES relationships between similar stories."""
        logger.info("Creating similarity relationships...")

        # Find stories with shared themes
        query = """
        MATCH (s1:Story)-[:EXEMPLIFIES]->(t:Theme)<-[:EXEMPLIFIES]-(s2:Story)
        WHERE s1.id < s2.id
        WITH s1, s2, count(t) as shared_themes
        WHERE shared_themes >= 2
        CREATE (s1)-[:ECHOES {shared_themes: shared_themes}]->(s2)
        """
        self.client.execute_write_query(query)

    def create_contradiction_relationships(self) -> None:
        """Create CONTRADICTS relationships between conflicting stories."""
        logger.info("Creating contradiction relationships...")

        # Find stories about the same event but with different outcomes or framings
        query = """
        MATCH (s1:Story)-[:ABOUT]->(e:Event)<-[:ABOUT]-(s2:Story)
        WHERE s1.id < s2.id
        AND s1.outcome <> s2.outcome
        CREATE (s1)-[:CONTRADICTS]->(s2)
        """
        try:
            self.client.execute_write_query(query)
        except Exception as e:
            logger.warning(f"Could not create contradiction relationships: {e}")
