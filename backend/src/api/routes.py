"""
API routes for the narrative knowledge graph.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel

from ..services.graph.graph_queries import NarrativeQueryService
from ..services.extraction.claude_extractor import ClaudeNarrativeExtractor
from .ai_routes import router as ai_router

router = APIRouter()
query_service = NarrativeQueryService()
extractor = ClaudeNarrativeExtractor()

# Include AI routes
router.include_router(ai_router)


# Health check endpoint
@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint to verify system status."""
    try:
        # Test Neo4j connection by running a simple query
        query_service.search_stories(limit=1)
        neo4j_status = "connected"
    except Exception as e:
        neo4j_status = "disconnected"

    return {
        "status": "healthy" if neo4j_status == "connected" else "degraded",
        "neo4j": neo4j_status,
        "api": "operational"
    }


# Request/Response Models
class StorySearchRequest(BaseModel):
    """Request model for story search."""
    themes: Optional[List[str]] = None
    groups: Optional[List[str]] = None
    story_type: Optional[str] = None
    limit: int = 10


class NarrativeExtractionRequest(BaseModel):
    """Request model for narrative extraction."""
    text: str
    story_id: str
    source: str = "user_input"
    context: Optional[Dict[str, Any]] = None


# Stories endpoints
@router.get("/stories/search")
async def search_stories(
    themes: Optional[List[str]] = Query(None),
    groups: Optional[List[str]] = Query(None),
    story_type: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """
    Search for stories matching criteria.

    - **themes**: Filter by themes
    - **groups**: Filter by group involvement
    - **story_type**: Filter by story type (success, failure, etc.)
    - **limit**: Maximum number of results
    """
    try:
        results = query_service.search_stories(
            themes=themes,
            groups=groups,
            story_type=story_type,
            limit=limit
        )
        # Return empty list if no results instead of error
        return results if results else []
    except Exception as e:
        # Log the error but return empty list to prevent frontend crashes
        import logging
        logging.error(f"Error searching stories: {e}")
        return []


@router.get("/stories/{story_id}")
async def get_story(story_id: str) -> Dict[str, Any]:
    """Get a specific story by ID."""
    try:
        results = query_service.search_stories(limit=1000)
        story = next((s for s in results if s.get("id") == story_id), None)

        if not story:
            raise HTTPException(status_code=404, detail="Story not found")

        return story
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Perspective endpoints
@router.get("/perspectives/group/{group_name}")
async def get_group_perspective(
    group_name: str,
    topic: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """
    Get how a group frames topics in their stories.

    - **group_name**: Name of the group
    - **topic**: Optional topic filter
    """
    try:
        perspective = query_service.get_group_perspective(group_name, topic)
        return perspective
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/perspectives/compare/{event_name}")
async def compare_perspectives(event_name: str) -> Dict[str, Any]:
    """
    Compare how different groups tell stories about the same event.

    - **event_name**: Name of the event to compare
    """
    try:
        comparison = query_service.compare_perspectives(event_name)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Pattern matching endpoints
@router.get("/patterns/precedents")
async def find_precedents(
    themes: List[str] = Query(...),
    story_type: Optional[str] = Query(None),
    limit: int = Query(5, ge=1, le=20)
) -> List[Dict[str, Any]]:
    """
    Find similar past situations based on themes.

    - **themes**: Themes to match
    - **story_type**: Optional story type filter
    - **limit**: Number of results
    """
    try:
        precedents = query_service.find_precedents(
            themes=themes,
            story_type=story_type,
            limit=limit
        )
        return precedents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/similar/{story_id}")
async def find_similar_patterns(
    story_id: str,
    min_shared_themes: int = Query(2, ge=1, le=5)
) -> List[Dict[str, Any]]:
    """
    Find stories with similar patterns to a current situation.

    - **story_id**: ID of the current story
    - **min_shared_themes**: Minimum number of shared themes
    """
    try:
        similar = query_service.find_similar_patterns(story_id, min_shared_themes)
        return similar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/cautionary")
async def get_cautionary_tales(
    themes: List[str] = Query(...)
) -> List[Dict[str, Any]]:
    """
    Get cautionary tales (failure stories) about specific themes.

    - **themes**: Themes to search for
    """
    try:
        tales = query_service.get_cautionary_tales(themes)
        return tales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Analysis endpoints
@router.get("/analysis/causality/{story_id}")
async def trace_causality(story_id: str) -> Dict[str, Any]:
    """
    Show causal relationships in a story.

    - **story_id**: Story to analyze
    """
    try:
        causality = query_service.trace_causality(story_id)
        return causality
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/values/{group_name}")
async def get_group_values(group_name: str) -> List[Dict[str, Any]]:
    """
    Get values emphasized by a group in their stories.

    - **group_name**: Name of the group
    """
    try:
        values = query_service.get_group_value_emphasis(group_name)
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Index endpoints
@router.get("/index/{dimension}")
async def get_narrative_index(
    dimension: str = Path(..., regex="^(theme|group|type|value)$")
) -> List[Dict[str, Any]]:
    """
    Get index of narratives by dimension.

    - **dimension**: One of: theme, group, type, value
    """
    try:
        index = query_service.get_narrative_index(dimension)
        return index if index else []
    except Exception as e:
        import logging
        logging.error(f"Error getting narrative index for {dimension}: {e}")
        return []


# Graph data endpoint
@router.get("/graph/data")
async def get_graph_data(
    limit: int = Query(100, ge=10, le=500)
) -> Dict[str, Any]:
    """
    Get graph data for visualization (D3.js format).

    - **limit**: Maximum number of nodes
    """
    try:
        data = query_service.get_graph_data_for_visualization(limit)
        # Always return valid structure even if empty
        if not data or not isinstance(data, dict):
            return {"nodes": [], "links": []}
        return data
    except Exception as e:
        # Log the error but return empty graph structure
        import logging
        logging.error(f"Error getting graph data: {e}")
        return {"nodes": [], "links": []}


# Extraction endpoints
@router.post("/extract/narrative")
async def extract_narrative(request: NarrativeExtractionRequest) -> Dict[str, Any]:
    """
    Extract structured narrative elements from text using Claude API.

    - **text**: Raw narrative text
    - **story_id**: Unique identifier for the story
    - **source**: Source of the narrative (default: user_input)
    - **context**: Optional context information
    """
    try:
        story = extractor.extract_and_create_story(
            text=request.text,
            story_id=request.story_id,
            source=request.source,
            context=request.context
        )

        return {
            "story_id": story.id,
            "extracted": {
                "summary": story.content.summary,
                "themes": story.themes.primary_themes,
                "actors": {
                    "protagonists": story.actors.protagonists,
                    "stakeholders": story.actors.stakeholders
                },
                "story_type": story.structure.story_type.value,
                "lessons": story.themes.lessons_learned
            },
            "full_story": story.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Query examples endpoint
@router.get("/examples/queries")
async def get_query_examples() -> Dict[str, Any]:
    """Get example queries and use cases."""
    return {
        "queries": [
            {
                "name": "Stories by group and topic",
                "description": "What stories do engineers tell about product decisions?",
                "endpoint": "/stories/search?groups=Engineering Team&themes=prioritization&themes=technical-debt"
            },
            {
                "name": "Event comparison",
                "description": "How is 'The Big Feature Launch' told differently by groups?",
                "endpoint": "/perspectives/compare/The Big Feature Launch"
            },
            {
                "name": "Group values",
                "description": "What values does the Executive Team emphasize?",
                "endpoint": "/analysis/values/Executive Team"
            },
            {
                "name": "Similar patterns",
                "description": "Find stories with similar patterns",
                "endpoint": "/patterns/similar/{story_id}?min_shared_themes=2"
            },
            {
                "name": "Cautionary tales",
                "description": "What cautionary tales exist about moving too fast?",
                "endpoint": "/patterns/cautionary?themes=speed&themes=risk"
            },
            {
                "name": "Theme index",
                "description": "Browse narratives by theme",
                "endpoint": "/index/theme"
            }
        ]
    }
