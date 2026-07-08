from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import run_stdio, text_response

app = Server("code_examples_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="code_example",
            description="Return small snippets for common DevOps/cloud topics.",
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
    if name != "code_example":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    query = arguments.get("query", "")
    lowered = query.lower()

    snippets = {
        "dockerfile": "FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD [\"python\", \"app.py\"]",
        "github actions": "name: ci\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4",
        "fastapi": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/health')\ndef health(): return {'status': 'ok'}",
        "cloud run": "gcloud run deploy app --image gcr.io/PROJECT/app --region australia-southeast1",
    }

    for key, value in snippets.items():
        if key in lowered:
            return text_response({"status": "ok", "topic": key, "snippet": value})

    return text_response({"status": "ok", "topic": query, "snippet": "# Add a focused snippet for this topic"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
