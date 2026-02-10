"""Tests for the FHIR-style extension mechanism."""

from osti import DiagramInfo, DrillBlock, Extension, SessionMetadata, SessionPlan, Source


def test_extension_string_value():
    """Extension with a string value."""
    ext = Extension(url="https://example.com/ext/video-url", value_string="https://youtube.com/watch?v=123")
    assert ext.url == "https://example.com/ext/video-url"
    assert ext.value_string == "https://youtube.com/watch?v=123"
    assert ext.value_integer is None


def test_extension_integer_value():
    """Extension with an integer value."""
    ext = Extension(url="https://example.com/ext/player-age", value_integer=16)
    assert ext.value_integer == 16


def test_extension_float_value():
    """Extension with a float value."""
    ext = Extension(url="https://example.com/ext/xg", value_float=0.85)
    assert ext.value_float == 0.85


def test_extension_boolean_value():
    """Extension with a boolean value."""
    ext = Extension(url="https://example.com/ext/verified", value_boolean=True)
    assert ext.value_boolean is True


def test_extension_object_value():
    """Extension with a complex object value."""
    ext = Extension(
        url="https://example.com/ext/gps-data",
        name="GPS Tracking",
        value_object={"total_distance_m": 5200, "top_speed_kmh": 28.5},
    )
    assert ext.value_object["total_distance_m"] == 5200
    assert ext.name == "GPS Tracking"


def test_extension_on_session_plan():
    """Extensions on a SessionPlan survive round-trip."""
    plan = SessionPlan(
        metadata=SessionMetadata(title="Extension Test"),
        source=Source(filename="test.pdf"),
        extensions=[
            Extension(url="https://example.com/ext/club", value_string="FC Test"),
        ],
    )
    json_str = plan.model_dump_json()
    reparsed = SessionPlan.model_validate_json(json_str)
    assert len(reparsed.extensions) == 1
    assert reparsed.extensions[0].value_string == "FC Test"


def test_extension_on_drill_block():
    """Extensions on a DrillBlock survive round-trip."""
    drill = DrillBlock(
        name="Ext Drill",
        extensions=[
            Extension(url="https://example.com/ext/intensity", value_integer=8),
        ],
    )
    json_str = drill.model_dump_json()
    reparsed = DrillBlock.model_validate_json(json_str)
    assert reparsed.extensions[0].value_integer == 8


def test_extension_on_diagram_info():
    """Extensions on DiagramInfo survive round-trip."""
    diagram = DiagramInfo(
        description="Test diagram",
        extensions=[
            Extension(url="https://example.com/ext/quality-score", value_float=0.92),
        ],
    )
    json_str = diagram.model_dump_json()
    reparsed = DiagramInfo.model_validate_json(json_str)
    assert reparsed.extensions[0].value_float == 0.92
