import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole


class UserRepository:
    """Acesso a dados de usuários. Só fala com o banco, sem regra de negócio."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.CUSTOMER,
    ) -> User:
        user = User(email=email, hashed_password=hashed_password, role=role)
        self._session.add(user)
        # flush envia o INSERT (e já dispara erros de constraint), sem commitar.
        await self._session.flush()
        return user
