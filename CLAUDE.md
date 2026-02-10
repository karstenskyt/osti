# OSTI -- Project Instructions

## Testing

Run tests using the project virtual environment:

```bash
# Windows
.venv\Scripts\python -m pytest tests/ -v

# Linux / macOS
.venv/bin/python -m pytest tests/ -v
```

## Virtual Environment

```bash
.venv\Scripts\pip install -e ".[dev]"   # Windows
```

## Code Style

- Pydantic V2 models are the source of truth
- All new Optional fields must default to `None`
- Coordinates use the 0-100 normalized (Opta) system
- Enum values are lowercase strings (except GameElement and SituationType which use Title Case for backward compatibility)

## Architecture

- `src/osti/session_plan.py` -- Core schema (SessionPlan, DrillBlock, DiagramInfo, etc.)
- `src/osti/tactical.py` -- Tactical models (TacticalContext, GameElement, LaneName, etc.)
- `src/osti/extensions.py` -- FHIR-style Extension type
- `src/osti/__init__.py` -- Public API surface
- `scripts/generate.py` -- Artifact generation (JSON Schema + LinkML YAML)
- `examples/` -- Reference session plans
- `tests/` -- Pytest suite (models, examples, extensions)
- `generated/` -- CI-generated artifacts (gitignored)

## Schema Version

SCHEMA_VERSION in `src/osti/session_plan.py` is the single source of truth.
Also mirrored in `pyproject.toml` `version` and `__init__.py` `__version__`.
All three must stay in sync.
