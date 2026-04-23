from __future__ import annotations

import json
from unittest.mock import AsyncMock

from fastmcp import FastMCP
from hotmart import AuthenticationError, BadRequestError, NotFoundError


class TestListSubscriptions:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_subscriptions.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("list_subscriptions", {"product_id": 10})
        mock_client.list_subscriptions.assert_called_once_with(product_id=10)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_subscriptions.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("list_subscriptions", {})
        parsed = json.loads(result.content[0].text)
        assert "items" in parsed

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.list_subscriptions.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("list_subscriptions", {})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetSubscriptionSummary:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_summary.return_value = {"items": [], "page_info": None}
        await mcp_server.call_tool("get_subscription_summary", {"subscriber_code": "SUB1"})
        mock_client.get_subscription_summary.assert_called_once_with(subscriber_code="SUB1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_summary.return_value = {"items": [], "page_info": None}
        result = await mcp_server.call_tool("get_subscription_summary", {})
        json.loads(result.content[0].text)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_summary.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_subscription_summary", {})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetSubscriptionPurchases:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_purchases.return_value = [{"id": 1}]
        await mcp_server.call_tool("get_subscription_purchases", {"subscriber_code": "SUB1"})
        mock_client.get_subscription_purchases.assert_called_once_with("SUB1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_purchases.return_value = [{"id": 1}]
        result = await mcp_server.call_tool("get_subscription_purchases", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert isinstance(parsed, list)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_purchases.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("get_subscription_purchases", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."


class TestGetSubscriptionTransactions:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_transactions.return_value = [{"id": 1}]
        await mcp_server.call_tool("get_subscription_transactions", {"subscriber_code": "SUB1"})
        mock_client.get_subscription_transactions.assert_called_once_with("SUB1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_transactions.return_value = []
        result = await mcp_server.call_tool("get_subscription_transactions", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert isinstance(parsed, list)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_subscription_transactions.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_subscription_transactions", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestCancelSubscriptions:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.cancel_subscriptions.return_value = {"status": "ok"}
        await mcp_server.call_tool("cancel_subscriptions", {"subscriber_code": '["SUB1", "SUB2"]'})
        mock_client.cancel_subscriptions.assert_called_once_with(["SUB1", "SUB2"], send_mail=True)

    async def test_single_code_as_string(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.cancel_subscriptions.return_value = {"status": "ok"}
        await mcp_server.call_tool("cancel_subscriptions", {"subscriber_code": "SUB1"})
        mock_client.cancel_subscriptions.assert_called_once_with(["SUB1"], send_mail=True)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.cancel_subscriptions.return_value = {"status": "ok"}
        result = await mcp_server.call_tool("cancel_subscriptions", {"subscriber_code": '["SUB1"]'})
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.cancel_subscriptions.side_effect = BadRequestError("invalid")
        result = await mcp_server.call_tool("cancel_subscriptions", {"subscriber_code": '["SUB1"]'})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Bad request."


class TestReactivateSubscriptions:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.reactivate_subscriptions.return_value = {"status": "ok"}
        await mcp_server.call_tool("reactivate_subscriptions", {"subscriber_code": '["SUB1"]'})
        mock_client.reactivate_subscriptions.assert_called_once_with(["SUB1"], charge=False)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.reactivate_subscriptions.return_value = {"status": "ok"}
        result = await mcp_server.call_tool("reactivate_subscriptions", {"subscriber_code": '["SUB1"]'})
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.reactivate_subscriptions.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("reactivate_subscriptions", {"subscriber_code": '["SUB1"]'})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestReactivateSubscription:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.reactivate_subscription.return_value = {"status": "ok"}
        await mcp_server.call_tool("reactivate_subscription", {"subscriber_code": "SUB1", "charge": True})
        mock_client.reactivate_subscription.assert_called_once_with("SUB1", charge=True)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.reactivate_subscription.return_value = {"status": "ok"}
        result = await mcp_server.call_tool("reactivate_subscription", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.reactivate_subscription.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("reactivate_subscription", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."


class TestChangeSubscriptionDueDay:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.change_subscription_due_day.return_value = {"status": "ok"}
        await mcp_server.call_tool("change_subscription_due_day", {"subscriber_code": "SUB1", "due_day": 15})
        mock_client.change_subscription_due_day.assert_called_once_with("SUB1", 15)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.change_subscription_due_day.return_value = {"status": "ok"}
        result = await mcp_server.call_tool("change_subscription_due_day", {"subscriber_code": "SUB1", "due_day": 10})
        parsed = json.loads(result.content[0].text)
        assert parsed["status"] == "ok"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.change_subscription_due_day.side_effect = BadRequestError("invalid day")
        result = await mcp_server.call_tool("change_subscription_due_day", {"subscriber_code": "SUB1", "due_day": 15})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Bad request."
