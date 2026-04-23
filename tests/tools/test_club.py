from __future__ import annotations

import json
from unittest.mock import AsyncMock

from fastmcp import FastMCP
from hotmart import AuthenticationError, NotFoundError


class TestGetClubModules:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_modules.return_value = [{"id": "m1"}]
        await mcp_server.call_tool("get_club_modules", {"subdomain": "myclub", "is_extra": True})
        mock_client.get_club_modules.assert_called_once_with("myclub", is_extra=True)

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_modules.return_value = [{"id": "m1"}]
        result = await mcp_server.call_tool("get_club_modules", {"subdomain": "myclub"})
        parsed = json.loads(result.content[0].text)
        assert isinstance(parsed, list)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_modules.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("get_club_modules", {"subdomain": "myclub"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."


class TestGetClubPages:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_pages.return_value = [{"id": "p1"}]
        await mcp_server.call_tool("get_club_pages", {"subdomain": "myclub", "module_id": "m1"})
        mock_client.get_club_pages.assert_called_once_with("myclub", "m1")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_pages.return_value = []
        result = await mcp_server.call_tool("get_club_pages", {"subdomain": "myclub", "module_id": "m1"})
        parsed = json.loads(result.content[0].text)
        assert isinstance(parsed, list)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_pages.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_club_pages", {"subdomain": "myclub", "module_id": "m1"})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetClubStudents:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_students.return_value = [{"email": "a@b.com"}]
        await mcp_server.call_tool("get_club_students", {"subdomain": "myclub"})
        mock_client.get_club_students.assert_called_once_with("myclub")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_students.return_value = []
        result = await mcp_server.call_tool("get_club_students", {"subdomain": "myclub"})
        parsed = json.loads(result.content[0].text)
        assert isinstance(parsed, list)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_students.side_effect = AuthenticationError("err")
        result = await mcp_server.call_tool("get_club_students", {"subdomain": "myclub"})
        parsed = json.loads(result.content[0].text)
        assert "error" in parsed


class TestGetClubStudentProgress:
    async def test_calls_correct_sdk_method(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_student_progress.return_value = [{"progress": 50}]
        await mcp_server.call_tool("get_club_student_progress", {"subdomain": "myclub", "student_email": "a@b.com"})
        mock_client.get_club_student_progress.assert_called_once_with("myclub", student_email="a@b.com")

    async def test_returns_valid_json(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_student_progress.return_value = []
        result = await mcp_server.call_tool("get_club_student_progress", {"subdomain": "myclub"})
        parsed = json.loads(result.content[0].text)
        assert isinstance(parsed, list)

    async def test_handles_sdk_error(self, mcp_server: FastMCP, mock_client: AsyncMock) -> None:
        mock_client.get_club_student_progress.side_effect = NotFoundError("not found")
        result = await mcp_server.call_tool("get_club_student_progress", {"subdomain": "myclub"})
        parsed = json.loads(result.content[0].text)
        assert parsed["error"] == "Resource not found."
