import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import SessionDep
from app.core.exceptions import EmailAlreadyRegisteredError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository


def normalize_email(email: str) -> str:
    return email.strip().lower()


class UserService:
    """Regras de negócio de usuários. Também é quem controla a transação."""

    def __init__(self, session: AsyncSession, repository: UserRepository) -> None:
        self._session = session
        self._repository = repository

    async def register(self, email: str, password: str) -> User:
        email = normalize_email(email)

        # Caminho rápido: evita gastar um hash argon2 (~200 ms) à toa.
        if await self._repository.get_by_email(email) is not None:
            raise EmailAlreadyRegisteredError(email)

        try:
            user = await self._repository.create(
                email=email, hashed_password=hash_password(password)
            )
            await self._session.commit()
        except IntegrityError as exc:
            # Duas requisições simultâneas passaram pela checagem acima:
            # quem decide é a constraint única do banco.
            await self._session.rollback()
            raise EmailAlreadyRegisteredError(email) from exc
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self._repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self._repository.get_by_email(normalize_email(email))


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session=session, repository=UserRepository(session))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
