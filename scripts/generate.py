#!/usr/bin/env python3
"""Generate OSTI artifacts from Pydantic models.

Produces:
  - generated/osti.schema.json   (JSON Schema from Pydantic)
  - generated/osti.linkml.yaml   (LinkML YAML via schema-automator, optional)
"""

import json
import subprocess
import sys
from pathlib import Path

# Ensure the package is importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from osti import SCHEMA_VERSION, SessionPlan  # noqa: E402

GENERATED = ROOT / "generated"


def generate_json_schema() -> Path:
    """Export Pydantic JSON Schema to generated/osti.schema.json."""
    GENERATED.mkdir(exist_ok=True)

    schema = SessionPlan.model_json_schema()
    schema["$id"] = f"https://karstenskyt.github.io/osti/v{SCHEMA_VERSION}/schema.json"
    schema["title"] = "OSTI SessionPlan"
    schema["description"] = (
        f"Open Standard for Training Interoperability v{SCHEMA_VERSION} — "
        "FHIR-inspired schema for soccer/football session plans."
    )

    out = GENERATED / "osti.schema.json"
    out.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    print(f"  JSON Schema -> {out}")
    return out


def generate_linkml_yaml(json_schema_path: Path) -> Path | None:
    """Convert JSON Schema to LinkML YAML using schema-automator (optional)."""
    out = GENERATED / "osti.linkml.yaml"
    try:
        subprocess.run(
            [
                sys.executable, "-m", "schema_automator.importers.json_schema_import",
                str(json_schema_path),
                "-o", str(out),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"  LinkML YAML -> {out}")
        return out
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"  LinkML YAML -- skipped ({exc.__class__.__name__})")
        print("  Install with: pip install osti[dev]")
        return None


def main() -> None:
    print(f"OSTI v{SCHEMA_VERSION} -- Artifact Generation")
    print("=" * 50)
    json_schema = generate_json_schema()
    generate_linkml_yaml(json_schema)
    print("Done.")


if __name__ == "__main__":
    main()
