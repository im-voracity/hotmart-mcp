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


def register_sales_tools(mcp: FastMCP, client: HotmartMCPClient) -> None:
    """Register sales tools. See SPEC.md §4.1."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_sales_history(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        start_date: Annotated[int | None, Field(description="Start date (epoch ms)")] = None,
        end_date: Annotated[int | None, Field(description="End date (epoch ms)")] = None,
        sales_source: Annotated[str | None, Field(description="Sales source identifier")] = None,
        transaction: Annotated[str | None, Field(description="Filter by transaction code")] = None,
        buyer_name: Annotated[str | None, Field(description="Filter by buyer name")] = None,
        buyer_email: Annotated[str | None, Field(description="Filter by buyer email")] = None,
        transaction_status: Annotated[str | None, Field(description="Filter by status (e.g. APPROVED)")] = None,
        payment_type: Annotated[str | None, Field(description="Filter by payment method")] = None,
        offer_code: Annotated[str | None, Field(description="Filter by offer code")] = None,
        commission_as: Annotated[str | None, Field(description="Commission role filter")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get sales history with buyer, product, and payment details."""
        kwargs = _filter_none(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            sales_source=sales_source,
            transaction=transaction,
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            transaction_status=transaction_status,
            payment_type=payment_type,
            offer_code=offer_code,
            commission_as=commission_as,
            max_results=max_results,
            page_token=page_token,
        )
        result = await client.get_sales_history(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_sales_summary(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        start_date: Annotated[int | None, Field(description="Start date (epoch ms)")] = None,
        end_date: Annotated[int | None, Field(description="End date (epoch ms)")] = None,
        sales_source: Annotated[str | None, Field(description="Sales source identifier")] = None,
        affiliate_name: Annotated[str | None, Field(description="Filter by affiliate name")] = None,
        payment_type: Annotated[str | None, Field(description="Filter by payment method")] = None,
        offer_code: Annotated[str | None, Field(description="Filter by offer code")] = None,
        transaction: Annotated[str | None, Field(description="Filter by transaction code")] = None,
        transaction_status: Annotated[str | None, Field(description="Filter by status")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get aggregated sales commission values."""
        kwargs = _filter_none(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            sales_source=sales_source,
            affiliate_name=affiliate_name,
            payment_type=payment_type,
            offer_code=offer_code,
            transaction=transaction,
            transaction_status=transaction_status,
            max_results=max_results,
            page_token=page_token,
        )
        result = await client.get_sales_summary(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_sales_participants(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        start_date: Annotated[int | None, Field(description="Start date (epoch ms)")] = None,
        end_date: Annotated[int | None, Field(description="End date (epoch ms)")] = None,
        buyer_email: Annotated[str | None, Field(description="Filter by buyer email")] = None,
        buyer_name: Annotated[str | None, Field(description="Filter by buyer name")] = None,
        sales_source: Annotated[str | None, Field(description="Sales source identifier")] = None,
        transaction: Annotated[str | None, Field(description="Filter by transaction code")] = None,
        affiliate_name: Annotated[str | None, Field(description="Filter by affiliate name")] = None,
        commission_as: Annotated[str | None, Field(description="Commission role filter")] = None,
        transaction_status: Annotated[str | None, Field(description="Filter by status")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get sales participant and user data."""
        kwargs = _filter_none(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            buyer_email=buyer_email,
            buyer_name=buyer_name,
            sales_source=sales_source,
            transaction=transaction,
            affiliate_name=affiliate_name,
            commission_as=commission_as,
            transaction_status=transaction_status,
            max_results=max_results,
            page_token=page_token,
        )
        result = await client.get_sales_participants(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_sales_commissions(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        start_date: Annotated[int | None, Field(description="Start date (epoch ms)")] = None,
        end_date: Annotated[int | None, Field(description="End date (epoch ms)")] = None,
        transaction: Annotated[str | None, Field(description="Filter by transaction code")] = None,
        commission_as: Annotated[str | None, Field(description="Commission role filter")] = None,
        transaction_status: Annotated[str | None, Field(description="Filter by status")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get commission breakdown by role per transaction."""
        kwargs = _filter_none(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            transaction=transaction,
            commission_as=commission_as,
            transaction_status=transaction_status,
            max_results=max_results,
            page_token=page_token,
        )
        result = await client.get_sales_commissions(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_sales_price_details(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        start_date: Annotated[int | None, Field(description="Start date (epoch ms)")] = None,
        end_date: Annotated[int | None, Field(description="End date (epoch ms)")] = None,
        transaction: Annotated[str | None, Field(description="Filter by transaction code")] = None,
        transaction_status: Annotated[str | None, Field(description="Filter by status")] = None,
        payment_type: Annotated[str | None, Field(description="Filter by payment method")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get price, fee, and VAT details per transaction."""
        kwargs = _filter_none(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            transaction=transaction,
            transaction_status=transaction_status,
            payment_type=payment_type,
            max_results=max_results,
            page_token=page_token,
        )
        result = await client.get_sales_price_details(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
    @handle_sdk_errors
    async def refund_sale(
        transaction_code: Annotated[str, Field(description="Transaction code to refund")],
    ) -> str:
        """Request a refund for a transaction."""
        result = await client.refund_sale(transaction_code)
        return json.dumps(result, indent=2)
