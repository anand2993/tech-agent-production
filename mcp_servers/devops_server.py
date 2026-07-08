from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("devops_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="devops_pattern",
            description="Return CI/CD and observability patterns.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "devops_pattern":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    pattern = {
        "pipeline": ["checkout", "unit test", "SAST", "build image", "container scan", "push image", "deploy", "smoke test"],
        "observability": ["logs", "metrics", "traces", "dashboards", "alerts"],
        "security": ["secret scanning", "dependency scanning", "SAST", "container image scanning", "least privilege"],
    }
    return text_response({"status": "ok", "topic": arguments.get("query", ""), "pattern": pattern})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
