"""
Story models representing narratives with multi-layered structure.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from .base import BaseNode, StoryType, NarrativeArc, TellingPurpose


class AISophistication(str, Enum):
    """Sophistication level of AI understanding in story."""
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class InnovationSignal(str, Enum):
    """Innovation culture signal in story."""
    RISK_TAKING = "risk_taking"
    RISK_AVERSE = "risk_averse"
    NEUTRAL = "neutral"


class AgencyFrame(str, Enum):
    """How agency is framed in AI stories."""
    HUMAN_IN_CONTROL = "human_in_control"
    AI_IN_CONTROL = "ai_in_control"
    PARTNERSHIP = "partnership"


class TimeFrame(str, Enum):
    """Temporal frame of the story."""
    PAST_EXPERIENCE = "past_experience"
    CURRENT_STATE = "current_state"
    FUTURE_VISION = "future_vision"


class NarrativeFunction(str, Enum):
    """Function of the narrative."""
    WARNING = "warning"
    CELEBRATION = "celebration"
    EXPLANATION = "explanation"
    JUSTIFICATION = "justification"


class ContentLayer(BaseModel):
    """Content layer of a story - what happened."""
    summary: str = Field(..., description="Brief summary of the story (2-3 sentences)")
    full_text: str = Field(..., description="Complete narrative text")
    key_quotes: List[str] = Field(default_factory=list, description="Notable quotes from the story")
    outcome: str = Field(..., description="What resulted from the events")


class StructureLayer(BaseModel):
    """Structure layer - how the story is organized."""
    story_type: StoryType
    narrative_arc: Dict[NarrativeArc, str] = Field(
        ...,
        description="Story arc stages with descriptions"
    )
    temporal_sequence: List[str] = Field(
        default_factory=list,
        description="Ordered list of events"
    )
    causal_chain: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Cause-effect relationships: [{'cause': '...', 'effect': '...'}]"
    )


class ActorLayer(BaseModel):
    """Actor layer - who was involved."""
    protagonists: List[str] = Field(
        default_factory=list,
        description="Main actors who drove the action"
    )
    stakeholders: List[str] = Field(
        default_factory=list,
        description="People affected by events"
    )
    decision_makers: List[str] = Field(
        default_factory=list,
        description="People who made key decisions"
    )
    group_affiliations: List[str] = Field(
        default_factory=list,
        description="Groups/teams involved"
    )


class ThemeLayer(BaseModel):
    """Theme layer - what it means."""
    primary_themes: List[str] = Field(
        ...,
        max_length=5,
        description="Core themes (max 5)"
    )
    problems_addressed: List[str] = Field(
        default_factory=list,
        description="Issues/challenges this story addresses"
    )
    values_expressed: List[str] = Field(
        default_factory=list,
        description="Organizational values demonstrated"
    )
    lessons_learned: List[str] = Field(
        default_factory=list,
        description="Key takeaways and learnings"
    )


class ContextLayer(BaseModel):
    """Context layer - when, where, and why."""
    timestamp: datetime = Field(..., description="When the events occurred")
    era: Optional[str] = Field(None, description="Era or phase (e.g., 'early startup', 'post-Series-B')")
    department: Optional[str] = Field(None, description="Department context")
    project: Optional[str] = Field(None, description="Associated project")
    why_told: TellingPurpose = Field(..., description="Purpose of telling this story")
    trigger_events: List[str] = Field(
        default_factory=list,
        description="Events that triggered this story"
    )


class AIAnalysisLayer(BaseModel):
    """
    AI analysis layer - AI-specific properties for narrative intelligence.

    Used to analyze organizational AI adoption patterns, cultural signals,
    and narrative gaps.
    """
    ai_related: bool = Field(
        default=False,
        description="Whether this story relates to AI/automation"
    )
    ai_sentiment: Optional[float] = Field(
        None,
        ge=-1.0,
        le=1.0,
        description="Sentiment toward AI in this story (-1 to 1)"
    )
    ai_sophistication: Optional[AISophistication] = Field(
        None,
        description="Level of AI understanding demonstrated"
    )
    innovation_signal: Optional[InnovationSignal] = Field(
        None,
        description="Innovation vs risk-aversion signal"
    )
    agency_frame: Optional[AgencyFrame] = Field(
        None,
        description="How control/agency is framed"
    )
    time_frame: Optional[TimeFrame] = Field(
        None,
        description="Temporal framing of the narrative"
    )
    narrative_function: Optional[NarrativeFunction] = Field(
        None,
        description="Function this narrative serves"
    )

    # Additional AI-specific metadata
    ai_concepts_mentioned: List[str] = Field(
        default_factory=list,
        description="AI concepts/terms mentioned (e.g., 'copilot', 'automation')"
    )
    experimentation_indicator: bool = Field(
        default=False,
        description="Whether story indicates experimentation with AI"
    )
    failure_framing: Optional[str] = Field(
        None,
        description="How failures are framed: 'learning', 'warning', 'neutral'"
    )


class VariationLayer(BaseModel):
    """Variation layer - how different groups tell it."""
    teller_identity: str = Field(..., description="Who is telling this version")
    teller_role: str = Field(..., description="Role of the teller")
    teller_department: str = Field(..., description="Department of the teller")
    audience: List[str] = Field(
        default_factory=list,
        description="Who this was told to"
    )
    framing: str = Field(..., description="How the story is positioned/framed")
    emphasis: List[str] = Field(
        default_factory=list,
        description="What aspects are highlighted"
    )
    downplayed: List[str] = Field(
        default_factory=list,
        description="What aspects are minimized or omitted"
    )
    telling_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this version was told"
    )


class Story(BaseNode):
    """
    Complete story model with all layers.

    Represents an organizational narrative with:
    - Content: What happened
    - Structure: How it's organized
    - Actors: Who was involved
    - Themes: What it means
    - Context: When, where, why
    - Variations: Different tellings
    - AI Analysis: AI-specific properties (optional)
    """
    # Core layers
    content: ContentLayer
    structure: StructureLayer
    actors: ActorLayer
    themes: ThemeLayer
    context: ContextLayer
    variations: List[VariationLayer] = Field(
        default_factory=list,
        description="Different versions/tellings of this story"
    )

    # AI analysis layer (optional)
    ai_analysis: Optional[AIAnalysisLayer] = Field(
        None,
        description="AI-specific analysis properties"
    )

    # Metadata
    source: str = Field(..., description="Where this story came from (e.g., 'slack', 'interview')")
    confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence in extraction quality"
    )
    tags: List[str] = Field(default_factory=list)

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        node_props = {
            "id": self.id,
            "summary": self.content.summary,
            "full_text": self.content.full_text,
            "outcome": self.content.outcome,
            "type": self.structure.story_type.value,
            "timestamp": self.context.timestamp.isoformat(),
            "era": self.context.era,
            "department": self.context.department,
            "project": self.context.project,
            "why_told": self.context.why_told.value,
            "primary_themes": self.themes.primary_themes,
            "lessons": self.themes.lessons_learned,
            "source": self.source,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat(),
        }

        # Add AI analysis properties if available
        if self.ai_analysis:
            ai_props = {
                "ai_related": self.ai_analysis.ai_related,
                "ai_sentiment": self.ai_analysis.ai_sentiment,
                "ai_sophistication": self.ai_analysis.ai_sophistication.value if self.ai_analysis.ai_sophistication else None,
                "innovation_signal": self.ai_analysis.innovation_signal.value if self.ai_analysis.innovation_signal else None,
                "agency_frame": self.ai_analysis.agency_frame.value if self.ai_analysis.agency_frame else None,
                "time_frame": self.ai_analysis.time_frame.value if self.ai_analysis.time_frame else None,
                "narrative_function": self.ai_analysis.narrative_function.value if self.ai_analysis.narrative_function else None,
                "ai_concepts_mentioned": self.ai_analysis.ai_concepts_mentioned,
                "experimentation_indicator": self.ai_analysis.experimentation_indicator,
                "failure_framing": self.ai_analysis.failure_framing,
            }
            node_props.update(ai_props)

        return node_props

    def add_variation(self, variation: VariationLayer) -> None:
        """Add a new telling variation to this story."""
        self.variations.append(variation)
        self.updated_at = datetime.utcnow()


class StoryComparison(BaseModel):
    """Comparison of different tellings of the same story."""
    event_id: str
    story_ids: List[str]
    differences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Differences in emphasis, attribution, hero, lesson, tone"
    )
    common_elements: List[str] = Field(default_factory=list)
    group_perspectives: Dict[str, str] = Field(default_factory=dict)
