"""OSTI — Open Standard for Training Interoperability.

FHIR-inspired schema for soccer/football session plans.
"""

from osti.extensions import Extension
from osti.session_plan import (
    SCHEMA_VERSION,
    ArrowType,
    BallPosition,
    DiagramInfo,
    DrillBlock,
    DrillSetup,
    EquipmentObject,
    EquipmentType,
    GoalInfo,
    MovementArrow,
    PageAnnotation,
    PitchView,
    PitchViewType,
    PitchZone,
    PlayerPosition,
    SessionMetadata,
    SessionPlan,
    Source,
)
from osti.tactical import (
    GameElement,
    LaneName,
    SituationType,
    TacticalContext,
)

__version__ = SCHEMA_VERSION

__all__ = [
    # Core
    "SessionPlan",
    "SessionMetadata",
    "DrillBlock",
    "DrillSetup",
    "Source",
    # Diagram
    "DiagramInfo",
    "PlayerPosition",
    "MovementArrow",
    "EquipmentObject",
    "GoalInfo",
    "BallPosition",
    "PitchZone",
    "PitchView",
    "PageAnnotation",
    # Enums
    "PitchViewType",
    "ArrowType",
    "EquipmentType",
    # Tactical
    "TacticalContext",
    "GameElement",
    "LaneName",
    "SituationType",
    # Extensions
    "Extension",
    # Version
    "SCHEMA_VERSION",
]
