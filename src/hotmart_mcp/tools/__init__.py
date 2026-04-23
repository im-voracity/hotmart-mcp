from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP

from ..client import HotmartMCPClient
from .club import register_club_tools
from .coupons import register_coupon_tools
from .events import register_event_tools
from .negotiation import register_negotiation_tools
from .products import register_product_tools
from .sales import register_sales_tools
from .subscriptions import register_subscription_tools

ToolMode = Literal["essential", "write", "all"]

ESSENTIAL_TOOLS: frozenset[str] = frozenset(
    {
        # Sales (5 read)
        "get_sales_history",
        "get_sales_summary",
        "get_sales_participants",
        "get_sales_commissions",
        "get_sales_price_details",
        # Subscriptions (4 read)
        "list_subscriptions",
        "get_subscription_summary",
        "get_subscription_purchases",
        "get_subscription_transactions",
        # Products (3 read)
        "list_products",
        "get_product_offers",
        "get_product_plans",
        # Coupons (1 read)
        "list_coupons",
        # Club (4 read)
        "get_club_modules",
        "get_club_pages",
        "get_club_students",
        "get_club_student_progress",
        # Events (2 read)
        "get_event",
        "get_event_tickets",
    }
)

WRITE_TOOLS: frozenset[str] = frozenset(
    {
        "refund_sale",
        "cancel_subscriptions",
        "reactivate_subscriptions",
        "reactivate_subscription",
        "change_subscription_due_day",
        "create_coupon",
        "delete_coupon",
        "create_negotiation",
    }
)

ALL_TOOLS: frozenset[str] = ESSENTIAL_TOOLS | WRITE_TOOLS

_VALID_MODES: dict[str, frozenset[str]] = {
    "essential": ESSENTIAL_TOOLS,
    "write": ALL_TOOLS,
    "all": ALL_TOOLS,
}


def _allowed_tools(mode: ToolMode) -> frozenset[str]:
    if mode not in _VALID_MODES:
        msg = f"Unknown mode: {mode!r}. Valid modes: {sorted(_VALID_MODES)}"
        raise ValueError(msg)
    return _VALID_MODES[mode]


def register_all_tools(mcp: FastMCP, client: HotmartMCPClient, *, mode: ToolMode = "essential") -> None:
    """Register all tools then remove those not in the active mode.

    See SPEC.md §3.2 for the filtering mechanism.
    """
    register_sales_tools(mcp, client)
    register_subscription_tools(mcp, client)
    register_product_tools(mcp, client)
    register_coupon_tools(mcp, client)
    register_club_tools(mcp, client)
    register_event_tools(mcp, client)
    register_negotiation_tools(mcp, client)

    allowed = _allowed_tools(mode)

    registered = [key.split(":")[1].split("@")[0] for key in mcp.local_provider._components if key.startswith("tool:")]

    for name in registered:
        if name not in allowed:
            mcp.local_provider.remove_tool(name)
