"""
Entity models for actors, groups, events, themes, and other graph nodes.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from .base import BaseNode, ActorRole


class Person(BaseNode):
    """A person who appears in or tells stories."""
    name: str = Field(..., description="Person's name")
    role: str = Field(..., description="Primary role (e.g., 'PM', 'Engineer', 'CEO')")
    department: str = Field(..., description="Department affiliation")
    seniority: Optional[str] = Field(None, description="Seniority level")
    bio: Optional[str] = Field(None, description="Brief biography")

    # Story involvement
    stories_told: List[str] = Field(
        default_factory=list,
        description="IDs of stories this person has told"
    )
    stories_involved_in: List[str] = Field(
        default_factory=list,
        description="IDs of stories this person appears in"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "seniority": self.seniority or "",
            "bio": self.bio or "",
            "created_at": self.created_at.isoformat(),
        }


class Group(BaseNode):
    """A team, department, or organizational unit."""
    name: str = Field(..., description="Group name")
    type: str = Field(..., description="Type (e.g., 'department', 'team', 'workgroup')")
    description: Optional[str] = Field(None, description="Group description")
    parent_group: Optional[str] = Field(None, description="Parent group ID if hierarchical")

    # Membership
    members: List[str] = Field(
        default_factory=list,
        description="Person IDs who belong to this group"
    )

    # Narrative characteristics
    common_themes: List[str] = Field(
        default_factory=list,
        description="Themes commonly emphasized by this group"
    )
    values_emphasized: List[str] = Field(
        default_factory=list,
        description="Values this group emphasizes in their stories"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description or "",
            "parent_group": self.parent_group or "",
            "created_at": self.created_at.isoformat(),
        }


class Event(BaseNode):
    """A specific occurrence that stories reference."""
    name: str = Field(..., description="Event name")
    description: str = Field(..., description="What happened")
    timestamp: datetime = Field(..., description="When it occurred")
    category: str = Field(..., description="Event category (e.g., 'launch', 'incident', 'decision')")

    # Context
    participants: List[str] = Field(
        default_factory=list,
        description="Person IDs involved"
    )
    affected_groups: List[str] = Field(
        default_factory=list,
        description="Group IDs affected"
    )

    # Impact
    impact: Optional[str] = Field(None, description="Description of impact")
    severity: Optional[int] = Field(None, ge=1, le=5, description="Severity/importance (1-5)")

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category,
            "impact": self.impact or "",
            "severity": self.severity or 0,
            "created_at": self.created_at.isoformat(),
        }


class Theme(BaseNode):
    """A recurring theme or concept in stories."""
    name: str = Field(..., description="Theme name")
    description: str = Field(..., description="What this theme represents")
    category: str = Field(
        ...,
        description="Theme category (e.g., 'innovation', 'risk', 'collaboration')"
    )

    # Usage
    story_count: int = Field(default=0, description="Number of stories with this theme")
    groups_using: List[str] = Field(
        default_factory=list,
        description="Groups that frequently use this theme"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "story_count": self.story_count,
            "created_at": self.created_at.isoformat(),
        }


class Decision(BaseNode):
    """A key decision point in a narrative."""
    name: str = Field(..., description="Decision name")
    description: str = Field(..., description="What was decided")
    timestamp: datetime = Field(..., description="When the decision was made")

    # Decision details
    decision_makers: List[str] = Field(
        default_factory=list,
        description="Person IDs who made the decision"
    )
    options_considered: List[str] = Field(
        default_factory=list,
        description="Alternatives that were considered"
    )
    rationale: Optional[str] = Field(None, description="Why this decision was made")

    # Outcome
    outcome: Optional[str] = Field(None, description="What resulted")
    success: Optional[bool] = Field(None, description="Whether it was successful")

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "rationale": self.rationale or "",
            "outcome": self.outcome or "",
            "success": self.success if self.success is not None else None,
            "created_at": self.created_at.isoformat(),
        }


class Outcome(BaseNode):
    """A result or consequence in a narrative."""
    description: str = Field(..., description="What resulted")
    type: str = Field(
        ...,
        description="Outcome type (e.g., 'positive', 'negative', 'mixed', 'learning')"
    )
    impact: str = Field(..., description="Impact description")

    # Metrics
    measurable: bool = Field(default=False, description="Whether outcome is quantifiable")
    metrics: Optional[Dict[str, Any]] = Field(
        None,
        description="Quantifiable metrics if applicable"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type,
            "impact": self.impact,
            "measurable": self.measurable,
            "created_at": self.created_at.isoformat(),
        }


class Value(BaseNode):
    """An organizational value expressed in stories."""
    name: str = Field(..., description="Value name (e.g., 'Innovation', 'Integrity')")
    description: str = Field(..., description="What this value means")

    # Usage patterns
    story_count: int = Field(default=0, description="Number of stories exemplifying this value")
    groups_emphasizing: List[str] = Field(
        default_factory=list,
        description="Groups that emphasize this value"
    )

    # Expression
    typical_expressions: List[str] = Field(
        default_factory=list,
        description="How this value is typically expressed in narratives"
    )

    def to_graph_node(self) -> Dict[str, Any]:
        """Convert to Neo4j node properties."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "story_count": self.story_count,
            "created_at": self.created_at.isoformat(),
        }


class GroupPerspective(BaseModel):
    """Analysis of how a group frames a particular topic."""
    group_id: str
    group_name: str
    topic: str

    # Framing analysis
    common_themes: List[str] = Field(default_factory=list)
    typical_framing: str = Field(..., description="How this group typically frames the topic")
    values_emphasized: List[str] = Field(default_factory=list)
    example_stories: List[str] = Field(
        default_factory=list,
        description="Story IDs exemplifying this perspective"
    )


class CausalChain(BaseModel):
    """A sequence of cause-effect relationships."""
    story_id: str
    chain: List[Dict[str, str]] = Field(
        ...,
        description="Ordered sequence of cause-effect pairs"
    )

    def to_narrative(self) -> str:
        """Convert causal chain to narrative text."""
        narrative_parts = []
        for link in self.chain:
            narrative_parts.append(f"{link['cause']} led to {link['effect']}")
        return ", which ".join(narrative_parts) + "."
