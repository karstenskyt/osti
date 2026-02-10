"""Tests that validate example JSON files against OSTI models."""

import json
from pathlib import Path

import pytest

from osti import SessionPlan

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def _example_files():
    """Collect all .json files from the examples directory."""
    return sorted(EXAMPLES_DIR.glob("*.json"))


@pytest.fixture(params=_example_files(), ids=lambda p: p.stem)
def example_path(request):
    return request.param


def test_example_validates(example_path: Path):
    """Each example JSON must validate against the SessionPlan model."""
    data = json.loads(example_path.read_text(encoding="utf-8"))
    plan = SessionPlan.model_validate(data)
    assert plan.metadata.title
    assert plan.source.filename


def test_example_round_trip(example_path: Path):
    """Load → dump → reload must be lossless (except generated fields like id)."""
    data = json.loads(example_path.read_text(encoding="utf-8"))
    plan = SessionPlan.model_validate(data)
    json_str = plan.model_dump_json()
    reparsed = SessionPlan.model_validate_json(json_str)
    assert reparsed.metadata.title == plan.metadata.title
    assert len(reparsed.drills) == len(plan.drills)
    for orig, rp in zip(plan.drills, reparsed.drills):
        assert orig.name == rp.name


def test_nielsen_has_three_drills():
    """Nielsen example should have exactly 3 drills."""
    path = EXAMPLES_DIR / "nielsen.json"
    if not path.exists():
        pytest.skip("nielsen.json not found")
    data = json.loads(path.read_text(encoding="utf-8"))
    plan = SessionPlan.model_validate(data)
    assert len(plan.drills) == 3


def test_nielsen_drill_types():
    """Nielsen drills should have specific drill_type values."""
    path = EXAMPLES_DIR / "nielsen.json"
    if not path.exists():
        pytest.skip("nielsen.json not found")
    data = json.loads(path.read_text(encoding="utf-8"))
    plan = SessionPlan.model_validate(data)
    types = [d.drill_type for d in plan.drills]
    assert types == ["Technical Drill", "Game-Related Practice", "Phase of Play"]
