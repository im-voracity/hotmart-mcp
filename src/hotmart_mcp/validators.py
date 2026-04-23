from __future__ import annotations

import json
from typing import Any


def parse_if_string(value: Any) -> Any:
    """Parse JSON strings from MCP clients that serialize nested objects."""
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError):
        return value
