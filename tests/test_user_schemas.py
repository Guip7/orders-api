import pytest
from pydantic import ValidationError

from app.core.db import Base
from app.models.user import UserRole
from app.schemas.user import UserCreate


def test_user_create_accepts_valid_data() -> None:
    user = UserCreate(email="ana@example.com", password="supersecret")

    assert user.email == "ana@example.com"


def test_user_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="nao-e-email", password="supersecret")


def test_user_create_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="ana@example.com", password="curta")


def test_users_table_is_registered_in_metadata() -> None:
    table = Base.metadata.tables["users"]

    assert {"id", "email", "hashed_password", "role", "is_active"} <= set(
        table.c.keys()
    )
    assert table.c.email.unique
    assert {role.value for role in UserRole} == {"customer", "admin"}
