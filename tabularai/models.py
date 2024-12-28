"""Models."""

from typing import Literal

from pydantic import BaseModel


class Field(BaseModel):
    """Column."""

    name: str
    definition: str | None = None
    examples: list[str] | None = None


class SheetAction(BaseModel):
    """Action."""

    action: Literal["keep", "discard"]


class RowSlice(BaseModel):
    """Row slice."""

    row_start: int
    row_end: int
