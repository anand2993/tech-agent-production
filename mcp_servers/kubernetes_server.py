from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("kubernetes_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="kubernetes_pattern",
            description="Return Kubernetes explanation snippets and YAML.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "kubernetes_pattern":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    snippet = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: app
        image: nginx:latest
        ports:
        - containerPort: 80"""

    return text_response({
        "status": "ok",
        "topic": arguments.get("query", ""),
        "pattern": "Deployment manages replicated Pods. Service exposes them internally or externally.",
        "snippet": snippet,
    })


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
