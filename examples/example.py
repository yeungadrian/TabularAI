from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel


class Settings(BaseModel):
    filename: str = "tests/data/msft.xlsx"
    base_url: str = "http://localhost:1234/v1"
    api_key: str = "lm-studio"


def main():
    settings = Settings()
    OpenAI(base_url=settings.base_url, api_key=settings.api_key)

    with Path("tabularai/prompts/sheet_template.md").open() as f:
        sheet_template = f.read()

    sheet_template.format("asd", "Asd")

    # completion = client.beta.chat.completions.parse(
    #     model="llama3.2-3b",
    #     messages=[
    #         {"role": "user", "content": sheet_prompt},
    #     ],
    #     response_format=SheetAction,
    # )

    # event = completion.choices[0].message.parsed


if __name__ == "__main__":
    main()
