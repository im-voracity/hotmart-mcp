from __future__ import annotations

from typing import Any

from hotmart import AsyncHotmart

from .config import HotmartMCPConfig


def _paginated_to_dict(page: Any) -> dict[str, Any]:
    """Convert a PaginatedResponse to a plain dict."""
    items = [item.model_dump() for item in page.items]
    page_info = None
    if page.page_info and page.page_info.next_page_token:
        page_info = {"next_page_token": page.page_info.next_page_token}
    return {"items": items, "page_info": page_info}


def _list_to_dicts(items: list[Any]) -> list[dict[str, Any]]:
    """Convert a list of Pydantic models to plain dicts."""
    return [item.model_dump() for item in items]


_OK = {"status": "ok"}


class HotmartMCPClient:
    """Async wrapper around the Hotmart SDK.

    See SPEC.md §5 for the architecture contract.
    """

    def __init__(self, config: HotmartMCPConfig) -> None:
        self._sdk = AsyncHotmart(
            client_id=config.client_id,
            client_secret=config.client_secret,
            basic=config.basic,
            sandbox=config.sandbox,
        )

    async def __aenter__(self) -> HotmartMCPClient:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self._sdk.aclose()

    # --- Sales ---

    async def get_sales_history(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.sales.history(**kwargs)
        return _paginated_to_dict(page)

    async def get_sales_summary(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.sales.summary(**kwargs)
        return _paginated_to_dict(page)

    async def get_sales_participants(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.sales.participants(**kwargs)
        return _paginated_to_dict(page)

    async def get_sales_commissions(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.sales.commissions(**kwargs)
        return _paginated_to_dict(page)

    async def get_sales_price_details(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.sales.price_details(**kwargs)
        return _paginated_to_dict(page)

    async def refund_sale(self, transaction_code: str) -> dict[str, str]:
        await self._sdk.sales.refund(transaction_code)
        return _OK

    # --- Subscriptions ---

    async def list_subscriptions(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.subscriptions.list(**kwargs)
        return _paginated_to_dict(page)

    async def get_subscription_summary(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.subscriptions.summary(**kwargs)
        return _paginated_to_dict(page)

    async def get_subscription_purchases(self, subscriber_code: str) -> list[dict[str, Any]]:
        items = await self._sdk.subscriptions.purchases(subscriber_code)
        return _list_to_dicts(items)

    async def get_subscription_transactions(self, subscriber_code: str) -> list[dict[str, Any]]:
        items = await self._sdk.subscriptions.transactions(subscriber_code)
        return _list_to_dicts(items)

    async def cancel_subscriptions(self, subscriber_code: list[str], *, send_mail: bool = True) -> dict[str, Any]:
        result = await self._sdk.subscriptions.cancel(subscriber_code, send_mail=send_mail)
        if result is None:
            return _OK
        return dict(result.model_dump())

    async def reactivate_subscriptions(self, subscriber_code: list[str], *, charge: bool = False) -> dict[str, Any]:
        result = await self._sdk.subscriptions.reactivate(subscriber_code, charge=charge)
        if result is None:
            return _OK
        return dict(result.model_dump())

    async def reactivate_subscription(self, subscriber_code: str, *, charge: bool = False) -> dict[str, Any]:
        result = await self._sdk.subscriptions.reactivate_single(subscriber_code, charge=charge)
        if result is None:
            return _OK
        return dict(result.model_dump())

    async def change_subscription_due_day(self, subscriber_code: str, due_day: int) -> dict[str, str]:
        await self._sdk.subscriptions.change_due_day(subscriber_code, due_day)
        return _OK

    # --- Products ---

    async def list_products(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.products.list(**kwargs)
        return _paginated_to_dict(page)

    async def get_product_offers(self, ucode: str, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.products.offers(ucode, **kwargs)
        return _paginated_to_dict(page)

    async def get_product_plans(self, ucode: str, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.products.plans(ucode, **kwargs)
        return _paginated_to_dict(page)

    # --- Coupons ---

    async def list_coupons(self, product_id: str, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.coupons.list(product_id, **kwargs)
        return _paginated_to_dict(page)

    async def create_coupon(self, product_id: str, coupon_code: str, discount: float) -> dict[str, str]:
        await self._sdk.coupons.create(product_id, coupon_code, discount)
        return _OK

    async def delete_coupon(self, coupon_id: str) -> dict[str, str]:
        await self._sdk.coupons.delete(coupon_id)
        return _OK

    # --- Club ---

    async def get_club_modules(self, subdomain: str, **kwargs: Any) -> list[dict[str, Any]]:
        items = await self._sdk.club.modules(subdomain, **kwargs)
        return _list_to_dicts(items)

    async def get_club_pages(self, subdomain: str, module_id: str) -> list[dict[str, Any]]:
        items = await self._sdk.club.pages(subdomain, module_id)
        return _list_to_dicts(items)

    async def get_club_students(self, subdomain: str) -> list[dict[str, Any]]:
        items = await self._sdk.club.students(subdomain)
        return _list_to_dicts(items)

    async def get_club_student_progress(self, subdomain: str, **kwargs: Any) -> list[dict[str, Any]]:
        items = await self._sdk.club.student_progress(subdomain, **kwargs)
        return _list_to_dicts(items)

    # --- Events ---

    async def get_event(self, event_id: str) -> dict[str, Any] | None:
        result = await self._sdk.events.get(event_id)
        if result is None:
            return None
        return dict(result.model_dump())

    async def get_event_tickets(self, **kwargs: Any) -> dict[str, Any]:
        page = await self._sdk.events.tickets(**kwargs)
        return _paginated_to_dict(page)

    # --- Negotiation ---

    async def create_negotiation(self, subscriber_code: str) -> dict[str, Any] | None:
        result = await self._sdk.negotiation.create(subscriber_code)
        if result is None:
            return None
        return dict(result.model_dump())
