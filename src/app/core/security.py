import uuid
from datetime import UTC, datetime, timedelta
from typing import Literal

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError

_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Gera o hash argon2id da senha (com salt aleatório embutido no resultado)."""
    return _password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Confere a senha contra o hash. Nunca levanta erro: hash inválido vira False."""
    try:
        return _password_hasher.verify(hashed_password, password)
    except (VerificationError, InvalidHashError):
        return False


TokenType = Literal["access", "refresh"]


class TokenPayload(BaseModel):
    sub: str
    type: TokenType
    jti: str
    iat: int
    exp: int


def create_token(subject: str, token_type: TokenType, expires_delta: timedelta) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "type": token_type,
        "jti": uuid.uuid4().hex,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(subject: str) -> str:
    minutes = get_settings().access_token_expire_minutes
    return create_token(subject, "access", timedelta(minutes=minutes))


def create_refresh_token(subject: str) -> str:
    days = get_settings().refresh_token_expire_days
    return create_token(subject, "refresh", timedelta(days=days))


def decode_token(token: str, expected_type: TokenType) -> TokenPayload:
    """Valida assinatura, expiração e tipo; problemas viram exceção de domínio."""
    settings = get_settings()
    try:
        data = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],  # nunca aceitar o algoritmo do token
            options={"require": ["exp", "iat", "sub", "jti"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError("token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidTokenError("invalid token") from exc

    payload = TokenPayload.model_validate(data)
    if payload.type != expected_type:
        raise InvalidTokenError(f"expected a {expected_type} token")
    return payload
