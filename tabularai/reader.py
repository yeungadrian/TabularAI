"""Convert excel files to markdown."""

import re
from typing import IO

from python_calamine import CalamineWorkbook
from tabulate import tabulate


def convert_excel(file: str | IO[bytes]) -> str:
    """Partition an excel workbook."""
    workbook = CalamineWorkbook.from_object(file)  # type: ignore
    markdown = ""
    for sheet_name in workbook.sheet_names:
        calamine_sheet = workbook.get_sheet_by_name(sheet_name)
        tabular_data = calamine_sheet.to_python()
        tabular_data = [[re.sub(r"\s+", " ", str(j)).strip() for j in i] for i in tabular_data]
        markdown += f"## Sheet: {sheet_name}\n\n"
        markdown += (
            tabulate(
                tabular_data,
                headers="firstrow",
            )
            + "\n\n"
        )
    return markdown.strip()
