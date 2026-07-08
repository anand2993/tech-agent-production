from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("gcp_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="gcp_pattern",
            description="Return GCP, GKE, and Cloud Run operational commands.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "gcp_pattern":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    snippet = "gcloud run services list --region australia-southeast1\ngcloud container clusters get-credentials CLUSTER --region REGION"
    return text_response({
        "status": "ok",
        "topic": arguments.get("query", ""),
        "snippet": snippet,
        "notes": ["Use Secret Manager", "Use Workload Identity for GKE", "Use Cloud Logging and Monitoring"],
    })


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
