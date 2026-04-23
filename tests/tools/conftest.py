from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastmcp import FastMCP

from hotmart_mcp.server import create_server


@pytest.fixture
def mock_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mcp_server(mock_client: AsyncMock) -> FastMCP:
    """Server in 'all' mode so every tool is available."""
    return create_server(mock_client, mode="all")
