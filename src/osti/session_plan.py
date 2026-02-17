"""Pydantic models for soccer session plan extraction.

This is the canonical OSTI (Open Standard for Training Interoperability)
schema. All session plan data should conform to these models.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .extensions import Extension
from .tactical import TacticalContext

SCHEMA_VERSION = "0.1.2"
"""Current OSTI schema version (SemVer)."""


# --- Enriched diagram enums ---


class PitchViewType(str, Enum):
    """What portion of the pitch is shown in the diagram."""

    FULL_PITCH = "full_pitch"
    HALF_PITCH = "half_pitch"
    PENALTY_AREA = "penalty_area"
    THIRD = "third"
    BETWEEN_HALF_AND_FULL = "between_half_and_full"
    CUSTOM = "custom"


class ArrowType(str, Enum):
    """Classification of movement arrows in diagrams."""

    RUN = "run"
    PASS = "pass"
    SHOT = "shot"
    DRIBBLE = "dribble"
    CROSS = "cross"
    THROUGH_BALL = "through_ball"
    MOVEMENT = "movement"


class EquipmentType(str, Enum):
    """Types of training equipment shown in diagrams."""

    CONE = "cone"
    MANNEQUIN = "mannequin"
    POLE = "pole"
    GATE = "gate"
    HURDLE = "hurdle"
    MINI_GOAL = "mini_goal"
    FULL_GOAL = "full_goal"
    AIR_BODY = "air_body"
    FLAG = "flag"


# --- Enriched diagram models ---


class PitchView(BaseModel):
    """Pitch dimensions and view type for the diagram."""

    view_type: PitchViewType = Field(
        PitchViewType.HALF_PITCH, description="What part of pitch is shown"
    )
    length_meters: Optional[float] = Field(
        None, description="Length of visible area in meters"
    )
    width_meters: Optional[float] = Field(
        None, description="Width of visible area in meters"
    )
    orientation: str = Field(
        "vertical", description="Orientation: 'vertical' or 'horizontal'"
    )


class MovementArrow(BaseModel):
    """A structured movement arrow on the diagram."""

    start_x: float = Field(..., description="Start X coordinate (0-100)")
    start_y: float = Field(..., description="Start Y coordinate (0-100)")
    end_x: float = Field(..., description="End X coordinate (0-100)")
    end_y: float = Field(..., description="End Y coordinate (0-100)")
    arrow_type: ArrowType = Field(
        ArrowType.MOVEMENT, description="Type of movement"
    )
    from_label: Optional[str] = Field(
        None, description="Label of the player/object at arrow start"
    )
    to_label: Optional[str] = Field(
        None, description="Label of the player/object at arrow end"
    )
    sequence_number: Optional[int] = Field(
        None, description="Order in the drill sequence"
    )
    label: Optional[str] = Field(
        None, description="Text label on the arrow"
    )


class EquipmentObject(BaseModel):
    """A piece of equipment placed on the diagram."""

    equipment_type: EquipmentType = Field(
        ..., description="Type of equipment"
    )
    x: float = Field(..., description="X coordinate (0-100)")
    y: float = Field(..., description="Y coordinate (0-100)")
    x2: Optional[float] = Field(
        None, description="End X for gates/lines (0-100)"
    )
    y2: Optional[float] = Field(
        None, description="End Y for gates/lines (0-100)"
    )
    label: Optional[str] = Field(None, description="Text label")
    color: Optional[str] = Field(None, description="Color of equipment")


class GoalInfo(BaseModel):
    """A goal on the diagram."""

    x: float = Field(..., description="X center coordinate (0-100)")
    y: float = Field(..., description="Y center coordinate (0-100)")
    goal_type: str = Field(
        "full_goal", description="'full_goal', 'mini_goal', or 'target_goal'"
    )
    width_meters: Optional[float] = Field(
        None, description="Goal width in meters"
    )


class BallPosition(BaseModel):
    """A ball position on the diagram."""

    x: float = Field(..., description="X coordinate (0-100)")
    y: float = Field(..., description="Y coordinate (0-100)")
    label: Optional[str] = Field(None, description="Text label")


class PitchZone(BaseModel):
    """A marked zone or area on the diagram."""

    zone_type: str = Field(
        "area", description="Zone type (e.g., 'area', 'channel', 'box')"
    )
    x1: float = Field(..., description="Top-left X coordinate (0-100)")
    y1: float = Field(..., description="Top-left Y coordinate (0-100)")
    x2: float = Field(..., description="Bottom-right X coordinate (0-100)")
    y2: float = Field(..., description="Bottom-right Y coordinate (0-100)")
    label: Optional[str] = Field(None, description="Zone label")
    color: Optional[str] = Field(None, description="Zone color")


class PlayerPosition(BaseModel):
    """Position of a player on the pitch diagram."""

    label: str = Field(..., description="Player label (e.g., 'GK', 'A1', 'D1')")
    x: float = Field(..., description="X coordinate (0-100, left to right)")
    y: float = Field(..., description="Y coordinate (0-100, bottom to top)")
    role: Optional[str] = Field(
        None, description="Role description (e.g., 'goalkeeper', 'attacker')"
    )
    color: Optional[str] = Field(
        None, description="Marker color (e.g., 'red', 'green', 'blue', 'yellow')"
    )


class DiagramInfo(BaseModel):
    """Information extracted from a drill diagram."""

    image_ref: Optional[str] = Field(
        None, description="Path or URI to the diagram image"
    )
    description: str = Field(
        "", description="Human-readable description of the diagram"
    )
    player_positions: list[PlayerPosition] = Field(
        default_factory=list, description="Player positions extracted from diagram"
    )
    pitch_view: Optional[PitchView] = Field(
        None, description="Pitch view type and dimensions"
    )
    arrows: list[MovementArrow] = Field(
        default_factory=list, description="Structured movement arrows"
    )
    equipment: list[EquipmentObject] = Field(
        default_factory=list, description="Equipment objects on the diagram"
    )
    goals: list[GoalInfo] = Field(
        default_factory=list, description="Goals on the diagram"
    )
    balls: list[BallPosition] = Field(
        default_factory=list, description="Ball positions on the diagram"
    )
    zones: list[PitchZone] = Field(
        default_factory=list, description="Marked zones on the diagram"
    )
    extensions: list[Extension] = Field(
        default_factory=list, description="FHIR-style extensions for custom data"
    )


class PageAnnotation(BaseModel):
    """Annotation for a single page that may contain 0, 1, or multiple diagrams."""

    page_description: str = Field(
        "", description="Brief description of the page content"
    )
    has_diagram: bool = Field(
        False, description="Whether the page contains any soccer diagram"
    )
    diagrams: list[DiagramInfo] = Field(
        default_factory=list,
        description="List of diagrams found on this page (empty if none)",
    )


class DrillSetup(BaseModel):
    """Setup information for a drill block."""

    description: str = Field("", description="Setup description text")
    player_count: Optional[str] = Field(
        None,
        description="Number/description of players (e.g., '1 GK + 6 field players')",
    )
    equipment: list[str] = Field(
        default_factory=list, description="Required equipment"
    )
    area_dimensions: Optional[str] = Field(
        None, description="Playing area dimensions (e.g., '20x15 yards')"
    )


class AdditionalSection(BaseModel):
    """A drill section with a non-standard header that doesn't map to a canonical field.

    Used when the source document contains section headers (e.g., "Fitness:",
    "Warm-Up Routine:") that aren't recognized as standard OSTI fields
    (setup, sequence, rules, scoring, coaching_points, progressions).
    The original header text is preserved as the title.
    """

    title: str = Field(..., description="Original section header text as found in the source")
    content: list[str] = Field(
        default_factory=list, description="Section content as list items"
    )


class DrillBlock(BaseModel):
    """A single drill/exercise within a session plan."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Drill name (e.g., 'Coach-Goalkeeper(s)')")
    setup: DrillSetup = Field(default_factory=DrillSetup)
    diagram: DiagramInfo = Field(default_factory=DiagramInfo)
    sequence: list[str] = Field(
        default_factory=list, description="Numbered execution steps"
    )
    rules: list[str] = Field(
        default_factory=list, description="Rules and constraints"
    )
    scoring: list[str] = Field(
        default_factory=list, description="Scoring criteria"
    )
    coaching_points: list[str] = Field(
        default_factory=list, description="Key coaching observations"
    )
    progressions: list[str] = Field(
        default_factory=list, description="Progression variations"
    )
    regressions: list[str] = Field(
        default_factory=list, description="Regression / simplification variations"
    )
    author: Optional[str] = Field(
        None, description="Author or coach for this drill (when different from session author)"
    )
    drill_type: Optional[str] = Field(
        None,
        description="Practice structure (e.g., 'Warm-Up', 'Technical Drill', "
        "'Game-Related Practice', 'Small-Sided Game', 'Phase of Play')",
    )
    directional: Optional[bool] = Field(
        None, description="Whether the drill has a primary direction of attack"
    )
    additional_sections: list[AdditionalSection] = Field(
        default_factory=list,
        description="Sections with non-standard headers not mapped to canonical fields",
    )
    tactical_context: Optional[TacticalContext] = Field(
        None, description="Tactical methodology context"
    )
    extensions: list[Extension] = Field(
        default_factory=list, description="FHIR-style extensions for custom data"
    )


class TrainingElements(BaseModel):
    """Coaching framework elements (Technical, Tactical, Physical, Social, Psychological).

    All five categories are optional to accommodate plans that combine
    Social and Psychological into a single "Psycho-Social" category,
    or omit categories entirely.
    """

    technical: list[str] = Field(
        default_factory=list, description="Technical skills and techniques"
    )
    tactical: list[str] = Field(
        default_factory=list, description="Tactical awareness and game understanding"
    )
    physical: list[str] = Field(
        default_factory=list, description="Physical attributes and demands"
    )
    social: list[str] = Field(
        default_factory=list, description="Social and communication skills"
    )
    psychological: list[str] = Field(
        default_factory=list, description="Psychological and mental attributes"
    )


class SessionMetadata(BaseModel):
    """Metadata about a session plan."""

    title: Optional[str] = Field(None, description="Session plan title")
    category: Optional[str] = Field(
        None, description="Category (e.g., 'Goalkeeping: General')"
    )
    difficulty: Optional[str] = Field(
        None, description="Difficulty level (e.g., 'Moderate')"
    )
    date: Optional[str] = Field(
        None,
        description="Session date, year, or season (e.g., '2023', '2023/24', 'Spring 2024')",
    )
    author: Optional[str] = Field(None, description="Author or organization")
    target_age_group: Optional[str] = Field(None, description="Target age group")
    duration_minutes: Optional[int] = Field(
        None, description="Session duration in minutes"
    )
    desired_outcome: Optional[str] = Field(
        None,
        description="Session-level learning objective or desired outcome",
    )


class Source(BaseModel):
    """Source document information."""

    filename: str = Field(..., description="Original PDF filename")
    page_count: int = Field(0, description="Number of pages in source PDF")
    extraction_timestamp: Optional[datetime] = Field(
        None, description="When the extraction was performed"
    )


class SessionPlan(BaseModel):
    """Complete extracted session plan — the root OSTI resource."""

    id: UUID = Field(default_factory=uuid4)
    metadata: SessionMetadata
    drills: list[DrillBlock] = Field(
        default_factory=list, description="Drill blocks in order"
    )
    training_elements: Optional[TrainingElements] = Field(
        None,
        description="Session-level coaching framework elements "
        "(Technical, Tactical, Physical, Social, Psychological)",
    )
    source: Source
    extensions: list[Extension] = Field(
        default_factory=list, description="FHIR-style extensions for custom data"
    )
