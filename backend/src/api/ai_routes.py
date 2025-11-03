"""
AI Narrative Intelligence API Routes

FastAPI routes for AI narrative analysis, including:
- AI initiative management
- Strategic question workflows
- Sub-agent analyses
- Comprehensive analysis
- Executive reporting
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field

from ..services.ai_narrative_intelligence_agent import AInarrativeIntelligenceAgent
from ..services.queries.ai_queries import AIQueries
from ..services.chat_agent import ChatAgent
from ..db.neo4j_client import neo4j_client


# Initialize router and services
router = APIRouter(prefix="/ai", tags=["AI Analysis"])

# Use global neo4j_client instance (connected in main.py)
ai_agent = AInarrativeIntelligenceAgent(neo4j_client)
ai_queries = AIQueries(neo4j_client)
chat_agent = ChatAgent()


# ==================== REQUEST/RESPONSE MODELS ====================

class AIInitiativeCreate(BaseModel):
    """Request model for creating AI initiative."""
    id: str
    name: str
    type: str = Field(..., pattern="^(tool|process|transformation|pilot)$")
    official_description: str
    stated_goals: List[str]
    status: str = Field(default="planned", pattern="^(planned|active|paused|completed|failed)$")


class ComprehensiveAnalysisRequest(BaseModel):
    """Request model for comprehensive analysis."""
    initiative_id: Optional[str] = None
    include_recommendations: bool = True
    generate_action_plan: bool = True


class ChatMessage(BaseModel):
    """Request model for chat message."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="ID to maintain conversation context")
    conversation_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous messages in conversation")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context (initiative_id, etc.)")


# ==================== AI INITIATIVE ENDPOINTS ====================

@router.get("/initiatives")
async def get_all_initiatives() -> List[Dict[str, Any]]:
    """
    Get all AI initiatives.

    Returns list of all registered AI initiatives with their properties.
    """
    try:
        initiatives = ai_queries.get_all_ai_initiatives()
        return initiatives
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/initiatives/{initiative_id}")
async def get_initiative(initiative_id: str) -> Dict[str, Any]:
    """
    Get a specific AI initiative by ID.

    - **initiative_id**: Unique identifier of the initiative
    """
    try:
        initiative = ai_queries.get_initiative_by_id(initiative_id)
        if not initiative:
            raise HTTPException(status_code=404, detail="Initiative not found")
        return initiative
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/initiatives")
async def create_initiative(initiative: AIInitiativeCreate) -> Dict[str, Any]:
    """
    Create a new AI initiative.

    - **id**: Unique identifier
    - **name**: Initiative name
    - **type**: One of: tool, process, transformation, pilot
    - **official_description**: Official description
    - **stated_goals**: List of stated goals
    - **status**: Current status (default: planned)
    """
    try:
        created = ai_queries.create_ai_initiative(initiative.dict())
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create initiative")
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/initiatives/{initiative_id}/stories")
async def get_initiative_stories(
    initiative_id: str,
    story_type: str = Query("all", pattern="^(all|official|actual)$")
) -> Dict[str, Any]:
    """
    Get stories related to an AI initiative.

    - **initiative_id**: Initiative identifier
    - **story_type**: Type of stories to fetch (all, official, actual)
    """
    try:
        if story_type == "official":
            stories = ai_queries.get_initiative_official_stories(initiative_id)
            return {"story_type": "official", "count": len(stories), "stories": stories}
        elif story_type == "actual":
            stories = ai_queries.get_initiative_actual_stories(initiative_id)
            return {"story_type": "actual", "count": len(stories), "stories": stories}
        else:
            official = ai_queries.get_initiative_official_stories(initiative_id)
            actual = ai_queries.get_initiative_actual_stories(initiative_id)
            return {
                "official": {"count": len(official), "stories": official},
                "actual": {"count": len(actual), "stories": actual}
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== STRATEGIC QUESTION ENDPOINTS ====================

@router.get("/analysis/question1")
async def answer_question_1(
    initiative_id: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """
    Q1: How do different teams/departments talk about AI differently?

    Analyzes vocabulary gaps, frame differences, sentiment variations,
    and sophistication levels across groups.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_agent.answer_question_1(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/question2")
async def answer_question_2() -> Dict[str, Any]:
    """
    Q2: Do we have an entrepreneurial culture that supports AI?

    Assesses innovation vs risk-aversion, experimentation indicators,
    failure tolerance, and learning orientation.
    """
    try:
        result = ai_agent.answer_question_2()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/question3/{initiative_id}")
async def answer_question_3(initiative_id: str) -> Dict[str, Any]:
    """
    Q3: Can you design a unified story that bridges different groups?

    Creates unified narrative by analyzing fragmentation, finding common ground,
    and designing messaging strategy.

    - **initiative_id**: Initiative to create unified story for (required)
    """
    try:
        result = ai_agent.answer_question_3(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/question4")
async def answer_question_4() -> Dict[str, Any]:
    """
    Q4: Are we risk-averse, and where does that show up?

    Identifies risk-aversion patterns, resistance hotspots, root causes,
    and intervention strategies.
    """
    try:
        result = ai_agent.answer_question_4()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/question5")
async def answer_question_5(
    initiative_id: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """
    Q5: Why does language vary by context?

    Explains context-driven language differences, trust factors,
    knowledge gaps, and strategic vs tactical framing.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_agent.answer_question_5(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== SUB-AGENT ANALYSIS ENDPOINTS ====================

@router.get("/analysis/gaps")
async def analyze_narrative_gaps(
    initiative_id: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """
    Analyze narrative gaps between official and actual stories.

    Uses NarrativeGapAnalyzer to compare vocabulary, framing, emphasis,
    sentiment, and beliefs.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_agent.gap_analyzer.analyze_official_vs_actual(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/frames")
async def analyze_frame_competition(
    initiative_id: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """
    Analyze competing narrative frames.

    Uses FrameCompetitionAnalyzer to map frames, identify conflicts,
    and find common ground.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_agent.frame_analyzer.map_competing_frames(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/culture")
async def assess_innovation_culture() -> Dict[str, Any]:
    """
    Assess organizational innovation culture.

    Uses CulturalSignalDetector to score experimentation, failure tolerance,
    agency, iteration speed, and narrative diversity.
    """
    try:
        result = ai_agent.culture_detector.assess_innovation_culture()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/resistance")
async def map_resistance_landscape() -> Dict[str, Any]:
    """
    Map resistance patterns across organization.

    Uses ResistanceMapper to identify patterns, root causes,
    narrative spread, and blocking effects.
    """
    try:
        result = ai_agent.resistance_mapper.map_resistance_landscape()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/readiness")
async def assess_adoption_readiness(
    initiative_id: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """
    Assess organizational readiness for AI adoption.

    Uses AdoptionReadinessScorer to score 6 dimensions: narrative alignment,
    cultural receptivity, trust, learning orientation, leadership coherence,
    and coordination narrative.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_agent.readiness_scorer.assess_readiness(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== COMPREHENSIVE ANALYSIS ENDPOINT ====================

@router.post("/analysis/comprehensive")
async def run_comprehensive_analysis(
    request: ComprehensiveAnalysisRequest
) -> Dict[str, Any]:
    """
    Run comprehensive AI narrative analysis across all 5 strategic questions.

    Generates:
    - All question answers
    - Executive summary
    - Action plan with prioritized recommendations

    - **initiative_id**: Optional initiative to focus on
    - **include_recommendations**: Include detailed recommendations
    - **generate_action_plan**: Generate prioritized action plan
    """
    try:
        result = ai_agent.run_comprehensive_analysis(request.initiative_id)

        if not request.include_recommendations:
            # Remove recommendations from sub-analyses to reduce payload size
            for key in result.get('detailed_analyses', {}):
                if 'recommendations' in result['detailed_analyses'][key]:
                    del result['detailed_analyses'][key]['recommendations']

        if not request.generate_action_plan:
            # Remove action plan if not requested
            if 'action_plan' in result:
                del result['action_plan']

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== DATA QUERY ENDPOINTS ====================

@router.get("/stories/ai")
async def get_ai_stories(
    group: Optional[str] = Query(None),
    sentiment_min: Optional[float] = Query(None, ge=-1.0, le=1.0),
    frame: Optional[str] = Query(None),
    sophistication: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
) -> List[Dict[str, Any]]:
    """
    Get AI-related stories with optional filters.

    - **group**: Filter by teller group
    - **sentiment_min**: Minimum sentiment threshold (-1.0 to 1.0)
    - **frame**: Filter by agency frame
    - **sophistication**: Filter by AI sophistication level
    - **limit**: Maximum number of results
    """
    try:
        if group:
            stories = ai_queries.get_ai_stories_by_group(group, limit)
        elif sentiment_min is not None:
            stories = ai_queries.get_ai_stories_by_sentiment(sentiment_min, limit)
        elif frame:
            stories = ai_queries.get_ai_stories_by_frame(frame, limit)
        elif sophistication:
            stories = ai_queries.get_ai_stories_by_sophistication(sophistication, limit)
        else:
            stories = ai_queries.get_all_ai_stories(limit)

        return stories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/sentiment-by-group")
async def get_sentiment_by_group(
    initiative_id: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """
    Get sentiment summary by group.

    Returns average, min, max sentiment and story count for each group.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_queries.get_group_sentiment_summary(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/frame-distribution")
async def get_frame_distribution(
    initiative_id: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """
    Get distribution of narrative frames.

    Returns count and groups for each frame type.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_queries.get_frame_distribution(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/adoption-timeline")
async def get_adoption_timeline(
    initiative_id: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """
    Get timeline of AI story creation and sentiment trends.

    - **initiative_id**: Optional initiative to focus on
    """
    try:
        result = ai_queries.get_ai_adoption_timeline(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/influential-stories")
async def get_influential_stories(
    limit: int = Query(20, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """
    Get most influential AI stories based on reference count.

    - **limit**: Maximum number of stories to return
    """
    try:
        result = ai_queries.get_most_influential_stories(limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/group-connectivity")
async def get_group_connectivity() -> List[Dict[str, Any]]:
    """
    Get connectivity between groups through story references.

    Shows which groups reference each other's stories and how often.
    """
    try:
        result = ai_queries.get_group_connectivity()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RESISTANCE & BARRIERS ENDPOINTS ====================

@router.get("/resistance/patterns")
async def get_resistance_patterns(
    group: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200)
) -> List[Dict[str, Any]]:
    """
    Get detected resistance patterns.

    - **group**: Filter by affected group
    - **limit**: Maximum number of patterns
    """
    try:
        if group:
            patterns = ai_queries.get_resistance_patterns_by_group(group, limit)
        else:
            patterns = ai_queries.get_all_resistance_patterns(limit)

        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resistance/root-causes/{group}")
async def get_resistance_root_causes(group: str) -> Dict[str, Any]:
    """
    Infer root causes of resistance for a specific group.

    Analyzes past failures, threat perception, resources, values, and knowledge gaps.

    - **group**: Group to analyze
    """
    try:
        result = ai_agent.resistance_mapper.infer_root_causes(group)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/barriers")
async def get_adoption_barriers(
    barrier_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """
    Get identified adoption barriers.

    - **barrier_type**: Filter by barrier type
    - **limit**: Maximum number of barriers
    """
    try:
        if barrier_type:
            barriers = ai_queries.get_barriers_by_type(barrier_type, limit)
        else:
            barriers = ai_queries.get_all_adoption_barriers(limit)

        return barriers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CULTURAL SIGNALS ENDPOINTS ====================

@router.get("/culture/signals")
async def get_cultural_signals(
    signal_type: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=200)
) -> List[Dict[str, Any]]:
    """
    Get detected cultural signals.

    - **signal_type**: Filter by signal type (innovation, risk_aversion, etc.)
    - **limit**: Maximum number of signals
    """
    try:
        if signal_type:
            signals = ai_queries.get_cultural_signals_by_type(signal_type, limit)
        else:
            signals = ai_queries.get_all_cultural_signals(limit)

        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/culture/risk-aversion")
async def detect_risk_aversion() -> Dict[str, Any]:
    """
    Detect risk-aversion patterns in the organization.

    Returns patterns, affected groups, severity, and recommendations.
    """
    try:
        result = ai_agent.culture_detector.detect_risk_aversion_patterns()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CONCEPTS & FRAMES ENDPOINTS ====================

@router.get("/concepts")
async def get_ai_concepts(
    limit: int = Query(100, ge=1, le=200)
) -> List[Dict[str, Any]]:
    """
    Get AI concepts mentioned in stories.

    Returns concepts sorted by mention count.

    - **limit**: Maximum number of concepts
    """
    try:
        concepts = ai_queries.get_all_ai_concepts(limit)
        return concepts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/concepts/{concept_id}/co-occurrence")
async def get_concept_co_occurrence(
    concept_id: str,
    limit: int = Query(20, ge=1, le=50)
) -> List[Dict[str, Any]]:
    """
    Get concepts that co-occur with a given concept.

    - **concept_id**: Concept to analyze
    - **limit**: Maximum number of related concepts
    """
    try:
        result = ai_queries.get_concept_co_occurrence(concept_id, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frames")
async def get_narrative_frames() -> List[Dict[str, Any]]:
    """
    Get all narrative frames.

    Returns all detected narrative frames used to describe AI.
    """
    try:
        frames = ai_queries.get_all_narrative_frames()
        return frames
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frames/conflicts/{initiative_id}")
async def get_frame_conflicts(initiative_id: str) -> List[Dict[str, Any]]:
    """
    Identify frame conflicts for an initiative.

    Returns competing frames and their conflict characteristics.

    - **initiative_id**: Initiative to analyze
    """
    try:
        result = ai_agent.frame_analyzer.identify_frame_conflicts(initiative_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CHAT ENDPOINT ====================

@router.post("/chat")
async def chat(request: ChatMessage) -> Dict[str, Any]:
    """
    Chat with AI agent about the narrative graph.

    Send a message and get an AI-generated response based on graph data.
    Supports conversation history for context-aware responses.

    - **message**: User's question or message
    - **conversation_id**: Optional ID to maintain conversation context
    - **conversation_history**: Previous messages in conversation
    - **context**: Additional context like initiative_id

    Returns:
    - **response**: AI-generated natural language response
    - **sources**: Cited sources (stories, initiatives, etc.)
    - **suggested_followups**: Suggested follow-up questions
    - **intent**: Classified intent type
    - **data_summary**: Summary of retrieved data
    """
    try:
        result = await chat_agent.chat(
            message=request.message,
            conversation_history=request.conversation_history,
            context=request.context
        )

        # Add conversation_id if not provided
        if not request.conversation_id:
            import uuid
            result['conversation_id'] = str(uuid.uuid4())
        else:
            result['conversation_id'] = request.conversation_id

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")


# ==================== UTILITY ENDPOINTS ====================

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for AI analysis service."""
    try:
        # Test database connectivity
        ai_queries.get_all_ai_initiatives()
        return {"status": "healthy", "service": "ai-narrative-intelligence"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@router.get("/examples")
async def get_api_examples() -> Dict[str, Any]:
    """Get example API usage patterns."""
    return {
        "strategic_questions": [
            {
                "name": "Team differences",
                "description": "How do different teams talk about AI?",
                "endpoint": "/ai/analysis/question1?initiative_id=ai_chatbot_2024"
            },
            {
                "name": "Culture assessment",
                "description": "Do we have entrepreneurial culture?",
                "endpoint": "/ai/analysis/question2"
            },
            {
                "name": "Unified story",
                "description": "Design unified narrative",
                "endpoint": "/ai/analysis/question3/ai_chatbot_2024"
            },
            {
                "name": "Risk aversion",
                "description": "Where is risk aversion showing up?",
                "endpoint": "/ai/analysis/question4"
            },
            {
                "name": "Language context",
                "description": "Why does language vary?",
                "endpoint": "/ai/analysis/question5"
            }
        ],
        "sub_agent_analyses": [
            {
                "name": "Narrative gaps",
                "endpoint": "/ai/analysis/gaps?initiative_id=ai_chatbot_2024"
            },
            {
                "name": "Frame competition",
                "endpoint": "/ai/analysis/frames"
            },
            {
                "name": "Innovation culture",
                "endpoint": "/ai/analysis/culture"
            },
            {
                "name": "Resistance mapping",
                "endpoint": "/ai/analysis/resistance"
            },
            {
                "name": "Adoption readiness",
                "endpoint": "/ai/analysis/readiness"
            }
        ],
        "comprehensive": {
            "name": "Full analysis",
            "description": "Run all 5 questions with executive dashboard",
            "endpoint": "/ai/analysis/comprehensive",
            "method": "POST",
            "body": {
                "initiative_id": "ai_chatbot_2024",
                "include_recommendations": True,
                "generate_action_plan": True
            }
        }
    }
