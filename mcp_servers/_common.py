import json
import sys
from typing import Any

import mcp.server.stdio
from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions


def log(server: str, msg: str) -> None:
    print(f"[{server}] {msg}", file=sys.stderr)


def text_response(data: Any) -> list[mcp_types.Content]:
    return [mcp_types.TextContent(type="text", text=json.dumps(data, indent=2))]


async def run_stdio(app: Server, version: str = "1.0.0"):
    async with mcp.server.stdio.stdio_server() as (r, w):
        await app.run(
            r,
            w,
            InitializationOptions(
                server_name=app.name,
                server_version=version,
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
