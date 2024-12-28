from typing import Literal

import rich
from openai import OpenAI
from pydantic import BaseModel
from tabulate import tabulate

from tabularai.reader import convert_excel

filename = "tests/data/msft.xlsx"
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class Field(BaseModel):
    """Column."""

    name: str
    definition: str | None = None
    examples: list[str] | None = None


class SheetAction(BaseModel):
    """Action."""

    action: Literal["keep", "discard"]


class RowSlice(BaseModel):
    """Aasd."""

    row_start: int
    row_end: int


sheets = convert_excel(filename)
_fields = [
    {
        "name": "Total cost of revenue",
    },
    {"name": "Total revenue"},
    {"name": "Operating income"},
]
fields = [Field.model_validate(i) for i in _fields]
formatted_fields = "\n- " + "\n- ".join([i["name"] for i in _fields])


events = []
for i in sheets:
    sheet_prompt = f"""
    You are required to attempt to produce a clean table with the following rows:
    {formatted_fields}

    The columns should be:
    - Twelve Months Ended June 2023
    - Twelve Months Ended June 2024		

    Here is a single sheet from an excel file:
    {i.markdown}

    
    Should the sheet be kept or discarded to build the required data?"""
    completion = client.beta.chat.completions.parse(
        model="llama3.2-3b",
        messages=[
            {"role": "user", "content": sheet_prompt},
        ],
        response_format=SheetAction,
    )

    event = completion.choices[0].message.parsed
    events.append(event)

print(events)


# the_sheet = sheets[2]

# sheet_prompt = f"""You are required to produce a clean table with the following rows:
# {formatted_fields}

# The columns should be:
# - FY 2022
# - FY 2023

# We will apply the following transformations to clean the dataframe:
# - slice rows
# - slice columns
# - insert data into cells
# - rename columns

# Here is the dataframe we are transforming represented in a markdown table:
# {the_sheet.markdown}

# The first step is to slice rows. What rows should be kept. Please output the range of row indices to keep.
# """
# completion = client.beta.chat.completions.parse(
#     model="llama3.2-3b",
#     messages=[
#         {"role": "user", "content": sheet_prompt},
#     ],
#     response_format=RowSlice,
#     temperature=0.0
# )

# print(completion.choices[0].message.parsed)

# print([the_sheet.data[4:7]])


# sheet_prompt_2 = f"""You are required to produce a clean table with the following rows:
# {formatted_fields}

# The columns should be:
# - FY 2022
# - FY 2023

# We will apply the following transformations to clean the dataframe:
# - slice rows
# - slice columns
# - insert data into cells
# - rename columns

# Here is the dataframe we are transforming represented in a markdown table:
# {the_sheet.markdown}

# The suggested slice applied was:
# {
#     "row_start": 4,
#     "row_end": 6
# }

# This produced:

# """