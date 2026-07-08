import os

from google.adk.agents import Agent

from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")

quiz_agent = Agent(
    name="quiz_agent",
    model=MODEL,
    description="Creates interview questions, quizzes, and hands-on tasks.",
    instruction=f"""You create practical interview and learning exercises.

For a topic, provide:
1. 5 interview questions
2. 3 hands-on tasks
3. 3 troubleshooting scenarios
4. Short expected answers

Focus on DevOps, Cloud, Kubernetes, Terraform, APIs, CI/CD, and platform engineering.


{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
)
