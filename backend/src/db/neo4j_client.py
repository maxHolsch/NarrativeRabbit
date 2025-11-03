"""
Neo4j database client with connection management and query execution.
"""
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Driver, Session, Result
from neo4j.exceptions import ServiceUnavailable, AuthError
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j database client for managing connections and executing queries."""

    def __init__(self):
        """Initialize the Neo4j client."""
        self._driver: Optional[Driver] = None
        self._uri = settings.neo4j_uri
        self._user = settings.neo4j_user
        self._password = settings.neo4j_password

    def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                connection_acquisition_timeout=120
            )
            # Verify connectivity
            self._driver.verify_connectivity()
            logger.info(f"Successfully connected to Neo4j at {self._uri}")
        except AuthError as e:
            logger.error(f"Authentication failed: {e}")
            raise
        except ServiceUnavailable as e:
            logger.error(f"Neo4j service unavailable: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self) -> None:
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            logger.info("Neo4j connection closed")

    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results.

        Args:
            query: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records as dictionaries
        """
        if not self._driver:
            raise RuntimeError("Database not connected. Call connect() first.")

        with self._driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def execute_write_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a write query within a transaction.

        Args:
            query: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records as dictionaries
        """
        if not self._driver:
            raise RuntimeError("Database not connected. Call connect() first.")

        def _execute_transaction(tx):
            result = tx.run(query, parameters or {})
            return [record.data() for record in result]

        with self._driver.session() as session:
            return session.execute_write(_execute_transaction)

    def execute_read_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a read query within a transaction.

        Args:
            query: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records as dictionaries
        """
        if not self._driver:
            raise RuntimeError("Database not connected. Call connect() first.")

        def _execute_transaction(tx):
            result = tx.run(query, parameters or {})
            return [record.data() for record in result]

        with self._driver.session() as session:
            return session.execute_read(_execute_transaction)

    def batch_execute(
        self,
        queries: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """
        Execute multiple queries in a single transaction.

        Args:
            queries: List of dictionaries with 'query' and 'parameters' keys

        Returns:
            List of results for each query
        """
        if not self._driver:
            raise RuntimeError("Database not connected. Call connect() first.")

        def _execute_batch(tx):
            results = []
            for query_dict in queries:
                query = query_dict.get('query', '')
                parameters = query_dict.get('parameters', {})
                result = tx.run(query, parameters)
                results.append([record.data() for record in result])
            return results

        with self._driver.session() as session:
            return session.execute_write(_execute_batch)

    def clear_database(self) -> None:
        """Clear all nodes and relationships from the database. USE WITH CAUTION!"""
        logger.warning("Clearing entire database...")
        query = "MATCH (n) DETACH DELETE n"
        self.execute_write_query(query)
        logger.info("Database cleared")

    def create_indexes(self) -> None:
        """Create indexes for improved query performance."""
        indexes = [
            "CREATE INDEX story_id IF NOT EXISTS FOR (s:Story) ON (s.id)",
            "CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)",
            "CREATE INDEX group_name IF NOT EXISTS FOR (g:Group) ON (g.name)",
            "CREATE INDEX theme_name IF NOT EXISTS FOR (t:Theme) ON (t.name)",
            "CREATE INDEX event_name IF NOT EXISTS FOR (e:Event) ON (e.name)",
            "CREATE INDEX story_timestamp IF NOT EXISTS FOR (s:Story) ON (s.timestamp)",
            "CREATE INDEX story_type IF NOT EXISTS FOR (s:Story) ON (s.type)",
        ]

        for index_query in indexes:
            try:
                self.execute_write_query(index_query)
                logger.info(f"Created index: {index_query}")
            except Exception as e:
                logger.warning(f"Index creation skipped or failed: {e}")

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats_query = """
        MATCH (n)
        WITH labels(n) AS labels
        UNWIND labels AS label
        RETURN label, count(*) AS count
        ORDER BY count DESC
        """
        results = self.execute_read_query(stats_query)

        relationship_query = """
        MATCH ()-[r]->()
        RETURN type(r) AS relationship_type, count(r) AS count
        ORDER BY count DESC
        """
        rel_results = self.execute_read_query(relationship_query)

        return {
            "nodes": results,
            "relationships": rel_results
        }


# Global client instance
neo4j_client = Neo4jClient()
