from __future__ import annotations

from hotmart_mcp.validators import parse_if_string


class TestParseIfString:
    """SPEC §6: JSON string parsing for MCP client parameters."""

    def test_parse_if_string_with_valid_json(self) -> None:
        assert parse_if_string('{"a": 1}') == {"a": 1}

    def test_parse_if_string_with_invalid_json(self) -> None:
        assert parse_if_string("not json") == "not json"

    def test_parse_if_string_with_dict(self) -> None:
        assert parse_if_string({"a": 1}) == {"a": 1}

    def test_parse_if_string_with_list(self) -> None:
        assert parse_if_string([1, 2]) == [1, 2]
