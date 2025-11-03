"""
AI Narrative Queries - Cypher Query Service

Provides reusable Cypher queries for AI narrative intelligence analysis.
Supports all sub-agents and main orchestrator with efficient graph queries.
"""

from typing import Dict, List, Any, Optional


class AIQueries:
    """
    Service providing Cypher queries for AI narrative analysis.

    All queries are optimized with:
    - Proper LIMIT clauses for performance
    - Parameter binding for security
    - Index usage where applicable
    - Efficient relationship traversal
    """

    def __init__(self, neo4j_client):
        """
        Initialize AI Queries service.

        Args:
            neo4j_client: Neo4j database client for executing queries
        """
        self.neo4j = neo4j_client

    # ==================== AI INITIATIVE QUERIES ====================

    def get_all_ai_initiatives(self) -> List[Dict]:
        """Fetch all AI initiatives with their basic properties."""
        query = """
        MATCH (i:AIInitiative)
        RETURN i
        ORDER BY i.created_at DESC
        LIMIT 100
        """
        results = self.neo4j.execute_read_query(query)
        return [record['i'] for record in results]

    def get_initiative_by_id(self, initiative_id: str) -> Optional[Dict]:
        """Fetch a specific AI initiative by ID."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})
        RETURN i
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return results[0]['i'] if results else None

    def get_initiative_official_stories(self, initiative_id: str) -> List[Dict]:
        """Fetch official stories for an initiative."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_OFFICIAL_STORY]->(s:Story)
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT 50
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return [record['s'] for record in results]

    def get_initiative_actual_stories(self, initiative_id: str) -> List[Dict]:
        """Fetch actual (employee) stories about an initiative."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT 500
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return [record['s'] for record in results]

    def get_initiative_stories_by_group(self, initiative_id: str) -> Dict[str, List[Dict]]:
        """Fetch stories grouped by teller group for an initiative."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
        RETURN s.teller_group as group, collect(s) as stories
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})

        grouped = {}
        for record in results:
            group = record['group'] or 'unknown'
            grouped[group] = record['stories']

        return grouped

    # ==================== AI STORY QUERIES ====================

    def get_all_ai_stories(self, limit: int = 1000) -> List[Dict]:
        """Fetch all AI-related stories."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [record['s'] for record in results]

    def get_ai_stories_by_group(self, group: str, limit: int = 200) -> List[Dict]:
        """Fetch AI stories from a specific group."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true AND s.teller_group = $group
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'group': group, 'limit': limit})
        return [record['s'] for record in results]

    def get_ai_stories_by_sentiment(self, min_sentiment: float = 0.5, limit: int = 200) -> List[Dict]:
        """Fetch AI stories with sentiment above threshold."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true AND s.ai_sentiment >= $min_sentiment
        RETURN s
        ORDER BY s.ai_sentiment DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'min_sentiment': min_sentiment, 'limit': limit})
        return [record['s'] for record in results]

    def get_ai_stories_by_frame(self, agency_frame: str, limit: int = 200) -> List[Dict]:
        """Fetch AI stories using a specific agency frame."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true AND s.agency_frame = $agency_frame
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'agency_frame': agency_frame, 'limit': limit})
        return [record['s'] for record in results]

    def get_ai_stories_by_sophistication(self, sophistication: str, limit: int = 200) -> List[Dict]:
        """Fetch AI stories at a specific sophistication level."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true AND s.ai_sophistication = $sophistication
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'sophistication': sophistication, 'limit': limit})
        return [record['s'] for record in results]

    # ==================== NARRATIVE FRAME QUERIES ====================

    def get_all_narrative_frames(self) -> List[Dict]:
        """Fetch all narrative frames."""
        query = """
        MATCH (f:NarrativeFrame)
        RETURN f
        ORDER BY f.created_at DESC
        LIMIT 100
        """
        results = self.neo4j.execute_read_query(query)
        return [record['f'] for record in results]

    def get_stories_using_frame(self, frame_id: str, limit: int = 200) -> List[Dict]:
        """Fetch stories using a specific narrative frame."""
        query = """
        MATCH (s:Story)-[:USES_FRAME]->(f:NarrativeFrame {id: $frame_id})
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'frame_id': frame_id, 'limit': limit})
        return [record['s'] for record in results]

    def get_competing_frames(self, initiative_id: str) -> List[Dict]:
        """Fetch frames that compete for an initiative."""
        query = """
        MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)-[:USES_FRAME]->(f:NarrativeFrame)
        WITH f, count(s) as story_count
        RETURN f, story_count
        ORDER BY story_count DESC
        LIMIT 10
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return [{'frame': record['f'], 'story_count': record['story_count']} for record in results]

    def get_frame_competition_relationships(self, initiative_id: str) -> List[Dict]:
        """Fetch FrameCompetition relationships for an initiative."""
        query = """
        MATCH (fc:FrameCompetition)-[:COMPETES_IN]->(i:AIInitiative {id: $initiative_id})
        MATCH (fc)-[:COMPETES_WITH]->(f1:NarrativeFrame)
        MATCH (fc)-[:COMPETES_WITH]->(f2:NarrativeFrame)
        WHERE f1 <> f2
        RETURN fc, f1, f2
        LIMIT 50
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return results

    # ==================== CULTURAL SIGNAL QUERIES ====================

    def get_all_cultural_signals(self, limit: int = 200) -> List[Dict]:
        """Fetch all detected cultural signals."""
        query = """
        MATCH (c:CulturalSignal)
        RETURN c
        ORDER BY c.detected_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [record['c'] for record in results]

    def get_cultural_signals_by_type(self, signal_type: str, limit: int = 100) -> List[Dict]:
        """Fetch cultural signals of a specific type."""
        query = """
        MATCH (c:CulturalSignal {type: $signal_type})
        RETURN c
        ORDER BY c.strength DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'signal_type': signal_type, 'limit': limit})
        return [record['c'] for record in results]

    def get_stories_revealing_signal(self, signal_id: str, limit: int = 100) -> List[Dict]:
        """Fetch stories that reveal a specific cultural signal."""
        query = """
        MATCH (s:Story)-[:REVEALS]->(c:CulturalSignal {id: $signal_id})
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'signal_id': signal_id, 'limit': limit})
        return [record['s'] for record in results]

    # ==================== RESISTANCE PATTERN QUERIES ====================

    def get_all_resistance_patterns(self, limit: int = 200) -> List[Dict]:
        """Fetch all detected resistance patterns."""
        query = """
        MATCH (r:ResistancePattern)
        RETURN r
        ORDER BY r.severity DESC, r.detected_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [record['r'] for record in results]

    def get_resistance_patterns_by_group(self, group: str, limit: int = 50) -> List[Dict]:
        """Fetch resistance patterns for a specific group."""
        query = """
        MATCH (r:ResistancePattern {affected_group: $group})
        RETURN r
        ORDER BY r.severity DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'group': group, 'limit': limit})
        return [record['r'] for record in results]

    def get_stories_indicating_resistance(self, pattern_id: str, limit: int = 100) -> List[Dict]:
        """Fetch stories that indicate a resistance pattern."""
        query = """
        MATCH (s:Story)-[:INDICATES]->(r:ResistancePattern {id: $pattern_id})
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'pattern_id': pattern_id, 'limit': limit})
        return [record['s'] for record in results]

    def get_resistance_spread_network(self, pattern_id: str) -> List[Dict]:
        """Fetch narrative contagion network for resistance spread."""
        query = """
        MATCH (r:ResistancePattern {id: $pattern_id})<-[:INDICATES]-(s1:Story)
        MATCH (s1)-[:REFERENCES|RESPONDS_TO]->(s2:Story)
        MATCH (s2)-[:INDICATES]->(r2:ResistancePattern)
        RETURN s1, s2, r2
        LIMIT 100
        """
        results = self.neo4j.execute_read_query(query, {'pattern_id': pattern_id})
        return results

    # ==================== ADOPTION BARRIER QUERIES ====================

    def get_all_adoption_barriers(self, limit: int = 100) -> List[Dict]:
        """Fetch all identified adoption barriers."""
        query = """
        MATCH (b:AdoptionBarrier)
        RETURN b
        ORDER BY b.severity DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [record['b'] for record in results]

    def get_barriers_by_type(self, barrier_type: str, limit: int = 50) -> List[Dict]:
        """Fetch adoption barriers of a specific type."""
        query = """
        MATCH (b:AdoptionBarrier {type: $barrier_type})
        RETURN b
        ORDER BY b.severity DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'barrier_type': barrier_type, 'limit': limit})
        return [record['b'] for record in results]

    def get_groups_encountering_barrier(self, barrier_id: str) -> List[str]:
        """Fetch groups encountering a specific barrier."""
        query = """
        MATCH (g:Group)-[:ENCOUNTERS]->(b:AdoptionBarrier {id: $barrier_id})
        RETURN g.name as group_name
        """
        results = self.neo4j.execute_read_query(query, {'barrier_id': barrier_id})
        return [record['group_name'] for record in results]

    # ==================== NARRATIVE GAP QUERIES ====================

    def get_all_narrative_gaps(self, limit: int = 100) -> List[Dict]:
        """Fetch all detected narrative gaps."""
        query = """
        MATCH (g:NarrativeGap)
        RETURN g
        ORDER BY g.severity DESC, g.detected_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [record['g'] for record in results]

    def get_gaps_for_initiative(self, initiative_id: str) -> List[Dict]:
        """Fetch narrative gaps for a specific initiative."""
        query = """
        MATCH (g:NarrativeGap)-[:IDENTIFIED_IN]->(i:AIInitiative {id: $initiative_id})
        RETURN g
        ORDER BY g.severity DESC
        LIMIT 50
        """
        results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        return [record['g'] for record in results]

    # ==================== AI CONCEPT QUERIES ====================

    def get_all_ai_concepts(self, limit: int = 200) -> List[Dict]:
        """Fetch all AI concepts mentioned in stories."""
        query = """
        MATCH (c:AIConcept)
        RETURN c
        ORDER BY c.mention_count DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [record['c'] for record in results]

    def get_stories_mentioning_concept(self, concept_id: str, limit: int = 200) -> List[Dict]:
        """Fetch stories mentioning a specific AI concept."""
        query = """
        MATCH (s:Story)-[:MENTIONS_CONCEPT]->(c:AIConcept {id: $concept_id})
        RETURN s
        ORDER BY s.created_at DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'concept_id': concept_id, 'limit': limit})
        return [record['s'] for record in results]

    def get_concept_co_occurrence(self, concept_id: str, limit: int = 50) -> List[Dict]:
        """Fetch concepts that co-occur with a given concept."""
        query = """
        MATCH (s:Story)-[:MENTIONS_CONCEPT]->(c1:AIConcept {id: $concept_id})
        MATCH (s)-[:MENTIONS_CONCEPT]->(c2:AIConcept)
        WHERE c1 <> c2
        WITH c2, count(s) as co_occurrence_count
        RETURN c2, co_occurrence_count
        ORDER BY co_occurrence_count DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'concept_id': concept_id, 'limit': limit})
        return [{'concept': record['c2'], 'count': record['co_occurrence_count']} for record in results]

    # ==================== ANALYSIS AGGREGATION QUERIES ====================

    def get_group_sentiment_summary(self, initiative_id: Optional[str] = None) -> List[Dict]:
        """Get sentiment summary by group."""
        if initiative_id:
            query = """
            MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
            WHERE s.ai_sentiment IS NOT NULL
            RETURN s.teller_group as group,
                   avg(s.ai_sentiment) as avg_sentiment,
                   min(s.ai_sentiment) as min_sentiment,
                   max(s.ai_sentiment) as max_sentiment,
                   count(s) as story_count
            ORDER BY avg_sentiment DESC
            """
            results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        else:
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true AND s.ai_sentiment IS NOT NULL
            RETURN s.teller_group as group,
                   avg(s.ai_sentiment) as avg_sentiment,
                   min(s.ai_sentiment) as min_sentiment,
                   max(s.ai_sentiment) as max_sentiment,
                   count(s) as story_count
            ORDER BY avg_sentiment DESC
            """
            results = self.neo4j.execute_read_query(query)

        return results

    def get_frame_distribution(self, initiative_id: Optional[str] = None) -> List[Dict]:
        """Get distribution of agency frames."""
        if initiative_id:
            query = """
            MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
            WHERE s.agency_frame IS NOT NULL
            RETURN s.agency_frame as frame,
                   count(s) as count,
                   collect(DISTINCT s.teller_group) as groups
            ORDER BY count DESC
            """
            results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        else:
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true AND s.agency_frame IS NOT NULL
            RETURN s.agency_frame as frame,
                   count(s) as count,
                   collect(DISTINCT s.teller_group) as groups
            ORDER BY count DESC
            """
            results = self.neo4j.execute_read_query(query)

        return results

    def get_sophistication_distribution(self, initiative_id: Optional[str] = None) -> List[Dict]:
        """Get distribution of AI sophistication levels."""
        if initiative_id:
            query = """
            MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
            WHERE s.ai_sophistication IS NOT NULL
            RETURN s.ai_sophistication as sophistication,
                   count(s) as count,
                   collect(DISTINCT s.teller_group) as groups
            ORDER BY count DESC
            """
            results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        else:
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true AND s.ai_sophistication IS NOT NULL
            RETURN s.ai_sophistication as sophistication,
                   count(s) as count,
                   collect(DISTINCT s.teller_group) as groups
            ORDER BY count DESC
            """
            results = self.neo4j.execute_read_query(query)

        return results

    def get_innovation_signal_distribution(self) -> List[Dict]:
        """Get distribution of innovation signals."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true AND s.innovation_signal IS NOT NULL
        RETURN s.innovation_signal as signal,
               count(s) as count,
               collect(DISTINCT s.teller_group) as groups
        ORDER BY count DESC
        """
        results = self.neo4j.execute_read_query(query)
        return results

    def get_time_frame_distribution(self) -> List[Dict]:
        """Get distribution of time frames in stories."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true AND s.time_frame IS NOT NULL
        RETURN s.time_frame as time_frame,
               count(s) as count,
               avg(s.ai_sentiment) as avg_sentiment
        ORDER BY count DESC
        """
        results = self.neo4j.execute_read_query(query)
        return results

    # ==================== RELATIONSHIP QUERIES ====================

    def get_story_references(self, story_id: str) -> Dict[str, List[Dict]]:
        """Get stories that reference or are referenced by a story."""
        # Outgoing references
        outgoing_query = """
        MATCH (s1:Story {id: $story_id})-[:REFERENCES]->(s2:Story)
        RETURN s2
        LIMIT 50
        """
        outgoing = self.neo4j.execute_read_query(outgoing_query, {'story_id': story_id})

        # Incoming references
        incoming_query = """
        MATCH (s1:Story)-[:REFERENCES]->(s2:Story {id: $story_id})
        RETURN s1
        LIMIT 50
        """
        incoming = self.neo4j.execute_read_query(incoming_query, {'story_id': story_id})

        return {
            'references_to': [record['s2'] for record in outgoing],
            'referenced_by': [record['s1'] for record in incoming]
        }

    def get_cross_group_references(self, group1: str, group2: str) -> List[Dict]:
        """Get stories where one group references another group's stories."""
        query = """
        MATCH (s1:Story {teller_group: $group1})-[:REFERENCES]->(s2:Story {teller_group: $group2})
        RETURN s1, s2
        LIMIT 100
        """
        results = self.neo4j.execute_read_query(query, {'group1': group1, 'group2': group2})
        return results

    def get_narrative_contagion_paths(self, source_story_id: str, max_depth: int = 3) -> List[Dict]:
        """Find narrative contagion paths from a source story."""
        query = """
        MATCH path = (s1:Story {id: $source_story_id})-[:REFERENCES*1..$max_depth]->(s2:Story)
        RETURN path
        LIMIT 50
        """
        results = self.neo4j.execute_read_query(query, {
            'source_story_id': source_story_id,
            'max_depth': max_depth
        })
        return results

    # ==================== ANALYTICS QUERIES ====================

    def get_ai_adoption_timeline(self, initiative_id: Optional[str] = None) -> List[Dict]:
        """Get timeline of AI-related story creation."""
        if initiative_id:
            query = """
            MATCH (i:AIInitiative {id: $initiative_id})-[:HAS_ACTUAL_STORIES]->(s:Story)
            WHERE s.created_at IS NOT NULL
            WITH date(s.created_at) as story_date,
                 count(s) as story_count,
                 avg(s.ai_sentiment) as avg_sentiment
            RETURN story_date, story_count, avg_sentiment
            ORDER BY story_date ASC
            LIMIT 365
            """
            results = self.neo4j.execute_read_query(query, {'initiative_id': initiative_id})
        else:
            query = """
            MATCH (s:Story)
            WHERE s.ai_related = true AND s.created_at IS NOT NULL
            WITH date(s.created_at) as story_date,
                 count(s) as story_count,
                 avg(s.ai_sentiment) as avg_sentiment
            RETURN story_date, story_count, avg_sentiment
            ORDER BY story_date ASC
            LIMIT 365
            """
            results = self.neo4j.execute_read_query(query)

        return results

    def get_most_influential_stories(self, limit: int = 20) -> List[Dict]:
        """Find most influential AI stories based on reference count."""
        query = """
        MATCH (s:Story)
        WHERE s.ai_related = true
        OPTIONAL MATCH (s)<-[:REFERENCES]-(other:Story)
        WITH s, count(other) as reference_count
        RETURN s, reference_count
        ORDER BY reference_count DESC
        LIMIT $limit
        """
        results = self.neo4j.execute_read_query(query, {'limit': limit})
        return [{'story': record['s'], 'influence_score': record['reference_count']} for record in results]

    def get_group_connectivity(self) -> List[Dict]:
        """Measure connectivity between groups through story references."""
        query = """
        MATCH (s1:Story)-[:REFERENCES]->(s2:Story)
        WHERE s1.teller_group <> s2.teller_group
        WITH s1.teller_group as from_group,
             s2.teller_group as to_group,
             count(*) as connection_count
        RETURN from_group, to_group, connection_count
        ORDER BY connection_count DESC
        LIMIT 100
        """
        results = self.neo4j.execute_read_query(query)
        return results

    # ==================== UTILITY METHODS ====================

    def create_ai_initiative(self, initiative_data: Dict) -> Dict:
        """Create a new AI initiative node."""
        query = """
        CREATE (i:AIInitiative {
            id: $id,
            name: $name,
            type: $type,
            official_description: $official_description,
            stated_goals: $stated_goals,
            status: $status,
            created_at: datetime()
        })
        RETURN i
        """
        results = self.neo4j.execute_write_query(query, initiative_data)
        return results[0]['i'] if results else None

    def link_story_to_initiative(self, story_id: str, initiative_id: str, is_official: bool = False) -> bool:
        """Link a story to an initiative."""
        rel_type = 'HAS_OFFICIAL_STORY' if is_official else 'HAS_ACTUAL_STORIES'

        query = f"""
        MATCH (s:Story {{id: $story_id}})
        MATCH (i:AIInitiative {{id: $initiative_id}})
        MERGE (i)-[r:{rel_type}]->(s)
        RETURN r
        """
        results = self.neo4j.execute_write_query(query, {
            'story_id': story_id,
            'initiative_id': initiative_id
        })
        return len(results) > 0

    def update_story_ai_analysis(self, story_id: str, analysis_data: Dict) -> bool:
        """Update AI analysis properties on a story."""
        query = """
        MATCH (s:Story {id: $story_id})
        SET s.ai_related = $ai_related,
            s.ai_sentiment = $ai_sentiment,
            s.ai_sophistication = $ai_sophistication,
            s.innovation_signal = $innovation_signal,
            s.agency_frame = $agency_frame,
            s.time_frame = $time_frame,
            s.ai_concepts_mentioned = $ai_concepts_mentioned,
            s.updated_at = datetime()
        RETURN s
        """
        params = {'story_id': story_id}
        params.update(analysis_data)

        results = self.neo4j.execute_write_query(query, params)
        return len(results) > 0
