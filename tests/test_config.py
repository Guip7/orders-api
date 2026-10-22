import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings


def test_defaults_when_no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("APP_NAME", "APP_VERSION", "ENVIRONMENT", "DEBUG", "LOG_LEVEL"):
        monkeypatch.delenv(var, raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "Orders API"
    assert settings.environment == "development"
    assert settings.debug is False
    assert settings.log_level == "INFO"


def test_reads_values_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_NAME", "Minha Loja")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Minha Loja"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"


def test_invalid_environment_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "staging")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
