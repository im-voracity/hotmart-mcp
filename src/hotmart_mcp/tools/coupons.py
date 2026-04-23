from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations
from pydantic import Field

from ..client import HotmartMCPClient
from ..exceptions import handle_sdk_errors


def register_coupon_tools(mcp: FastMCP, client: HotmartMCPClient | Any) -> None:
    """Register coupon tools. See SPEC.md §4.4."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def list_coupons(
        product_id: Annotated[str, Field(description="Product ID")],
        code: Annotated[str | None, Field(description="Filter by coupon code")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """List coupons for a product."""
        kwargs: dict[str, Any] = {}
        if code is not None:
            kwargs["code"] = code
        if page_token is not None:
            kwargs["page_token"] = page_token
        result = await client.list_coupons(product_id, **kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
    @handle_sdk_errors
    async def create_coupon(
        product_id: Annotated[str, Field(description="Product ID")],
        coupon_code: Annotated[str, Field(description="Coupon code")],
        discount: Annotated[float, Field(description="Discount percentage (0-100)", ge=0.0, le=100.0)],
    ) -> str:
        """Create a discount coupon for a product."""
        result = await client.create_coupon(product_id, coupon_code, discount)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
    @handle_sdk_errors
    async def delete_coupon(
        coupon_id: Annotated[str, Field(description="Coupon ID")],
    ) -> str:
        """Delete a coupon."""
        result = await client.delete_coupon(coupon_id)
        return json.dumps(result, indent=2)
