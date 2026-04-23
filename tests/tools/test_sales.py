from __future__ import annotations

import json
from unittest.mock import AsyncMock

from fastmcp import FastMCP
from hotmart import AuthenticationError, HotmartError, InternalServerError, NotFoundError, RateLimitError


class TestGetSalesHistory:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_sales_history", {"product_id": 123})
        mock_client.get_sales_history.assert_called_once_with(product_id=123)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.return_value = {"items": [{"id": 1}], "page_info": None}
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.side_effect = AuthenticationError("bad creds")
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Authentication failed. Check credentials."


class TestGetSalesSummary:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_summary.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_sales_summary", {"product_id": 42})
        mock_client.get_sales_summary.assert_called_once_with(product_id=42)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_summary.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_sales_summary", {})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_summary.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("get_sales_summary", {})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."


class TestGetSalesParticipants:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_participants.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_sales_participants", {"buyer_email": "a@b.com"})
        mock_client.get_sales_participants.assert_called_once_with(buyer_email="a@b.com")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_participants.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_sales_participants", {})
        json.loads(result.content[0].text)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_participants.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_sales_participants", {})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetSalesCommissions:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_commissions.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_sales_commissions", {"transaction": "TX1"})
        mock_client.get_sales_commissions.assert_called_once_with(transaction="TX1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_commissions.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_sales_commissions", {})
        json.loads(result.content[0].text)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_commissions.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_sales_commissions", {})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetSalesPriceDetails:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_price_details.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_sales_price_details", {"payment_type": "CREDIT_CARD"})
        mock_client.get_sales_price_details.assert_called_once_with(payment_type="CREDIT_CARD")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_price_details.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_sales_price_details", {})
        json.loads(result.content[0].text)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_price_details.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_sales_price_details", {})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestRefundSale:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.refund_sale.return_value = {"status": "ok"}
        await mcp_server.call_tool("refund_sale", {"transaction_code": "TX123"})
        mock_client.refund_sale.assert_called_once_with("TX123")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.refund_sale.return_value = {"status": "ok"}
        result = await mcp_server.call_tool("refund_sale", {"transaction_code": "TX123"})
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.refund_sale.side_effect = NotFoundError("tx not found")
        result = await mcp_server.call_tool("refund_sale", {"transaction_code": "TX123"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."


class TestErrorHandlerCoverage:
    """Test remaining exception types in handle_sdk_errors decorator."""

    async def test_rate_limit_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.side_effect = RateLimitError("rate limited")
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Rate limit exceeded. Try again later."

    async def test_internal_server_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.side_effect = InternalServerError("500")
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Hotmart API error."

    async def test_generic_hotmart_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.side_effect = HotmartError("unknown")
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Unexpected error."

    async def test_non_sdk_exception_caught(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.side_effect = RuntimeError("unexpected")
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Internal error."
        assert parsed["type"] == "RuntimeError"

    async def test_auth_error_includes_detail(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_sales_history.side_effect = AuthenticationError("HTTP 403: Forbidden")
        result = await mcp_server.call_tool("get_sales_history", {})
        parsed = json.loads(result.content[0].text)
        assert "detail" in parsed
        assert "403" in parsed["detail"]
