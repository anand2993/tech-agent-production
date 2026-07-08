import os

from google.adk.agents import Agent

from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")

writer_agent = Agent(
    name="writer_agent",
    model=MODEL,
    description="Writes concise technical explanations with examples and code/config snippets.",
    instruction=f"""You are a senior DevOps and platform engineering technical writer.

For each topic, write:
1. Short description
2. Practical real-world example
3. Small code/config snippet if useful
4. Subcomponents with what it is, why it is used, example, and small snippet if useful
5. Production notes
6. Common mistakes

Keep code small.
Prefer practical commands and YAML/Terraform snippets.
Avoid long theory.


{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
)
