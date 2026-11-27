from datetime import timedelta

import jwt
import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_token,
    decode_token,
)


def test_access_token_has_expected_claims() -> None:
    token = create_access_token("user-123")

    payload = decode_token(token, "access")

    assert payload.sub == "user-123"
    assert payload.type == "access"
    assert payload.exp > payload.iat


def test_refresh_token_lives_longer_than_access_token() -> None:
    access = decode_token(create_access_token("u"), "access")
    refresh = decode_token(create_refresh_token("u"), "refresh")

    assert refresh.exp > access.exp


def test_each_token_has_a_unique_jti() -> None:
    first = decode_token(create_refresh_token("u"), "refresh")
    second = decode_token(create_refresh_token("u"), "refresh")

    assert first.jti != second.jti


def test_expired_token_raises() -> None:
    token = create_token("u", "access", timedelta(seconds=-1))

    with pytest.raises(TokenExpiredError):
        decode_token(token, "access")


def test_refresh_token_cannot_be_used_as_access_token() -> None:
    token = create_refresh_token("u")

    with pytest.raises(InvalidTokenError):
        decode_token(token, "access")


def test_tampered_signature_is_rejected() -> None:
    token = create_access_token("u")
    forged = token[:-3] + ("AAA" if not token.endswith("AAA") else "BBB")

    with pytest.raises(InvalidTokenError):
        decode_token(forged, "access")


def test_token_signed_with_another_key_is_rejected() -> None:
    token = jwt.encode(
        {"sub": "u", "type": "access", "jti": "x", "iat": 1, "exp": 9999999999},
        "outra-chave-qualquer-com-mais-de-32-caracteres",
        algorithm="HS256",
    )

    with pytest.raises(InvalidTokenError):
        decode_token(token, "access")


def test_unsigned_token_is_rejected() -> None:
    token = jwt.encode(
        {"sub": "u", "type": "access", "jti": "x", "iat": 1, "exp": 9999999999},
        None,
        algorithm="none",
    )

    with pytest.raises(InvalidTokenError):
        decode_token(token, "access")


def test_garbage_is_rejected() -> None:
    with pytest.raises(InvalidTokenError):
        decode_token("isso-nao-e-um-jwt", "access")


def test_short_secret_key_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "curta")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_secret_key_is_not_exposed_in_repr() -> None:
    assert "test-secret-key" not in repr(get_settings())
