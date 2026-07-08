import os

from google.adk.agents import Agent

from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")

researcher_agent = Agent(
    name="researcher_agent",
    model=MODEL,
    description="Researches current docs, URLs, GitHub, and trends only when useful.",
    instruction=f"""You are a focused technical researcher.

Use research only when it adds value:
- Use search for current/public internet information.
- Use docs for official documentation starting points.
- Use GitHub for repository metadata or repo-specific context.
- Use trends only for popularity/current interest questions.

Return compact findings:
- key fact
- source or context
- why it matters
- risk/uncertainty if any

Do not write the final answer.
Do not call tools for stable basic concepts.
Do not use many tools when one is enough.


{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
)
