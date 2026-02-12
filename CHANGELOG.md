# Changelog

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
