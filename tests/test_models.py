"""Tests for OSTI Pydantic model validation."""

import json
from uuid import UUID

from osti import (
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


def test_schema_version():
    assert SCHEMA_VERSION == "0.1.1"


def test_session_plan_minimal():
    """Minimal valid SessionPlan."""
    plan = SessionPlan(
        metadata=SessionMetadata(title="Test Session"),
        source=Source(filename="test.pdf"),
    )
    assert plan.metadata.title == "Test Session"
    assert plan.source.filename == "test.pdf"
    assert isinstance(plan.id, UUID)
    assert plan.drills == []
    assert plan.extensions == []


def test_session_plan_round_trip():
    """Create → JSON → parse back → assert equal."""
    plan = SessionPlan(
        metadata=SessionMetadata(
            title="Round Trip Test",
            category="Testing",
            difficulty="Easy",
            author="Test Author",
            duration_minutes=60,
            desired_outcome="Verify round-trip",
        ),
        drills=[
            DrillBlock(
                name="Drill 1",
                setup=DrillSetup(
                    description="Setup desc",
                    player_count="2v2",
                    equipment=["cone", "ball"],
                    area_dimensions="20x20",
                ),
                diagram=DiagramInfo(
                    image_ref="img.png",
                    description="A drill diagram",
                    player_positions=[
                        PlayerPosition(label="A1", x=50, y=50, role="attacker", color="red"),
                    ],
                    pitch_view=PitchView(view_type=PitchViewType.HALF_PITCH),
                    arrows=[
                        MovementArrow(
                            start_x=10, start_y=20, end_x=30, end_y=40,
                            arrow_type=ArrowType.PASS, sequence_number=1,
                        ),
                    ],
                    equipment=[
                        EquipmentObject(equipment_type=EquipmentType.CONE, x=25, y=25),
                    ],
                    goals=[GoalInfo(x=50, y=100)],
                    balls=[BallPosition(x=50, y=50)],
                    zones=[PitchZone(x1=0, y1=0, x2=100, y2=50, label="Defensive Half")],
                ),
                sequence=["Step 1", "Step 2"],
                rules=["No offside"],
                scoring=["1 pt per goal"],
                coaching_points=["Stay balanced"],
                progressions=["Add defender"],
                drill_type="Small-Sided Game",
                directional=True,
                tactical_context=TacticalContext(
                    game_element=GameElement.POSITIONAL_ATTACK,
                    lanes=[LaneName.CENTRAL_CORRIDOR],
                    phase_of_play="attacking",
                    numerical_advantage="2v1",
                ),
            ),
        ],
        source=Source(filename="test.pdf", page_count=3),
    )
    json_str = plan.model_dump_json()
    parsed = SessionPlan.model_validate_json(json_str)
    assert parsed.metadata.title == plan.metadata.title
    assert len(parsed.drills) == 1
    assert parsed.drills[0].name == "Drill 1"
    assert parsed.drills[0].diagram.player_positions[0].label == "A1"
    assert parsed.drills[0].tactical_context.game_element == GameElement.POSITIONAL_ATTACK


def test_optional_fields_default_none():
    """All Optional fields on metadata default to None."""
    meta = SessionMetadata(title="Defaults")
    assert meta.category is None
    assert meta.difficulty is None
    assert meta.author is None
    assert meta.target_age_group is None
    assert meta.duration_minutes is None
    assert meta.desired_outcome is None


def test_source_no_default_timestamp():
    """Source.extraction_timestamp is None by default (consumers set it)."""
    src = Source(filename="test.pdf")
    assert src.extraction_timestamp is None


def test_all_pitch_view_types():
    """All PitchViewType enum values are valid."""
    for vt in PitchViewType:
        pv = PitchView(view_type=vt)
        assert pv.view_type == vt


def test_all_arrow_types():
    """All ArrowType enum values are valid."""
    for at in ArrowType:
        arrow = MovementArrow(start_x=0, start_y=0, end_x=100, end_y=100, arrow_type=at)
        assert arrow.arrow_type == at


def test_all_equipment_types():
    """All EquipmentType enum values are valid."""
    for et in EquipmentType:
        eq = EquipmentObject(equipment_type=et, x=50, y=50)
        assert eq.equipment_type == et


def test_all_game_elements():
    """All GameElement enum values are valid."""
    for ge in GameElement:
        tc = TacticalContext(game_element=ge)
        assert tc.game_element == ge


def test_all_lane_names():
    """All LaneName enum values are valid."""
    for ln in LaneName:
        tc = TacticalContext(lanes=[ln])
        assert ln in tc.lanes


def test_all_situation_types():
    """All SituationType enum values are valid."""
    for st in SituationType:
        tc = TacticalContext(situation_type=st)
        assert tc.situation_type == st


def test_diagram_info_description_field():
    """DiagramInfo uses 'description' not 'vlm_description'."""
    d = DiagramInfo(description="A test description")
    assert d.description == "A test description"
    data = d.model_dump()
    assert "description" in data
    assert "vlm_description" not in data


def test_drill_block_extensions_default():
    """DrillBlock extensions default to empty list."""
    db = DrillBlock(name="Test")
    assert db.extensions == []


def test_training_elements_defaults():
    """TrainingElements fields default to empty lists."""
    te = TrainingElements()
    assert te.technical == []
    assert te.tactical == []
    assert te.physical == []
    assert te.social == []
    assert te.psychological == []


def test_training_elements_populated():
    """TrainingElements accepts populated lists."""
    te = TrainingElements(
        technical=["Passing", "First touch"],
        tactical=["Pressing triggers"],
        physical=["Endurance"],
        social=["Communication"],
        psychological=["Decision-making under pressure"],
    )
    assert len(te.technical) == 2
    assert "Pressing triggers" in te.tactical


def test_session_plan_training_elements():
    """SessionPlan.training_elements is optional and defaults to None."""
    plan = SessionPlan(
        metadata=SessionMetadata(title="TE Test"),
        source=Source(filename="test.pdf"),
    )
    assert plan.training_elements is None

    plan_with_te = SessionPlan(
        metadata=SessionMetadata(title="TE Test"),
        source=Source(filename="test.pdf"),
        training_elements=TrainingElements(technical=["Dribbling"]),
    )
    assert plan_with_te.training_elements is not None
    assert plan_with_te.training_elements.technical == ["Dribbling"]


def test_drill_block_author():
    """DrillBlock.author is optional and defaults to None."""
    db = DrillBlock(name="Test")
    assert db.author is None

    db_with_author = DrillBlock(name="Test", author="Coach Smith")
    assert db_with_author.author == "Coach Smith"


def test_session_metadata_date():
    """SessionMetadata.date is optional and defaults to None."""
    meta = SessionMetadata(title="Date Test")
    assert meta.date is None

    meta_with_date = SessionMetadata(title="Date Test", date="2023/24")
    assert meta_with_date.date == "2023/24"


def test_json_schema_generation():
    """JSON Schema can be generated without errors."""
    schema = SessionPlan.model_json_schema()
    assert schema["type"] == "object"
    assert "SessionMetadata" in json.dumps(schema)
