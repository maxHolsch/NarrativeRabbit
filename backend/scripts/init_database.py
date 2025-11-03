"""
Script to initialize the database with sample narrative data.
"""
import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import neo4j_client
from src.services.data_generator import NarrativeDataGenerator
from src.services.graph.graph_populator import GraphPopulator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Initialize the database with sample data."""
    logger.info("=" * 80)
    logger.info("Narrative Knowledge Graph - Database Initialization")
    logger.info("=" * 80)

    # Connect to Neo4j
    logger.info(f"Connecting to Neo4j at {settings.neo4j_uri}...")
    try:
        neo4j_client.connect()
        logger.info("✓ Connected to Neo4j")
    except Exception as e:
        logger.error(f"✗ Failed to connect to Neo4j: {e}")
        logger.error("Make sure Neo4j is running (docker-compose up -d)")
        return 1

    # Generate sample data
    logger.info("\nGenerating sample narrative data...")
    generator = NarrativeDataGenerator(seed=42)

    try:
        data = generator.generate_all()
        logger.info("✓ Sample data generated")
        logger.info(f"  - {len(data['people'])} people")
        logger.info(f"  - {len(data['groups'])} groups")
        logger.info(f"  - {len(data['themes'])} themes")
        logger.info(f"  - {len(data['values'])} values")
        logger.info(f"  - {len(data['stories'])} stories")
        logger.info(f"  - {len(data['events'])} events")
        logger.info(f"  - {len(data['decisions'])} decisions")
    except Exception as e:
        logger.error(f"✗ Failed to generate data: {e}")
        return 1

    # Populate graph
    logger.info("\nPopulating Neo4j graph...")
    populator = GraphPopulator()

    try:
        populator.populate_all(data)
        logger.info("✓ Graph populated successfully")
    except Exception as e:
        logger.error(f"✗ Failed to populate graph: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Create similarity and contradiction relationships
    try:
        logger.info("\nCreating advanced relationships...")
        populator.create_story_similarity_relationships()
        logger.info("✓ Similarity relationships created")

        populator.create_contradiction_relationships()
        logger.info("✓ Contradiction relationships created")
    except Exception as e:
        logger.warning(f"⚠ Failed to create some relationships: {e}")

    # Print final stats
    logger.info("\nDatabase Statistics:")
    stats = neo4j_client.get_database_stats()

    if stats.get("nodes"):
        logger.info("\nNode counts:")
        for node_stat in stats["nodes"]:
            logger.info(f"  - {node_stat['label']}: {node_stat['count']}")

    if stats.get("relationships"):
        logger.info("\nRelationship counts:")
        for rel_stat in stats["relationships"]:
            logger.info(f"  - {rel_stat['relationship_type']}: {rel_stat['count']}")

    logger.info("\n" + "=" * 80)
    logger.info("Database initialization complete!")
    logger.info("=" * 80)
    logger.info(f"\nNeo4j Browser: http://localhost:7474")
    logger.info(f"API Documentation: http://localhost:8000/docs")
    logger.info("\nTo start the API server:")
    logger.info("  cd backend && python main.py")

    # Close connection
    neo4j_client.close()

    return 0


if __name__ == "__main__":
    exit(main())
