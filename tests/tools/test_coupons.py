from __future__ import annotations

import json
from unittest.mock import AsyncMock

from fastmcp import FastMCP
from hotmart import AuthenticationError, BadRequestError, NotFoundError


class TestListCoupons:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_coupons.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("list_coupons", {"product_id": "P1", "code": "SAVE10"})
        mock_client.list_coupons.assert_called_once_with("P1", code="SAVE10")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_coupons.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("list_coupons", {"product_id": "P1"})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_coupons.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("list_coupons", {"product_id": "P1"})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestCreateCoupon:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_coupon.return_value = {"status": "ok"}
        await mcp_server.call_tool("create_coupon", {"product_id": "P1", "coupon_code": "SAVE10", "discount": 10.0})
        mock_client.create_coupon.assert_called_once_with("P1", "SAVE10", 10.0)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_coupon.return_value = {"status": "ok"}
        args = {"product_id": "P1", "coupon_code": "SAVE10", "discount": 15.0}
        result = await mcp_server.call_tool("create_coupon", args)
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_coupon.side_effect = BadRequestError("invalid discount")
        args = {"product_id": "P1", "coupon_code": "X", "discount": 50.0}
        result = await mcp_server.call_tool("create_coupon", args)
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Bad request."


class TestDeleteCoupon:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.delete_coupon.return_value = {"status": "ok"}
        await mcp_server.call_tool("delete_coupon", {"coupon_id": "C1"})
        mock_client.delete_coupon.assert_called_once_with("C1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.delete_coupon.return_value = {"status": "ok"}
        result = await mcp_server.call_tool("delete_coupon", {"coupon_id": "C1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.delete_coupon.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("delete_coupon", {"coupon_id": "C1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."
