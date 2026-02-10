"""FHIR-style extension mechanism for custom data."""

from typing import Optional

from pydantic import BaseModel, Field


class Extension(BaseModel):
    """FHIR-style extension for custom data.

    Allows consumers to attach additional structured data to any OSTI
    resource without modifying the core schema. Pick the value field
    that matches the data type (only one should be set per extension).
    """

    url: str = Field(
        ..., description="URI identifying the extension definition"
    )
    name: Optional[str] = Field(
        None, description="Human-readable extension name"
    )
    value_string: Optional[str] = None
    value_integer: Optional[int] = None
    value_float: Optional[float] = None
    value_boolean: Optional[bool] = None
    value_object: Optional[dict] = None
