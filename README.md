# OSTI -- Open Standard for Training Interoperability

A FHIR-inspired schema for soccer/football session plans. OSTI provides a
single, versioned source of truth for representing training sessions, drill
diagrams, player positions, tactical context, and equipment layouts.

> Open [architecture.html](architecture.html) in a browser to explore the C4
> architecture diagrams (System Context, Container, Component, Dynamic).

## Installation

```bash
# From GitHub (current)
pip install git+https://github.com/karstenskyt/osti.git

# From a specific version
pip install git+https://github.com/karstenskyt/osti.git@v0.1.2

# Local development
git clone https://github.com/karstenskyt/osti.git
cd osti
pip install -e ".[dev]"
```

## Quick Start

```python
import json
from osti import SessionPlan, SCHEMA_VERSION

# Validate a session plan JSON file
with open("session.json", encoding="utf-8") as f:
    plan = SessionPlan.model_validate(json.load(f))

print(f"Schema v{SCHEMA_VERSION}: {plan.metadata.title}")
print(f"  {len(plan.drills)} drills")
```

## Schema Overview

| Resource | Description |
|----------|-------------|
| `SessionPlan` | Root resource -- a complete training session |
| `SessionMetadata` | Title, author, category, difficulty, duration |
| `DrillBlock` | A single drill/exercise with setup, sequence, coaching points |
| `DrillSetup` | Player count, equipment, area dimensions |
| `AdditionalSection` | Non-standard section header with content (e.g., "Fitness:") |
| `DiagramInfo` | Diagram with player positions, arrows, equipment, zones |
| `PlayerPosition` | Player marker on the pitch (x, y, label, role, color) |
| `MovementArrow` | Movement/pass/shot arrow between positions |
| `EquipmentObject` | Training equipment (cones, mannequins, goals, etc.) |
| `GoalInfo` | Goal placement on the diagram |
| `BallPosition` | Ball position marker |
| `PitchZone` | Marked area/channel on the pitch |
| `PitchView` | Pitch dimensions and orientation |
| `PageAnnotation` | Page-level annotation for multi-diagram documents |
| `TacticalContext` | Tactical methodology (game elements, lanes, phases) |
| `TrainingElements` | Coaching framework elements (Technical, Tactical, Physical, Social, Psychological) |
| `Source` | Source document metadata |
| `Extension` | FHIR-style extension for custom data |

All coordinates use the **0-100 normalized (Opta) system**.

## Example

See [`examples/nielsen.json`](examples/nielsen.json) for a complete 3-drill
goalkeeping session plan with full diagram data.

## Extension Mechanism

OSTI uses a FHIR-inspired extension model. Custom data can be attached to
`SessionPlan`, `DrillBlock`, and `DiagramInfo` without modifying the core schema:

```python
from osti import SessionPlan, Extension

plan = SessionPlan(
    metadata=...,
    source=...,
    extensions=[
        Extension(url="https://example.com/ext/club", value_string="FC Example"),
        Extension(url="https://example.com/ext/gps", value_object={"distance_m": 5200}),
    ],
)
```

## Versioning

OSTI follows [SemVer](https://semver.org/):

- **Patch** (0.1.x): Bug fixes, documentation updates
- **Minor** (0.x.0): New optional fields, new models, new enum values
- **Major** (x.0.0): Breaking changes to existing fields/types

The extension mechanism is the "escape valve" -- custom data via extensions avoids
the need for major version bumps.

## Artifact Generation

```bash
python scripts/generate.py
```

Produces:
- `generated/osti.schema.json` -- JSON Schema (from Pydantic)
- `generated/osti.linkml.yaml` -- LinkML YAML (requires `pip install osti[dev]`)

## License

[MIT](LICENSE)
