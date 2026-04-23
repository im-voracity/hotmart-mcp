from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations
from pydantic import Field

from ..client import HotmartMCPClient
from ..exceptions import handle_sdk_errors
from ..validators import parse_if_string


def _filter_none(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def register_subscription_tools(mcp: FastMCP, client: HotmartMCPClient) -> None:
    """Register subscription tools. See SPEC.md §4.2."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def list_subscriptions(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        plan_id: Annotated[int | None, Field(description="Filter by plan ID")] = None,
        accession_date: Annotated[int | None, Field(description="Accession start date (epoch ms)")] = None,
        end_accession_date: Annotated[int | None, Field(description="Accession end date (epoch ms)")] = None,
        status: Annotated[str | None, Field(description="Filter by status")] = None,
        subscriber_code: Annotated[str | None, Field(description="Filter by subscriber code")] = None,
        subscriber_email: Annotated[str | None, Field(description="Filter by subscriber email")] = None,
        transaction: Annotated[str | None, Field(description="Filter by transaction code")] = None,
        trial: Annotated[bool | None, Field(description="Filter by trial status")] = None,
        cancelation_date: Annotated[int | None, Field(description="Cancellation start date")] = None,
        end_cancelation_date: Annotated[int | None, Field(description="Cancellation end date")] = None,
        date_next_charge: Annotated[int | None, Field(description="Next charge start date")] = None,
        end_date_next_charge: Annotated[int | None, Field(description="Next charge end date")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """List subscriptions with filtering options."""
        kwargs = _filter_none(
            product_id=product_id, plan_id=plan_id, accession_date=accession_date,
            end_accession_date=end_accession_date, status=status, subscriber_code=subscriber_code,
            subscriber_email=subscriber_email, transaction=transaction, trial=trial,
            cancelation_date=cancelation_date, end_cancelation_date=end_cancelation_date,
            date_next_charge=date_next_charge, end_date_next_charge=end_date_next_charge,
            max_results=max_results, page_token=page_token,
        )
        result = await client.list_subscriptions(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_subscription_summary(
        product_id: Annotated[int | None, Field(description="Filter by product ID")] = None,
        subscriber_code: Annotated[str | None, Field(description="Filter by subscriber")] = None,
        accession_date: Annotated[int | None, Field(description="Accession start date")] = None,
        end_accession_date: Annotated[int | None, Field(description="Accession end date")] = None,
        date_next_charge: Annotated[int | None, Field(description="Next charge date filter")] = None,
        max_results: Annotated[int | None, Field(description="Max items per page")] = None,
        page_token: Annotated[str | None, Field(description="Pagination token")] = None,
    ) -> str:
        """Get subscription statistics summary."""
        kwargs = _filter_none(
            product_id=product_id, subscriber_code=subscriber_code, accession_date=accession_date,
            end_accession_date=end_accession_date, date_next_charge=date_next_charge,
            max_results=max_results, page_token=page_token,
        )
        result = await client.get_subscription_summary(**kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_subscription_purchases(
        subscriber_code: Annotated[str, Field(description="Subscriber identifier")],
    ) -> str:
        """Get purchase history for a subscriber."""
        result = await client.get_subscription_purchases(subscriber_code)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_subscription_transactions(
        subscriber_code: Annotated[str, Field(description="Subscriber identifier")],
    ) -> str:
        """Get transaction history for a subscriber."""
        result = await client.get_subscription_transactions(subscriber_code)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
    @handle_sdk_errors
    async def cancel_subscriptions(
        subscriber_code: Annotated[str, Field(description='JSON list of subscriber codes, e.g. \'["SUB1", "SUB2"]\'')],
        send_mail: Annotated[bool, Field(description="Send cancellation email")] = True,
    ) -> str:
        """Cancel one or more subscriptions."""
        codes = parse_if_string(subscriber_code)
        if not isinstance(codes, list):
            codes = [codes]
        result = await client.cancel_subscriptions(codes, send_mail=send_mail)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
    @handle_sdk_errors
    async def reactivate_subscriptions(
        subscriber_code: Annotated[str, Field(description='JSON list of subscriber codes, e.g. \'["SUB1", "SUB2"]\'')],
        charge: Annotated[bool, Field(description="Charge immediately")] = False,
    ) -> str:
        """Reactivate one or more subscriptions in bulk."""
        codes = parse_if_string(subscriber_code)
        if not isinstance(codes, list):
            codes = [codes]
        result = await client.reactivate_subscriptions(codes, charge=charge)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
    @handle_sdk_errors
    async def reactivate_subscription(
        subscriber_code: Annotated[str, Field(description="Subscriber code")],
        charge: Annotated[bool, Field(description="Charge immediately")] = False,
    ) -> str:
        """Reactivate a single subscription."""
        result = await client.reactivate_subscription(subscriber_code, charge=charge)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
    @handle_sdk_errors
    async def change_subscription_due_day(
        subscriber_code: Annotated[str, Field(description="Subscriber code")],
        due_day: Annotated[int, Field(description="New billing day (1-28)", ge=1, le=28)],
    ) -> str:
        """Change the billing due day for a subscription."""
        result = await client.change_subscription_due_day(subscriber_code, due_day)
        return json.dumps(result, indent=2)
