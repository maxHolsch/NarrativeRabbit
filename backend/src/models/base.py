"""
Base models and enums for the narrative knowledge graph.
"""
from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class StoryType(str, Enum):
    """Types of organizational stories."""
    SUCCESS = "success"
    FAILURE = "failure"
    CONFLICT = "conflict"
    DECISION = "decision"
    LEARNING = "learning"
    CRISIS = "crisis"


class NarrativeArc(str, Enum):
    """Stages in a narrative arc."""
    SETUP = "setup"
    COMPLICATION = "complication"
    RISING_ACTION = "rising_action"
    CLIMAX = "climax"
    RESOLUTION = "resolution"
    REFLECTION = "reflection"


class ActorRole(str, Enum):
    """Roles that actors can play in stories."""
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist"
    DECISION_MAKER = "decision_maker"
    STAKEHOLDER = "stakeholder"
    WITNESS = "witness"
    SUPPORTER = "supporter"


class TellingPurpose(str, Enum):
    """Why a story is told."""
    TEACHING = "teaching"
    WARNING = "warning"
    CELEBRATING = "celebrating"
    EXPLAINING = "explaining"
    BONDING = "bonding"
    PERSUADING = "persuading"


class RelationshipType(str, Enum):
    """Types of relationships in the graph."""
    TELLS = "TELLS"
    ABOUT = "ABOUT"
    INVOLVES = "INVOLVES"
    BELONGS_TO = "BELONGS_TO"
    EXEMPLIFIES = "EXEMPLIFIES"
    LED_TO = "LED_TO"
    CONTRADICTS = "CONTRADICTS"
    ECHOES = "ECHOES"
    REFRAMES = "REFRAMES"
    PRECEDES = "PRECEDES"
    RESULTED_IN = "RESULTED_IN"

    # AI-specific relationships
    DESCRIBES_AI = "DESCRIBES_AI"  # Story describes an AI initiative
    USES_FRAME = "USES_FRAME"  # Story uses a narrative frame
    REVEALS = "REVEALS"  # Story reveals a cultural signal
    INDICATES = "INDICATES"  # Story indicates a resistance pattern
    ENCOUNTERS = "ENCOUNTERS"  # Group encounters an adoption barrier
    COMPETES_WITH = "COMPETES_WITH"  # Frame competes with another frame
    HAS_OFFICIAL_STORY = "HAS_OFFICIAL_STORY"  # Initiative has official narrative
    HAS_ACTUAL_STORIES = "HAS_ACTUAL_STORIES"  # Initiative has actual employee stories
    MENTIONS_CONCEPT = "MENTIONS_CONCEPT"  # Story mentions an AI concept


class BaseNode(BaseModel):
    """Base model for all graph nodes."""
    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BaseRelationship(BaseModel):
    """Base model for graph relationships."""
    from_id: str = Field(..., description="Source node ID")
    to_id: str = Field(..., description="Target node ID")
    type: RelationshipType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    properties: dict = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
