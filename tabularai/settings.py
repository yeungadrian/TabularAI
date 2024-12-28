"""Settings for markdown conversion."""

from pydantic import BaseModel, field_validator
from tabulate import tabulate_formats


class Settings(BaseModel):
    """Tabular settings."""

    skip_empty_area: bool = True
    tablefmt: str = "github"
    showindex: bool = True

    @field_validator("tablefmt")
    def validate_tablefmt(cls, v: str) -> str:
        """Validate tablefmt."""
        assert v in tabulate_formats
        return v