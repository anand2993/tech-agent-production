import os

from google.adk.agents import Agent

from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")

reviewer_agent = Agent(
    name="reviewer_agent",
    model=MODEL,
    description="Reviews technical accuracy, security, and production readiness.",
    instruction=f"""You are a strict technical reviewer.

Check answers for:
1. technical correctness
2. missing assumptions
3. security issues
4. cloud production readiness
5. overly long wording
6. missing commands or config
7. unsafe secret handling
8. incorrect DevOps terminology

Return specific improvements only, or say: Looks good.


{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
)
