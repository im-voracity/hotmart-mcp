from __future__ import annotations

import json
from unittest.mock import AsyncMock

from fastmcp import FastMCP
from hotmart import AuthenticationError, NotFoundError


class TestListProducts:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_products.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("list_products", {"status": "ACTIVE"})
        mock_client.list_products.assert_called_once_with(status="ACTIVE")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_products.return_value = {"items": [{"id": 1}], "page_info": None}
        result = await mcp_server.call_tool("list_products", {})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_products.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("list_products", {})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetProductOffers:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_product_offers.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_product_offers", {"ucode": "UC1", "max_results": 5})
        mock_client.get_product_offers.assert_called_once_with("UC1", max_results=5)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_product_offers.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_product_offers", {"ucode": "UC1"})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_product_offers.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("get_product_offers", {"ucode": "UC1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."


class TestGetProductPlans:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_product_plans.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_product_plans", {"ucode": "UC1"})
        mock_client.get_product_plans.assert_called_once_with("UC1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_product_plans.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_product_plans", {"ucode": "UC1"})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_product_plans.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_product_plans", {"ucode": "UC1"})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed
