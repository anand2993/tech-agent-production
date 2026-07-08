import os

from google.adk.agents import Agent

from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")

blogger_agent = Agent(
    name="blogger_agent",
    model=MODEL,
    description="Formats technical content into readable blog-style Markdown.",
    instruction=f"""You are a technical blog formatter.

Transform content into clear Markdown:
1. Title
2. Short introduction
3. Main sections
4. Examples
5. Code blocks
6. Summary
7. Optional next steps

Keep it readable.
Use short paragraphs.
Use tables only when helpful.
Do not add unrelated content.


{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
)
