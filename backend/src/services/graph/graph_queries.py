"""
Advanced query service for narrative knowledge graph.
Implements sophisticated patterns for exploring stories, perspectives, and relationships.
"""
from typing import List, Dict, Any, Optional
import logging

from ...db import neo4j_client

logger = logging.getLogger(__name__)


class NarrativeQueryService:
    """Service for querying the narrative knowledge graph."""

    def __init__(self):
        """Initialize the query service."""
        self.client = neo4j_client

    def search_stories(
        self,
        themes: Optional[List[str]] = None,
        groups: Optional[List[str]] = None,
        story_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for stories matching criteria.

        Args:
            themes: Filter by themes
            groups: Filter by group involvement
            story_type: Filter by story type
            limit: Maximum results

        Returns:
            List of matching stories with proper formatting
        """
        query_parts = ["MATCH (s:Story)"]
        where_clauses = []
        params = {"limit": limit}

        if story_type:
            where_clauses.append("s.type = $story_type")
            params["story_type"] = story_type

        # Get themes with the story
        if themes:
            query_parts.append("MATCH (s)-[:EXEMPLIFIES]->(t:Theme)")
            where_clauses.append("t.name IN $themes")
            params["themes"] = themes
        else:
            query_parts.append("OPTIONAL MATCH (s)-[:EXEMPLIFIES]->(t:Theme)")

        if groups:
            query_parts.append("""
                MATCH (s)<-[:TELLS]-(p:Person)-[:BELONGS_TO]->(g:Group)
            """)
            where_clauses.append("g.name IN $groups")
            params["groups"] = groups

        if where_clauses:
            query_parts.append("WHERE " + " AND ".join(where_clauses))

        query_parts.append("""
            WITH s, collect(DISTINCT t.name) as themes
            RETURN s, themes
            LIMIT $limit
        """)

        query = "\n".join(query_parts)
        results = self.client.execute_read_query(query, params)

        # Format stories with all required fields
        formatted_stories = []
        for r in results:
            story = r["s"]
            formatted_story = {
                "id": story.get("id", ""),
                "summary": story.get("summary", ""),
                "full_text": story.get("full_text", ""),
                "type": story.get("type", "learning"),
                "timestamp": story.get("timestamp", story.get("created_at", "2024-01-01T00:00:00Z")),
                "primary_themes": r.get("themes", []) or [],
                "secondary_themes": story.get("secondary_themes", []),
                "lessons": story.get("lessons", []),
                "outcome": story.get("outcome", ""),
                "department": story.get("department", ""),
                "group": story.get("group", ""),
                "protagonists": story.get("protagonists", []),
                "stakeholders": story.get("stakeholders", []),
                "values_represented": story.get("values_represented", []),
                "key_quotes": story.get("key_quotes", []),
                "source": story.get("source", "")
            }
            formatted_stories.append(formatted_story)

        return formatted_stories

    def get_group_perspective(
        self,
        group_name: str,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze how a group frames topics in their stories.

        Args:
            group_name: Name of the group
            topic: Optional topic filter

        Returns:
            Group perspective analysis
        """
        # Get stories told by this group
        query = """
        MATCH (g:Group {name: $group_name})<-[:BELONGS_TO]-(p:Person)-[:TELLS]->(s:Story)
        WITH s, collect(DISTINCT p.name) as tellers

        // Get themes
        OPTIONAL MATCH (s)-[:EXEMPLIFIES]->(t:Theme)
        WITH s, tellers, collect(DISTINCT t.name) as themes

        // Get values
        OPTIONAL MATCH (s)-[:EXEMPLIFIES]->(v:Value)
        WITH s, tellers, themes, collect(DISTINCT v.name) as values

        RETURN s, tellers, themes, values
        LIMIT 50
        """

        results = self.client.execute_read_query(query, {"group_name": group_name})

        # Aggregate perspective
        all_themes = []
        all_values = []
        stories = []

        for r in results:
            if r.get("themes"):
                all_themes.extend(r["themes"])
            if r.get("values"):
                all_values.extend(r["values"])
            stories.append({
                "id": r["s"]["id"],
                "summary": r["s"].get("summary", ""),
                "type": r["s"].get("type", "")
            })

        # Count theme frequency
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        # Count value frequency
        value_counts = {}
        for value in all_values:
            value_counts[value] = value_counts.get(value, 0) + 1

        return {
            "group": group_name,
            "story_count": len(stories),
            "common_themes": sorted(theme_counts.items(), key=lambda x: x[1], reverse=True),
            "emphasized_values": sorted(value_counts.items(), key=lambda x: x[1], reverse=True),
            "example_stories": stories[:5]
        }

    def compare_perspectives(self, event_name: str) -> Dict[str, Any]:
        """
        Compare how different groups tell stories about the same event.

        Args:
            event_name: Event to compare

        Returns:
            Perspective comparison
        """
        query = """
        MATCH (e:Event {name: $event_name})
        MATCH (s:Story)-[:ABOUT]->(e)
        MATCH (p:Person)-[:TELLS {framing: framing}]->(s)
        MATCH (p)-[:BELONGS_TO]->(g:Group)

        RETURN g.name as group,
               s.id as story_id,
               s.summary as summary,
               framing,
               p.name as teller
        """

        results = self.client.execute_read_query(query, {"event_name": event_name})

        # Group by department
        by_group = {}
        for r in results:
            group = r["group"]
            if group not in by_group:
                by_group[group] = []

            by_group[group].append({
                "story_id": r["story_id"],
                "summary": r["summary"],
                "framing": r.get("framing", ""),
                "teller": r["teller"]
            })

        return {
            "event": event_name,
            "perspectives": by_group,
            "group_count": len(by_group)
        }

    def find_precedents(
        self,
        themes: List[str],
        story_type: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar past situations based on themes.

        Args:
            themes: Themes to match
            story_type: Optional story type filter
            limit: Number of results

        Returns:
            Relevant precedent stories
        """
        query = """
        MATCH (s:Story)-[:EXEMPLIFIES]->(t:Theme)
        WHERE t.name IN $themes
        WITH s, count(t) as theme_matches
        WHERE theme_matches >= 1
        """

        if story_type:
            query += "\nAND s.type = $story_type"

        query += """

        // Get outcome
        OPTIONAL MATCH (s)-[:RESULTED_IN]->(o:Outcome)

        RETURN s, theme_matches, o.description as outcome
        ORDER BY theme_matches DESC
        LIMIT $limit
        """

        params = {"themes": themes, "limit": limit}
        if story_type:
            params["story_type"] = story_type

        results = self.client.execute_read_query(query, params)

        precedents = []
        for r in results:
            precedents.append({
                "story_id": r["s"]["id"],
                "summary": r["s"].get("summary", ""),
                "type": r["s"].get("type", ""),
                "theme_matches": r["theme_matches"],
                "outcome": r.get("outcome", r["s"].get("outcome", "")),
                "lessons": r["s"].get("lessons", [])
            })

        return precedents

    def trace_causality(self, story_id: str) -> Dict[str, Any]:
        """
        Show causal relationships in a story.

        Args:
            story_id: Story to analyze

        Returns:
            Causal chain information
        """
        query = """
        MATCH (s:Story {id: $story_id})

        // Get events in sequence
        OPTIONAL MATCH path = (e1:Event)-[:LED_TO*]->(e2:Event)
        WHERE (s)-[:ABOUT]->(e1)

        RETURN s,
               [event IN nodes(path) | event.description] as causal_chain
        """

        results = self.client.execute_read_query(query, {"story_id": story_id})

        if not results:
            return {"error": "Story not found"}

        story = results[0]["s"]
        causal_chain = results[0].get("causal_chain", [])

        return {
            "story_id": story_id,
            "summary": story.get("summary", ""),
            "causal_chain": causal_chain,
            "lessons": story.get("lessons", [])
        }

    def get_group_stories_by_topic(
        self,
        group_name: str,
        topic_keywords: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Q1: What stories do engineers tell about product decisions?

        Generalized to: What stories does {group} tell about {topic}?
        """
        query = """
        MATCH (g:Group {name: $group_name})<-[:BELONGS_TO]-(p:Person)-[:TELLS]->(s:Story)

        // Filter by topic (themes or keywords in summary)
        MATCH (s)-[:EXEMPLIFIES]->(t:Theme)
        WHERE any(keyword IN $keywords WHERE toLower(t.name) CONTAINS toLower(keyword)
           OR toLower(s.summary) CONTAINS toLower(keyword))

        WITH DISTINCT s, collect(DISTINCT p.name) as tellers, collect(DISTINCT t.name) as themes

        RETURN s.id as story_id,
               s.summary as summary,
               s.type as type,
               tellers,
               themes
        LIMIT 20
        """

        results = self.client.execute_read_query(
            query,
            {"group_name": group_name, "keywords": topic_keywords}
        )

        return [dict(r) for r in results]

    def compare_event_narratives(self, event_name: str) -> Dict[str, Any]:
        """
        Q2: How is "the big migration" told differently by groups?

        Shows different framings of the same event.
        """
        return self.compare_perspectives(event_name)

    def get_group_value_emphasis(self, group_name: str) -> List[Dict[str, Any]]:
        """
        Q3: What values does the exec team emphasize in their stories?
        """
        query = """
        MATCH (g:Group {name: $group_name})<-[:BELONGS_TO]-(p:Person)-[:TELLS]->(s:Story)
        MATCH (s)-[:EXEMPLIFIES]->(v:Value)

        WITH v.name as value, count(s) as frequency

        RETURN value, frequency
        ORDER BY frequency DESC
        """

        results = self.client.execute_read_query(query, {"group_name": group_name})
        return [dict(r) for r in results]

    def find_similar_patterns(
        self,
        current_story_id: str,
        min_shared_themes: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Q4: Find stories with similar patterns to a current situation.
        """
        query = """
        MATCH (current:Story {id: $story_id})-[:EXEMPLIFIES]->(t:Theme)
        WITH current, collect(t.name) as current_themes

        MATCH (similar:Story)-[:EXEMPLIFIES]->(t2:Theme)
        WHERE similar.id <> current.id AND t2.name IN current_themes

        WITH similar, current_themes, collect(t2.name) as similar_themes
        WITH similar,
             current_themes,
             similar_themes,
             size([theme IN current_themes WHERE theme IN similar_themes]) as shared_count
        WHERE shared_count >= $min_shared

        // Get outcome
        RETURN similar.id as story_id,
               similar.summary as summary,
               similar.type as type,
               similar.outcome as outcome,
               similar_themes as themes,
               shared_count
        ORDER BY shared_count DESC
        LIMIT 10
        """

        results = self.client.execute_read_query(
            query,
            {"story_id": current_story_id, "min_shared": min_shared_themes}
        )

        return [dict(r) for r in results]

    def get_cautionary_tales(self, themes: List[str]) -> List[Dict[str, Any]]:
        """
        Q5: What cautionary tales exist about moving too fast?
        """
        query = """
        MATCH (s:Story {type: 'failure'})-[:EXEMPLIFIES]->(t:Theme)
        WHERE t.name IN $themes

        WITH s, collect(t.name) as themes

        RETURN s.id as story_id,
               s.summary as summary,
               s.lessons as lessons,
               themes
        ORDER BY s.timestamp DESC
        LIMIT 10
        """

        results = self.client.execute_read_query(query, {"themes": themes})
        return [dict(r) for r in results]

    def show_causal_chains_by_theme(self, theme_name: str) -> List[Dict[str, Any]]:
        """
        Q6: Show causal chains in scaling stories.
        """
        query = """
        MATCH (s:Story)-[:EXEMPLIFIES]->(t:Theme {name: $theme})

        // Get events related to this story
        OPTIONAL MATCH path = (s)-[:ABOUT]->(e1:Event)-[:LED_TO*]->(e2:Event)

        RETURN s.id as story_id,
               s.summary as summary,
               [node IN nodes(path) | node.description] as causal_chain
        LIMIT 10
        """

        results = self.client.execute_read_query(query, {"theme": theme_name})
        return [dict(r) for r in results]

    def get_narrative_index(
        self,
        dimension: str = "theme"
    ) -> List[Dict[str, Any]]:
        """
        Get index of narratives by dimension (theme, group, time, etc.).

        Args:
            dimension: One of 'theme', 'group', 'type', 'value'

        Returns:
            Index with counts
        """
        if dimension == "theme":
            query = """
            MATCH (t:Theme)<-[:EXEMPLIFIES]-(s:Story)
            WITH t.name as theme, count(s) as story_count
            RETURN theme, story_count
            ORDER BY story_count DESC
            """
        elif dimension == "group":
            query = """
            MATCH (g:Group)<-[:BELONGS_TO]-(p:Person)-[:TELLS]->(s:Story)
            WITH g.name as group, count(DISTINCT s) as story_count
            RETURN group, story_count
            ORDER BY story_count DESC
            """
        elif dimension == "type":
            query = """
            MATCH (s:Story)
            WITH s.type as type, count(s) as story_count
            RETURN type, story_count
            ORDER BY story_count DESC
            """
        elif dimension == "value":
            query = """
            MATCH (v:Value)<-[:EXEMPLIFIES]-(s:Story)
            WITH v.name as value, count(s) as story_count
            RETURN value, story_count
            ORDER BY story_count DESC
            """
        else:
            return []

        results = self.client.execute_read_query(query)
        return [dict(r) for r in results]

    def get_graph_data_for_visualization(
        self,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get graph data suitable for D3.js force-directed visualization.

        Returns:
            Dictionary with nodes and links arrays
        """
        try:
            # Get nodes of different types
            nodes_query = """
            MATCH (n)
            WHERE n:Story OR n:Person OR n:Group OR n:Theme OR n:Event
            RETURN
                labels(n)[0] as type,
                n.id as id,
                n.name as name,
                n.summary as summary
            LIMIT $limit
            """

            nodes_results = self.client.execute_read_query(nodes_query, {"limit": limit})

            # If no nodes found, return empty structure
            if not nodes_results:
                logger.warning("No nodes found in database for visualization")
                return {"nodes": [], "links": []}

            # Get relationships
            links_query = """
            MATCH (source)-[r]->(target)
            WHERE (source:Story OR source:Person OR source:Group OR source:Theme)
            AND (target:Story OR target:Person OR target:Theme OR target:Event OR target:Group)
            RETURN
                source.id as source,
                target.id as target,
                type(r) as type
            LIMIT $limit
            """

            links_results = self.client.execute_read_query(links_query, {"limit": limit * 2})

            # Format for D3.js
            nodes = []
            node_ids = set()

            for node in nodes_results:
                node_id = node.get("id")
                if not node_id:
                    continue

                node_ids.add(node_id)

                # Create label from name or summary
                label = node.get("name")
                if not label and node.get("summary"):
                    label = node["summary"][:50]
                    if len(node["summary"]) > 50:
                        label += "..."
                if not label:
                    label = node_id

                nodes.append({
                    "id": node_id,
                    "type": node.get("type", "Unknown"),
                    "label": label,
                })

            # Only include links where both source and target nodes exist
            links = []
            for link in links_results:
                source_id = link.get("source")
                target_id = link.get("target")

                if source_id and target_id and source_id in node_ids and target_id in node_ids:
                    links.append({
                        "source": source_id,
                        "target": target_id,
                        "type": link.get("type", "RELATED_TO")
                    })

            logger.info(f"Returning {len(nodes)} nodes and {len(links)} links for visualization")

            return {
                "nodes": nodes,
                "links": links
            }

        except Exception as e:
            logger.error(f"Error getting graph data for visualization: {e}")
            return {"nodes": [], "links": []}
