# Changelog

## [0.1.2] - 2026-02-16

### Added
- `AdditionalSection` model — preserves non-standard section headers (e.g., "Fitness:",
  "Warm-Up Routine:") that don't map to canonical DrillBlock fields
- `DrillBlock.additional_sections` — list of AdditionalSection entries
- `DrillBlock.regressions` — regression/simplification variations (counterpart to progressions)

### Changed
- `SessionMetadata.title` — changed from required to optional (defaults to `None`).
  Some session plans (e.g., SFA coaching badges) have no explicit title.

## [0.1.1] - 2026-02-12

### Added
- `TrainingElements` model — coaching framework elements (Technical, Tactical,
  Physical, Social, Psychological) at the session level
- `SessionPlan.training_elements` — optional session-level training elements
- `SessionMetadata.date` — optional session date, year, or season
- `DrillBlock.author` — optional per-drill author (when different from session author)

## [0.1.0] - 2026-02-10

### Added
- Core schema: SessionPlan, SessionMetadata, DrillBlock, DrillSetup, Source
- Diagram schema: DiagramInfo, PlayerPosition, MovementArrow, EquipmentObject,
  GoalInfo, BallPosition, PitchZone, PitchView, PageAnnotation
- Tactical schema: TacticalContext, GameElement, LaneName, SituationType
- Enums: PitchViewType, ArrowType, EquipmentType
- FHIR-style Extension mechanism
- JSON Schema artifact generation
- Example session plan (nielsen)
- CI pipeline for artifact generation and documentation
