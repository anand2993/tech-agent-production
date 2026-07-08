from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("terraform_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="terraform_pattern",
            description="Return Terraform examples and best practices.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "terraform_pattern":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    snippet = """terraform {
  required_version = ">= 1.6.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}"""

    return text_response({
        "status": "ok",
        "topic": arguments.get("query", ""),
        "snippet": snippet,
        "best_practices": [
            "Use remote state",
            "Use modules",
            "Use variables",
            "Use least-privilege service accounts",
            "Run terraform fmt, validate, plan before apply",
        ],
    })


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
