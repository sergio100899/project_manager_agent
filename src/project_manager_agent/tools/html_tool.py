from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import re


class CleanHTMLToolInput(BaseModel):
    raw_text: str = Field(
        ...,
        description="Raw content of the file that contains <html>...</html>.",
    )


class CleanHTMLTool(BaseTool):
    name: str = "clean_html_tool"
    description: str = """Extract and retain **only all** the content that is inside <html>...</html> tags.
        If there are multiple HTML sections in the file, keep them all intact.
        Remove absolutely everything that is outside any <html> tag."""
    args_schema: Type[BaseModel] = CleanHTMLToolInput

    def _run(self, raw_text: str) -> str:
        html_blocks = re.findall(r"<html[\s\S]*?<\/html>", raw_text, re.IGNORECASE)

        if not html_blocks:
            return "No content found inside <html> tags."

        return "\n\n".join(html_blocks)
