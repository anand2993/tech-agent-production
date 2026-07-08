from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("docs_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="official_docs_lookup",
            description="Return official docs links for common technologies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "official_docs_lookup":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    query = arguments.get("query", "")
    limit = int(arguments.get("limit", 5))

    docs = {
        "kubernetes": "https://kubernetes.io/docs/",
        "gke": "https://cloud.google.com/kubernetes-engine/docs",
        "cloud run": "https://cloud.google.com/run/docs",
        "terraform": "https://developer.hashicorp.com/terraform/docs",
        "aws": "https://docs.aws.amazon.com/",
        "ecs": "https://docs.aws.amazon.com/ecs/",
        "eks": "https://docs.aws.amazon.com/eks/",
        "gcp": "https://cloud.google.com/docs",
        "github actions": "https://docs.github.com/actions",
        "docker": "https://docs.docker.com/",
        "helm": "https://helm.sh/docs/",
        "mcp": "https://modelcontextprotocol.io/",
    }

    lowered = query.lower()
    matches = [{"topic": k, "url": v} for k, v in docs.items() if k in lowered]
    if not matches:
        matches = [{"topic": "general", "url": "Use official vendor documentation for the exact product/version."}]

    return text_response({"status": "ok", "query": query, "matches": matches[:limit]})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
