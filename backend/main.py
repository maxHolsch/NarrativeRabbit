"""
Main FastAPI application for Narrative Knowledge Graph.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.db import neo4j_client
from src.api import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Narrative Knowledge Graph API...")
    try:
        neo4j_client.connect()
        logger.info("Successfully connected to Neo4j")
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {e}")
        logger.warning("API will start but database operations will fail")

    yield

    # Shutdown
    logger.info("Shutting down...")
    neo4j_client.close()


# Create FastAPI app
app = FastAPI(
    title="Narrative Knowledge Graph API",
    description="""
    API for querying organizational narratives and their relationships.

    ## Features

    * **Story Search**: Find stories by themes, groups, and types
    * **Perspective Analysis**: Compare how different groups tell stories
    * **Pattern Matching**: Find similar situations and precedents
    * **Causal Analysis**: Trace cause-effect relationships
    * **Cultural Insights**: Understand group values and narrative patterns
    * **LLM Extraction**: Extract structured narratives from text

    ## Use Cases

    1. **Decision Support**: Find relevant precedents for current decisions
    2. **Onboarding**: Understand organizational culture through stories
    3. **Cultural Assessment**: Analyze narrative alignment across groups
    4. **Knowledge Management**: Capture and query organizational knowledge
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Narrative Knowledge Graph API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "stories": "/api/stories/search",
            "perspectives": "/api/perspectives/group/{group_name}",
            "patterns": "/api/patterns/precedents",
            "graph": "/api/graph/data",
            "examples": "/api/examples/queries"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        stats = neo4j_client.get_database_stats()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        stats = {}

    return {
        "status": "healthy",
        "database": db_status,
        "stats": stats
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
