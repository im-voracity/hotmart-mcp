from __future__ import annotations

import json
from unittest.mock import AsyncMock

from fastmcp import FastMCP
from hotmart import NotFoundError


class TestCreateNegotiation:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_negotiation.return_value = {"negotiation_id": "N1"}
        await mcp_server.call_tool("create_negotiation", {"subscriber_code": "SUB1"})
        mock_client.create_negotiation.assert_called_once_with("SUB1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_negotiation.return_value = {"negotiation_id": "N1"}
        result = await mcp_server.call_tool("create_negotiation", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["negotiation_id"] == "N1"

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_negotiation.side_effect = NotFoundError("subscriber not found")
        result = await mcp_server.call_tool("create_negotiation", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."

    async def test_null_result_returns_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.create_negotiation.return_value = None
        result = await mcp_server.call_tool("create_negotiation", {"subscriber_code": "SUB1"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Negotiation not available."
