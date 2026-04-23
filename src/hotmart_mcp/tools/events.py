from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations
from pydantic import Field

from ..client import HotmartMCPClient
from ..exceptions import handle_sdk_errors


def register_event_tools(mcp: FastMCP, client: HotmartMCPClient | Any) -> None:
    """Register event tools. See SPEC.md §4.6."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_event(
        event_id: Annotated[str, Field(description="Event ID")],
    ) -> str:
        """Get event details."""
        result = await client.get_event(event_id)
        if result is None:
            return json.dumps({"error": "Event not found.", "event_id": event_id})
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_event_tickets(
        product_id: Annotated[int, Field(description="Product ID")],
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get event tickets for a product."""
        kwargs: dict[str, Any] = {"product_id": product_id}
        if max_results is not None:
            kwargs["max_results"] = max_results
        if page_token is not None:
            kwargs["page_token"] = page_token
        result = await client.get_event_tickets(**kwargs)
        return json.dumps(result, indent=2)
