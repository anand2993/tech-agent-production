import os

from google.adk.agents import Agent
from mcp.client.stdio import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams

from tech_agent.agents.blogger import blogger_agent
from tech_agent.agents.diagram import diagram_agent
from tech_agent.agents.planner import planner_agent
from tech_agent.agents.quiz import quiz_agent
from tech_agent.agents.researcher import researcher_agent
from tech_agent.agents.reviewer import reviewer_agent
from tech_agent.agents.writer import writer_agent
from tech_agent.shared.prompts import COMMON_SECURITY_RULES, COMMON_STYLE_RULES

MODEL = os.getenv("MODEL", "gemini-flash-latest")


def python_mcp(script_name: str) -> MCPToolset:
    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="python",
                args=[f"mcp_servers/{script_name}"],
            )
        )
    )


search_tools = python_mcp("search_server.py")
docs_tools = python_mcp("docs_server.py")
github_tools = python_mcp("github_server.py")
trends_tools = python_mcp("trends_server.py")
code_examples_tools = python_mcp("code_examples_server.py")
kubernetes_tools = python_mcp("kubernetes_server.py")
terraform_tools = python_mcp("terraform_server.py")
aws_tools = python_mcp("aws_server.py")
gcp_tools = python_mcp("gcp_server.py")
devops_tools = python_mcp("devops_server.py")

planner_agent.tools = [trends_tools]
researcher_agent.tools = [search_tools, docs_tools, github_tools, trends_tools]
writer_agent.tools = [
    code_examples_tools,
    kubernetes_tools,
    terraform_tools,
    aws_tools,
    gcp_tools,
    devops_tools,
]

root_agent = Agent(
    name="tech_content_orchestrator",
    model=MODEL,
    description="Production-style technical learning orchestrator for DevOps, Cloud, Kubernetes, Terraform, APIs, and AI agents.",
    instruction=f"""
You are the root orchestrator.

Use specialist agents logically:
1. planner_agent creates the structure.
2. researcher_agent gathers current/source-backed context only when needed.
3. writer_agent creates the practical explanation and snippets.
4. reviewer_agent checks accuracy and production readiness.
5. blogger_agent formats the final Markdown.
6. diagram_agent creates diagrams only when useful.
7. quiz_agent creates questions/tasks only when requested.

Default final answer structure:
## Short description
## Practical example
## Code/config snippet
## Subcomponents
## Production notes
## Summary

Token-saving rules:
- Do not call tools unless needed.
- Do not use all MCP servers for every request.
- Stable concept questions should be answered directly.
- Use search/docs only for current, version-sensitive, or source-backed answers.
- Keep snippets small and focused.

{COMMON_STYLE_RULES}

{COMMON_SECURITY_RULES}
""",
    sub_agents=[
        planner_agent,
        researcher_agent,
        writer_agent,
        reviewer_agent,
        blogger_agent,
        diagram_agent,
        quiz_agent,
    ],
)
