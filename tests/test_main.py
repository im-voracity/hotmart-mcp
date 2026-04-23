from __future__ import annotations

from hotmart_mcp.__main__ import parse_args


class TestParseArgs:
    """SPEC §2.2: CLI argument modes."""

    def test_default_essential_mode(self) -> None:
        args = parse_args([])
        assert args.mode == "essential"

    def test_write_mode(self) -> None:
        args = parse_args(["--write"])
        assert args.mode == "write"

    def test_all_mode(self) -> None:
        args = parse_args(["--all"])
        assert args.mode == "all"

    def test_essential_explicit(self) -> None:
        args = parse_args(["--essential"])
        assert args.mode == "essential"
