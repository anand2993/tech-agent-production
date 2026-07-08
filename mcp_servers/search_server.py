import os

import httpx
from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import log, run_stdio, text_response

app = Server("search_server")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="search_public_web",
            description="Search public internet using Brave Search if BRAVE_API_KEY is configured.",
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
    if name != "search_public_web":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    query = arguments.get("query", "")
    limit = int(arguments.get("limit", 5))

    try:
        api_key = os.getenv("BRAVE_API_KEY")
        if not api_key:
            return text_response({
                "status": "not_configured",
                "message": "BRAVE_API_KEY is not set. Configure it for live web search.",
                "query": query,
            })

        headers = {"Accept": "application/json", "X-Subscription-Token": api_key}
        params = {"q": query, "count": min(limit, 10)}

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        results = []
        for item in data.get("web", {}).get("results", [])[:limit]:
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description"),
            })

        return text_response({"status": "ok", "query": query, "results": results})
    except Exception as error:
        log("search_server", str(error))
        return text_response({"status": "error", "message": str(error)})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
