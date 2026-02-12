workspace "OSTI" "Open Standard for Training Interoperability — FHIR-inspired schema for soccer/football session plans" {

    model {
        coach = person "Coach / Analyst" "Creates and consumes soccer training session plans"
        developer = person "Developer" "Builds applications that read/write session plans"

        osti = softwareSystem "OSTI Schema Library" "Python package providing Pydantic V2 models, enums, and validators for soccer session plan data. FHIR-inspired extension mechanism." {
            publicApi = container "Public API" "Package entry point exposing all models, enums, and SCHEMA_VERSION" "Python, __init__.py"
            coreSchema = container "Core Schema" "SessionPlan, DrillBlock, DiagramInfo, TrainingElements, and 10 supporting models with 105 typed fields" "Python, Pydantic V2" {
                sessionPlan = component "SessionPlan" "Root: id, metadata, drills, elements, source, extensions" "BaseModel"
                sessionMetadata = component "SessionMetadata" "title, category, difficulty, date, author" "BaseModel"
                drillBlock = component "DrillBlock" "name, setup, diagram, coaching_points" "BaseModel"
                diagramInfo = component "DiagramInfo" "positions, arrows, equipment, goals, zones" "BaseModel"
                source = component "Source" "filename, page_count, timestamp" "BaseModel"
                playerPosition = component "PlayerPosition" "label, x, y, role, color" "BaseModel" "DiagramModel"
                movementArrow = component "MovementArrow" "coords, arrow_type, labels" "BaseModel" "DiagramModel"
                equipmentObject = component "EquipmentObject" "type, x, y, label" "BaseModel" "DiagramModel"
                arrowTypeEnum = component "ArrowType" "run, pass, shot, dribble, cross, movement" "Enum" "DiagramModel"
                equipTypeEnum = component "EquipmentType" "cone, mannequin, pole, gate, hurdle" "Enum" "DiagramModel"
            }
            tactical = container "Tactical Models" "TacticalContext, GameElement, LaneName, SituationType for Peters/Schumacher methodology" "Python, Pydantic V2" {
                tacticalContext = component "TacticalContext" "methodology, game_element, lanes, phase" "BaseModel"
                gameElement = component "GameElement" "Counter Attack, Pressing, Build-Up Play" "Enum"
            }
            extensions = container "Extension System" "FHIR-style Extension model supporting string, int, float, bool, and object payloads" "Python, Pydantic V2" {
                extension = component "Extension" "url, name, value_string/int/float/bool/object" "BaseModel"
            }
            generator = container "Artifact Generator" "scripts/generate.py — produces JSON Schema and optional LinkML YAML from Pydantic models" "Python script"
            tests = container "Test Suite" "31 tests covering models, examples, extensions, and round-trip serialization" "pytest"
        }

        consumerApp = softwareSystem "Consumer App" "Any application that imports OSTI to validate session plans" "External"
        githubPages = softwareSystem "GitHub Pages" "Hosts JSON Schema and architecture documentation" "External"
        githubReleases = softwareSystem "GitHub Releases" "Distributes versioned wheel packages" "External"
        ci = softwareSystem "GitHub Actions CI" "Runs tests, generates schema, deploys to Pages, builds wheel on tags" "External"

        # System Context relationships
        coach -> consumerApp "Uses to plan training sessions"
        consumerApp -> osti "Imports and validates against" "pip install osti"
        developer -> osti "Installs and imports" "pip install"
        osti -> githubPages "Publishes schema artifacts" "CI/CD"
        osti -> githubReleases "Publishes wheel on tag" "CI/CD"

        # Container relationships
        developer -> publicApi "from osti import SessionPlan"
        publicApi -> coreSchema "Re-exports models and enums"
        publicApi -> tactical "Re-exports TacticalContext, enums"
        publicApi -> extensions "Re-exports Extension"
        coreSchema -> tactical "Imports TacticalContext"
        coreSchema -> extensions "Imports Extension"
        generator -> coreSchema "Calls model_json_schema()"
        ci -> generator "Runs on push/tag"
        ci -> tests "Runs pytest"
        ci -> githubPages "Deploys schema + docs"
        consumerApp -> publicApi "pip install osti"

        # Component relationships
        sessionPlan -> sessionMetadata "contains"
        sessionPlan -> drillBlock "contains list"
        sessionPlan -> extension "extends via list"
        drillBlock -> diagramInfo "contains"
        drillBlock -> tacticalContext "optional"
        diagramInfo -> playerPosition "contains list"
        diagramInfo -> movementArrow "contains list"
        diagramInfo -> equipmentObject "contains list"
        movementArrow -> arrowTypeEnum "uses"
        equipmentObject -> equipTypeEnum "uses"
        tacticalContext -> gameElement "uses"
    }

    views {
        systemContext osti "SystemContext" "System Context — OSTI in the training-plan ecosystem" {
            include *
            autoLayout
        }

        container osti "Containers" "Container diagram — modules within the OSTI schema library" {
            include *
            autoLayout
        }

        component coreSchema "Components" "Component diagram — models within the Core Schema" {
            include *
            autoLayout
        }

        dynamic osti "Dynamic" "Session Plan Validation Flow" {
            developer -> publicApi "Calls SessionPlan.model_validate(data)"
            publicApi -> coreSchema "Delegates to Pydantic validation"
            coreSchema -> tactical "Validates TacticalContext and enums"
            coreSchema -> extensions "Validates Extension payloads"
            publicApi -> developer "Returns typed SessionPlan or ValidationError"
            autoLayout
        }

        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
            element "DiagramModel" {
                background #A8D0F5
                color #000000
            }
            relationship "Relationship" {
                color #707070
            }
        }
    }

}
