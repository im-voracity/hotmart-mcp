from __future__ import annotations

import argparse
from collections.abc import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for tool mode selection."""
    parser = argparse.ArgumentParser(description="Hotmart MCP server")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--essential",
        dest="mode",
        action="store_const",
        const="essential",
        help="Read-only tools only (default)",
    )
    group.add_argument("--write", dest="mode", action="store_const", const="write", help="Essential + mutation tools")
    group.add_argument("--all", dest="mode", action="store_const", const="all", help="All tools")
    parser.set_defaults(mode="essential")
    return parser.parse_args(argv)


def main() -> None:
    """Entry point for the hotmart-mcp CLI."""
    args = parse_args()

    from .client import HotmartMCPClient
    from .config import HotmartMCPConfig
    from .server import create_server

    config = HotmartMCPConfig()  # type: ignore[call-arg]
    client = HotmartMCPClient(config)
    server = create_server(client, mode=args.mode)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
