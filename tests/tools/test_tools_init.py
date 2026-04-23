from __future__ import annotations

from unittest.mock import AsyncMock

from hotmart_mcp.server import create_server
from hotmart_mcp.tools import ALL_TOOLS, ESSENTIAL_TOOLS, WRITE_TOOLS


def _tool_names(server) -> set[str]:
    return {key.split(":")[1].split("@")[0] for key in server.local_provider._components if key.startswith("tool:")}


class TestToolFiltering:
    def test_essential_mode_only_has_read_tools(self) -> None:
        server = create_server(AsyncMock(), mode="essential")
        names = _tool_names(server)
        assert names == ESSENTIAL_TOOLS
        assert len(names) == 19

    def test_write_mode_has_all_tools(self) -> None:
        server = create_server(AsyncMock(), mode="write")
        names = _tool_names(server)
        assert names == ALL_TOOLS
        assert len(names) == 27

    def test_all_mode_same_as_write(self) -> None:
        server = create_server(AsyncMock(), mode="all")
        names = _tool_names(server)
        assert names == ALL_TOOLS
        assert len(names) == 27

    def test_essential_tools_are_subset_of_write(self) -> None:
        assert ESSENTIAL_TOOLS < ALL_TOOLS
        assert WRITE_TOOLS < ALL_TOOLS
        assert set() == ESSENTIAL_TOOLS & WRITE_TOOLS
