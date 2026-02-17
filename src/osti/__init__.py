"""OSTI — Open Standard for Training Interoperability.

FHIR-inspired schema for soccer/football session plans.
"""

from osti.extensions import Extension
from osti.session_plan import (
    SCHEMA_VERSION,
    AdditionalSection,
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
    TrainingElements,
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
    "AdditionalSection",
    "Source",
    "TrainingElements",
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
