from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations
from pydantic import Field

from ..client import HotmartMCPClient
from ..exceptions import handle_sdk_errors


def register_negotiation_tools(mcp: FastMCP, client: HotmartMCPClient | Any) -> None:
    """Register negotiation tools. See SPEC.md §4.7."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
    @handle_sdk_errors
    async def create_negotiation(
        subscriber_code: Annotated[str, Field(description="Subscriber code")],
    ) -> str:
        """Create an installment negotiation for a subscription."""
        result = await client.create_negotiation(subscriber_code)
        if result is None:
            return json.dumps({"error": "Negotiation not available.", "subscriber_code": subscriber_code})
        return json.dumps(result, indent=2)
