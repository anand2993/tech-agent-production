from typing import Optional

from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from _common import log, run_stdio, text_response

app = Server("trends_server")


def _pn_for_daily(geo: Optional[str]) -> str:
    mapping = {
        "US": "united_states",
        "GB": "united_kingdom",
        "UK": "united_kingdom",
        "CA": "canada",
        "AU": "australia",
        "IN": "india",
        "DE": "germany",
        "FR": "france",
        "JP": "japan",
        "BR": "brazil",
    }
    return mapping.get((geo or "US").upper(), "united_states")


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return [
        mcp_types.Tool(
            name="trends",
            description="Return Google Trends related/rising queries for a keyword using pytrends.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                    "geo": {"type": "string", "default": "US"},
                    "timeframe": {"type": "string", "default": "now 7-d"},
                    "quick": {"type": "boolean", "default": True},
                },
                "required": ["keyword"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name != "trends":
        return text_response({"status": "error", "message": f"Unknown tool: {name}"})

    keyword = arguments.get("keyword", "")
    geo = arguments.get("geo", "US")
    timeframe = arguments.get("timeframe", "now 7-d")
    quick = bool(arguments.get("quick", True))

    try:
        from pytrends.request import TrendReq

        pt = TrendReq(hl="en-US", tz=360, retries=0, backoff_factor=0)
        pt.build_payload([keyword], timeframe=timeframe, geo=geo or "")

        rq = pt.related_queries() or {}
        bucket = rq.get(keyword, {}) if isinstance(rq, dict) else {}

        def pack(df):
            result = []
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    result.append({
                        "query": str(row.get("query", "")),
                        "value": int(row.get("value", 0)),
                    })
            return result

        top = pack(bucket.get("top"))
        rising = pack(bucket.get("rising"))

        if not top and not rising:
            try:
                trends_df = pt.trending_searches(pn=_pn_for_daily(geo))
                if trends_df is not None and not trends_df.empty:
                    col = trends_df.columns[0]
                    rising = [{"query": str(x), "value": 0} for x in trends_df[col].tolist()[:20]]
            except Exception as fallback_error:
                log("trends_server", f"fallback failed: {fallback_error}")

        return text_response({
            "status": "ok",
            "keyword": keyword,
            "geo": geo,
            "timeframe": timeframe,
            "quick": quick,
            "related": {"top": top, "rising": rising},
        })
    except Exception as error:
        return text_response({"status": "error", "message": str(error)})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_stdio(app))
