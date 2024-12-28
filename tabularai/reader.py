"""Convert excel files to markdown."""

import re
from datetime import date, datetime, time, timedelta
from typing import IO

from pydantic import BaseModel
from python_calamine import CalamineWorkbook
from tabulate import tabulate

from tabularai.settings import Settings


class Sheet(BaseModel):
    """Aasd."""

    sheet_name: str
    data: list[list[int | float | str | bool | time | date | datetime | timedelta]]
    markdown: str


def convert_excel(file: str | IO[bytes], settings: Settings | None = None) -> list[Sheet]:
    """Convert an excel workbook into markdown."""
    if settings is None:
        settings = Settings()

    workbook = CalamineWorkbook.from_object(file)  # type: ignore

    sheets: list[Sheet] = []
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python(skip_empty_area=settings.skip_empty_area)
        markdown = f"## Sheet: {sheet_name}\n\n"
        markdown += tabulate(
            [[re.sub(r"\s+", " ", str(j)).strip() for j in i] for i in tabular_data],
            headers="firstrow",
            tablefmt=settings.tablefmt,
            showindex=settings.showindex,
        )
        sheets.append(Sheet(sheet_name=sheet_name, data=tabular_data, markdown=markdown))
    return sheets
