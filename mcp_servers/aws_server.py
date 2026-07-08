from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("aws_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="aws_pattern",
            description="Return AWS ECS/EKS/CloudWatch operational commands.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "aws_pattern":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    snippet = "aws ecs list-clusters\naws ecs list-services --cluster my-cluster\naws logs tail /ecs/my-service --follow"
    return text_response({
        "status": "ok",
        "topic": arguments.get("query", ""),
        "snippet": snippet,
        "notes": ["Use IAM least privilege", "Use CloudWatch logs/metrics", "Use Secrets Manager for secrets"],
    })


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
