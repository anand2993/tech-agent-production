import os

import httpx
from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import log, run_stdio, text_response

app = Server("github_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="github_repo_context",
            description="Get GitHub repository metadata.",
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
    if name != "github_repo_context":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    query = arguments.get("query", "")
    try:
        repo_ref = query.strip().replace("https://github.com/", "").strip("/")
        parts = repo_ref.split("/")
        if len(parts) < 2:
            return text_response({"status": "error", "message": "Use owner/repo or a GitHub repository URL."})

        owner, repo = parts[0], parts[1]
        headers = {"Accept": "application/vnd.github+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
            response.raise_for_status()
            data = response.json()

        return text_response({
            "status": "ok",
            "repo": f"{owner}/{repo}",
            "description": data.get("description"),
            "language": data.get("language"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "default_branch": data.get("default_branch"),
        })
    except Exception as error:
        log("github_server", str(error))
        return text_response({"status": "error", "message": str(error)})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
