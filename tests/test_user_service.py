from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import EmailAlreadyRegisteredError
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.user import UserService


@pytest.fixture
def session() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def repository() -> AsyncMock:
    repo = AsyncMock(spec=UserRepository)
    repo.get_by_email.return_value = None
    repo.create.side_effect = lambda email, hashed_password, **_: User(
        email=email, hashed_password=hashed_password
    )
    return repo


@pytest.fixture
def service(session: AsyncMock, repository: AsyncMock) -> UserService:
    return UserService(session=session, repository=repository)


async def test_register_hashes_password_and_commits(
    service: UserService, session: AsyncMock, repository: AsyncMock
) -> None:
    user = await service.register("Ana@Example.com ", "supersecret")

    assert user.email == "ana@example.com"
    assert user.hashed_password != "supersecret"
    assert user.hashed_password.startswith("$argon2id$")
    repository.create.assert_awaited_once()
    session.commit.assert_awaited_once()


async def test_register_rejects_existing_email(
    service: UserService, session: AsyncMock, repository: AsyncMock
) -> None:
    repository.get_by_email.return_value = User(
        email="ana@example.com", hashed_password="x"
    )

    with pytest.raises(EmailAlreadyRegisteredError):
        await service.register("ana@example.com", "supersecret")

    repository.create.assert_not_awaited()
    session.commit.assert_not_awaited()


async def test_register_handles_race_condition(
    service: UserService, session: AsyncMock, repository: AsyncMock
) -> None:
    repository.create.side_effect = IntegrityError("INSERT", {}, Exception("dup"))

    with pytest.raises(EmailAlreadyRegisteredError):
        await service.register("ana@example.com", "supersecret")

    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()


async def test_get_by_email_normalizes_input(
    service: UserService, repository: AsyncMock
) -> None:
    await service.get_by_email("  ANA@Example.com")

    repository.get_by_email.assert_awaited_once_with("ana@example.com")
