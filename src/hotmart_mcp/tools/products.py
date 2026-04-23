from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations
from pydantic import Field

from ..client import HotmartMCPClient
from ..exceptions import handle_sdk_errors


def _filter_none(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def register_product_tools(mcp: FastMCP, client: HotmartMCPClient) -> None:
    """Register product tools. See SPEC.md §4.3."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def list_products(
        id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        status: Annotated[str | None, Field(description="Filter by status (ACTIVE, DRAFT...)")] = None,
        format: Annotated[str | None, Field(description="Filter by format (ONLINE_COURSE...)")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """List products with filtering options."""
        kwargs = _filter_none(id=id, status=status, format=format, max_results=max_results, page_token=page_token)
        result = await client.list_products(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_product_offers(
        ucode: Annotated[str, Field(description="Product ucode")],
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get offers and payment options for a product."""
        kwargs = _filter_none(max_results=max_results, page_token=page_token)
        result = await client.get_product_offers(ucode, **kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_product_plans(
        ucode: Annotated[str, Field(description="Product ucode")],
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get subscription plans for a product."""
        kwargs = _filter_none(max_results=max_results, page_token=page_token)
        result = await client.get_product_plans(ucode, **kwargs)
        return json.dumps(result, indent=2)
