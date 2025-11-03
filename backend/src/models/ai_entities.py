"""
AI-specific entity models for the narrative knowledge graph.

These models extend the base narrative system to support AI adoption analysis,
including initiatives, concepts, frames, cultural signals, and resistance patterns.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from .base import BaseNode


class AIInitiativeStatus(str, Enum):
    """Status of an AI initiative."""
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class AIInitiativeType(str, Enum):
    """Type of AI initiative."""
    TOOL = "tool"
    PROCESS = "process"
    TRANSFORMATION = "transformation"
    PILOT = "pilot"


class AIConceptCategory(str, Enum):
    """Category of AI concept."""
    TECHNOLOGY = "technology"
    CAPABILITY = "capability"
    RISK = "risk"
    OPPORTUNITY = "opportunity"


class FrameType(str, Enum):
    """Types of narrative frames for AI."""
    OPPORTUNITY = "opportunity"
    THREAT = "threat"
    TOOL = "tool"
    REPLACEMENT = "replacement"
    PARTNER = "partner"
    EXPERIMENT = "experiment"
    MANDATE = "mandate"


class FrameValence(str, Enum):
    """Emotional valence of a frame."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    NEUTRAL = "neutral"


class FrameSophistication(str, Enum):
    """Sophistication level of framing."""
    SIMPLISTIC = "simplistic"
    NUANCED = "nuanced"
    EXPERT = "expert"


class SignalType(str, Enum):
    """Types of cultural signals."""
    RISK_AVERSION = "risk_aversion"
    INNOVATION = "innovation"
    SKEPTICISM = "skepticism"
    ENTHUSIASM = "enthusiasm"


class BarrierType(str, Enum):
    """Types of adoption barriers."""
    CULTURAL = "cultural"
    TECHNICAL = "technical"
    RESOURCE = "resource"
    POLITICAL = "political"


class AIInitiative(BaseNode):
    """
    An AI initiative, project, or tool being introduced in the organization.

    Tracks both official descriptions and how the initiative is actually
    perceived and discussed by employees.
    """
    name: str = Field(..., description="Initiative name")
    type: AIInitiativeType = Field(..., description="Type of initiative")
    official_description: str = Field(..., description="Official/leadership description")
    stated_goals: List[str] = Field(
        default_factory=list,
        description="Officially stated goals"
    )
    timeline: Optional[Dict[str, str]] = Field(
        None,
        description="Timeline with start_date and end_date"
    )
    status: AIInitiativeStatus = Field(..., description="Current status")

    # Story tracking
    official_story_ids: List[str] = Field(
        default_factory=list,
        description="IDs of official/leadership stories about this initiative"
    )
    actual_story_ids: List[str] = Field(
        default_factory=list,
        description="IDs of employee stories about this initiative"
    )

    # Metrics
    awareness_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="How aware employees are of this initiative"
    )
    sentiment_score: Optional[float] = Field(
        None,
        ge=-1.0,
        le=1.0,
        description="Overall employee sentiment"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "official_description": self.official_description,
            "stated_goals": self.stated_goals,
            "timeline": self.timeline or {},
            "status": self.status.value,
            "awareness_score": self.awareness_score or 0.0,
            "sentiment_score": self.sentiment_score or 0.0,
            "created_at": self.created_at.isoformat(),
        }


class AIConcept(BaseNode):
    """
    A term or concept related to AI (e.g., "AI", "automation", "copilot").

    Tracks how different groups understand and react to AI terminology.
    """
    term: str = Field(..., description="The AI term or concept")
    category: AIConceptCategory = Field(..., description="Category of concept")

    # Sentiment profile by group
    sentiment_profile: Dict[str, float] = Field(
        default_factory=dict,
        description="Sentiment scores by group: {group_name: sentiment_score}"
    )

    # Usage patterns
    usage_count: int = Field(default=0, description="How often this term appears")
    groups_using: List[str] = Field(
        default_factory=list,
        description="Groups that use this term"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "term": self.term,
            "category": self.category.value,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat(),
        }


class NarrativeFrame(BaseNode):
    """
    A narrative frame - how AI is positioned and understood.

    Examples: "AI as opportunity", "AI as threat", "AI as tool"
    """
    frame_type: FrameType = Field(..., description="Type of frame")
    description: str = Field(..., description="Description of this frame")
    valence: FrameValence = Field(..., description="Emotional valence")
    sophistication: FrameSophistication = Field(
        ...,
        description="Sophistication of framing"
    )

    # Usage tracking
    story_count: int = Field(default=0, description="Stories using this frame")
    groups_using: List[str] = Field(
        default_factory=list,
        description="Groups that use this frame"
    )

    # Frame characteristics
    typical_language: List[str] = Field(
        default_factory=list,
        description="Common words/phrases in this frame"
    )
    emphasis_points: List[str] = Field(
        default_factory=list,
        description="What this frame emphasizes"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "frame_type": self.frame_type.value,
            "description": self.description,
            "valence": self.valence.value,
            "sophistication": self.sophistication.value,
            "story_count": self.story_count,
            "typical_language": self.typical_language,
            "emphasis_points": self.emphasis_points,
            "created_at": self.created_at.isoformat(),
        }


class CulturalSignal(BaseNode):
    """
    A cultural signal detected in narratives.

    Indicates whether the organization tends toward innovation or risk aversion.
    """
    signal_type: SignalType = Field(..., description="Type of cultural signal")
    strength: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Strength of signal (0-1)"
    )
    evidence: List[str] = Field(
        ...,
        description="Story IDs that provide evidence for this signal"
    )
    group_specificity: Optional[str] = Field(
        None,
        description="Group ID if signal is specific to one group"
    )

    # Analysis
    description: str = Field(..., description="What this signal indicates")
    interpretation: str = Field(..., description="What this means for AI adoption")

    # Temporal tracking
    detected_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this signal was detected"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "signal_type": self.signal_type.value,
            "strength": self.strength,
            "group_specificity": self.group_specificity or "",
            "description": self.description,
            "interpretation": self.interpretation,
            "detected_at": self.detected_at.isoformat(),
            "created_at": self.created_at.isoformat(),
        }


class ResistancePattern(BaseNode):
    """
    A pattern of resistance to AI adoption.

    Examples: passive resistance, active opposition, skepticism
    """
    pattern_name: str = Field(..., description="Name of resistance pattern")
    manifestation: str = Field(
        ...,
        description="How this resistance manifests in narratives"
    )
    root_cause: str = Field(
        ...,
        description="Inferred root cause of resistance"
    )
    affected_initiatives: List[str] = Field(
        default_factory=list,
        description="Initiative IDs affected by this pattern"
    )

    # Severity
    severity: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Severity of resistance (0-1)"
    )

    # Evidence
    evidence_stories: List[str] = Field(
        ...,
        description="Story IDs demonstrating this pattern"
    )
    affected_groups: List[str] = Field(
        default_factory=list,
        description="Groups exhibiting this pattern"
    )

    # Spread tracking
    spreading: bool = Field(
        default=False,
        description="Whether this pattern is spreading"
    )
    spread_velocity: Optional[float] = Field(
        None,
        description="How fast it's spreading (stories per week)"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "pattern_name": self.pattern_name,
            "manifestation": self.manifestation,
            "root_cause": self.root_cause,
            "severity": self.severity,
            "spreading": self.spreading,
            "spread_velocity": self.spread_velocity or 0.0,
            "created_at": self.created_at.isoformat(),
        }


class AdoptionBarrier(BaseNode):
    """
    A barrier to AI adoption.

    Can be cultural, technical, resource-based, or political.
    """
    barrier_type: BarrierType = Field(..., description="Type of barrier")
    description: str = Field(..., description="Description of barrier")
    affected_groups: List[str] = Field(
        ...,
        description="Group IDs affected by this barrier"
    )
    severity: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Severity of barrier (0-1)"
    )

    # Analysis
    evidence_stories: List[str] = Field(
        ...,
        description="Story IDs evidencing this barrier"
    )
    mitigation_strategies: List[str] = Field(
        default_factory=list,
        description="Potential mitigation strategies"
    )

    # Status
    addressable: bool = Field(
        default=True,
        description="Whether this barrier can be addressed"
    )
    addressed: bool = Field(
        default=False,
        description="Whether mitigation has been attempted"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "barrier_type": self.barrier_type.value,
            "description": self.description,
            "severity": self.severity,
            "addressable": self.addressable,
            "addressed": self.addressed,
            "created_at": self.created_at.isoformat(),
        }


class FrameCompetition(BaseModel):
    """
    Analysis of competing frames between groups.

    Shows how different frames conflict and compete for dominance.
    """
    frame_a_id: str
    frame_b_id: str
    frame_a_type: FrameType
    frame_b_type: FrameType
    groups_a: List[str] = Field(..., description="Groups using frame A")
    groups_b: List[str] = Field(..., description="Groups using frame B")
    conflict_type: str = Field(
        ...,
        description="Type of conflict (opposing, complementary, contradictory)"
    )
    impact: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Impact of this competition on adoption"
    )


class NarrativeGap(BaseModel):
    """
    Analysis of gap between official and actual narratives.

    Shows where leadership messaging diverges from employee reality.
    """
    initiative_id: str
    gap_dimensions: Dict[str, Any] = Field(
        ...,
        description="Different dimensions of gaps: vocabulary, framing, emphasis, emotion, belief"
    )
    severity: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall severity of gaps"
    )
    implications: List[str] = Field(
        ...,
        description="What these gaps mean for adoption"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="How to address these gaps"
    )
