from __future__ import annotations

import json
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations
from pydantic import Field

from ..client import HotmartMCPClient
from ..exceptions import handle_sdk_errors


def register_club_tools(mcp: FastMCP, client: HotmartMCPClient) -> None:
    """Register club/members area tools. See SPEC.md §4.5."""

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_club_modules(
        subdomain: Annotated[str, Field(description="Members area subdomain")],
        is_extra: Annotated[bool | None, Field(description="Filter extra modules")] = None,
    ) -> str:
        """Get course modules for a members area."""
        kwargs: dict[str, Any] = {}
        if is_extra is not None:
            kwargs["is_extra"] = is_extra
        result = await client.get_club_modules(subdomain, **kwargs)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_club_pages(
        subdomain: Annotated[str, Field(description="Members area subdomain")],
        module_id: Annotated[str, Field(description="Module identifier")],
    ) -> str:
        """Get pages within a course module."""
        result = await client.get_club_pages(subdomain, module_id)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_club_students(
        subdomain: Annotated[str, Field(description="Members area subdomain")],
    ) -> str:
        """Get enrolled students for a members area."""
        result = await client.get_club_students(subdomain)
        return json.dumps(result, indent=2)

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    @handle_sdk_errors
    async def get_club_student_progress(
        subdomain: Annotated[str, Field(description="Members area subdomain")],
        student_email: Annotated[str | None, Field(description="Filter by email")] = None,
    ) -> str:
        """Get student completion progress data."""
        kwargs: dict[str, Any] = {}
        if student_email is not None:
            kwargs["student_email"] = student_email
        result = await client.get_club_student_progress(subdomain, **kwargs)
        return json.dumps(result, indent=2)
