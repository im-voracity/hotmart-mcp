from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from hotmart_mcp.client import HotmartMCPClient
from hotmart_mcp.config import HotmartMCPConfig


@pytest.fixture
def mock_config() -> HotmartMCPConfig:
    return HotmartMCPConfig(
        client_id="test-id",
        client_secret="test-secret",
        basic="Basic dGVzdA==",
    )


class TestHotmartMCPClient:
    """SPEC §5: Client wrapper around AsyncHotmart."""

    def test_client_initializes_async_hotmart(self, mock_config: HotmartMCPConfig) -> None:
        with patch("hotmart_mcp.client.AsyncHotmart") as mock_cls:
            client = HotmartMCPClient(mock_config)
            mock_cls.assert_called_once_with(
                client_id="test-id",
                client_secret="test-secret",
                basic="Basic dGVzdA==",
                sandbox=False,
            )
            assert client._sdk is mock_cls.return_value

    @pytest.mark.asyncio
    async def test_client_paginated_response_shape(self, mock_config: HotmartMCPConfig) -> None:
        with patch("hotmart_mcp.client.AsyncHotmart") as mock_cls:
            mock_item = MagicMock()
            mock_item.model_dump.return_value = {"id": 1, "name": "test"}
            mock_page_info = MagicMock()
            mock_page_info.next_page_token = "next-token"
            mock_page = MagicMock()
            mock_page.items = [mock_item]
            mock_page.page_info = mock_page_info

            mock_sdk = mock_cls.return_value
            mock_sdk.sales = MagicMock()
            mock_sdk.sales.history = AsyncMock(return_value=mock_page)

            client = HotmartMCPClient(mock_config)
            result = await client.get_sales_history()

            assert result == {
                "items": [{"id": 1, "name": "test"}],
                "page_info": {"next_page_token": "next-token"},
            }

    @pytest.mark.asyncio
    async def test_client_list_response_shape(self, mock_config: HotmartMCPConfig) -> None:
        with patch("hotmart_mcp.client.AsyncHotmart") as mock_cls:
            mock_item = MagicMock()
            mock_item.model_dump.return_value = {"module": "intro"}

            mock_sdk = mock_cls.return_value
            mock_sdk.club = MagicMock()
            mock_sdk.club.modules = AsyncMock(return_value=[mock_item])

            client = HotmartMCPClient(mock_config)
            result = await client.get_club_modules(subdomain="test")

            assert result == [{"module": "intro"}]

    @pytest.mark.asyncio
    async def test_client_void_response_shape(self, mock_config: HotmartMCPConfig) -> None:
        with patch("hotmart_mcp.client.AsyncHotmart") as mock_cls:
            mock_sdk = mock_cls.return_value
            mock_sdk.sales = MagicMock()
            mock_sdk.sales.refund = AsyncMock(return_value=None)

            client = HotmartMCPClient(mock_config)
            result = await client.refund_sale(transaction_code="TX123")

            assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_client_context_manager(self, mock_config: HotmartMCPConfig) -> None:
        with patch("hotmart_mcp.client.AsyncHotmart") as mock_cls:
            mock_sdk = mock_cls.return_value
            mock_sdk.aclose = AsyncMock()

            async with HotmartMCPClient(mock_config) as client:
                assert client._sdk is mock_sdk

            mock_sdk.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_client_forwards_kwargs(self, mock_config: HotmartMCPConfig) -> None:
        with patch("hotmart_mcp.client.AsyncHotmart") as mock_cls:
            mock_page = MagicMock()
            mock_page.items = []
            mock_page.page_info = None

            mock_sdk = mock_cls.return_value
            mock_sdk.sales = MagicMock()
            mock_sdk.sales.history = AsyncMock(return_value=mock_page)

            client = HotmartMCPClient(mock_config)
            await client.get_sales_history(product_id=123, start_date=1000, buyer_email="a@b.com")

            mock_sdk.sales.history.assert_called_once_with(product_id=123, start_date=1000, buyer_email="a@b.com")
