from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from .client import HotmartMCPClient
from .tools import ToolMode, register_all_tools


def create_server(client: HotmartMCPClient | Any, mode: ToolMode = "essential") -> FastMCP:
    """Create and configure the MCP server with tools filtered by mode.

    See SPEC.md §3 for mode definitions.
    """
    mcp = FastMCP("hotmart-mcp")
    register_all_tools(mcp, client, mode=mode)
    return mcp
