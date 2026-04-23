from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastmcp import FastMCP

from hotmart_mcp.server import create_server


class TestCreateServer:
    """SPEC §7: Server creation."""

    def test_create_server_returns_fastmcp(self) -> None:
        mock_client = AsyncMock()
        server = create_server(mock_client, mode="essential")
        assert isinstance(server, FastMCP)

    def test_server_has_name(self) -> None:
        mock_client = AsyncMock()
        server = create_server(mock_client, mode="essential")
        assert server.name == "hotmart-mcp"

    def test_server_has_tools_registered(self) -> None:
        mock_client = AsyncMock()
        server = create_server(mock_client, mode="essential")
        tool_keys = [k for k in server.local_provider._components if k.startswith("tool:")]
        assert len(tool_keys) > 0

    def test_server_rejects_invalid_mode(self) -> None:
        mock_client = AsyncMock()
        with pytest.raises(ValueError, match="Unknown mode"):
            create_server(mock_client, mode="invalid")
