from __future__ import annotations

import pytest
from pydantic import ValidationError

from hotmart_mcp.config import HotmartMCPConfig


class TestHotmartMCPConfig:
    """SPEC §2: Configuration guard clauses and defaults."""

    def test_config_loads_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOTMART_CLIENT_ID", "test-id")
        monkeypatch.setenv("HOTMART_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("HOTMART_BASIC", "Basic dGVzdA==")

        config = HotmartMCPConfig()  # type: ignore[call-arg]

        assert config.client_id.get_secret_value() == "test-id"
        assert config.client_secret.get_secret_value() == "test-secret"
        assert config.basic.get_secret_value() == "Basic dGVzdA=="

    def test_config_missing_client_id(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("HOTMART_CLIENT_ID", raising=False)
        monkeypatch.setenv("HOTMART_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("HOTMART_BASIC", "Basic dGVzdA==")

        with pytest.raises(ValidationError):
            HotmartMCPConfig()  # type: ignore[call-arg]

    def test_config_missing_client_secret(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOTMART_CLIENT_ID", "test-id")
        monkeypatch.delenv("HOTMART_CLIENT_SECRET", raising=False)
        monkeypatch.setenv("HOTMART_BASIC", "Basic dGVzdA==")

        with pytest.raises(ValidationError):
            HotmartMCPConfig()  # type: ignore[call-arg]

    def test_config_missing_basic(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOTMART_CLIENT_ID", "test-id")
        monkeypatch.setenv("HOTMART_CLIENT_SECRET", "test-secret")
        monkeypatch.delenv("HOTMART_BASIC", raising=False)

        with pytest.raises(ValidationError):
            HotmartMCPConfig()  # type: ignore[call-arg]

    def test_config_empty_client_id(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOTMART_CLIENT_ID", "")
        monkeypatch.setenv("HOTMART_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("HOTMART_BASIC", "Basic dGVzdA==")

        with pytest.raises(ValidationError):
            HotmartMCPConfig()  # type: ignore[call-arg]

    def test_config_sandbox_default_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOTMART_CLIENT_ID", "test-id")
        monkeypatch.setenv("HOTMART_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("HOTMART_BASIC", "Basic dGVzdA==")
        monkeypatch.delenv("HOTMART_SANDBOX", raising=False)

        config = HotmartMCPConfig()  # type: ignore[call-arg]

        assert config.sandbox is False

    def test_config_sandbox_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOTMART_CLIENT_ID", "test-id")
        monkeypatch.setenv("HOTMART_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("HOTMART_BASIC", "Basic dGVzdA==")
        monkeypatch.setenv("HOTMART_SANDBOX", "true")

        config = HotmartMCPConfig()  # type: ignore[call-arg]

        assert config.sandbox is True
