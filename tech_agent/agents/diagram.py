import os

from google.adk.agents import Agent

from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")

diagram_agent = Agent(
    name="diagram_agent",
    model=MODEL,
    description="Creates compact Mermaid diagrams for architecture and flow.",
    instruction=f"""You create Mermaid diagrams for technical architecture.

Preferred formats:
- flowchart TD
- sequenceDiagram
- graph LR

Rules:
- Keep diagrams small.
- Use clear labels.
- Do not overcomplicate.
- Provide a short explanation below the diagram.


{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
)
