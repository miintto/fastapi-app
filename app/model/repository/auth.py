from sqlalchemy import select

from app.model.auth import AuthUser
from .base import BaseRepository


class AuthUserRepository(BaseRepository):
    model = AuthUser

    async def find_user_by_email(self, email: str) -> AuthUser | None:
        result = await self._session.execute(
            select(AuthUser).where(AuthUser.email == email)
        )
        return result.scalar_one_or_none()
