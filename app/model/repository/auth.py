from sqlalchemy import insert, select

from app.model.auth import AuthUser, UserPermission
from .base import BaseRepository


class AuthUserRepository(BaseRepository):
    async def find_user_by_email(self, email: str) -> AuthUser | None:
        result = await self._session.execute(
            select(AuthUser).where(AuthUser.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(
        self, permission: UserPermission = UserPermission.NORMAL, **kwargs
    ) -> AuthUser:
        result = await self._session.execute(
            insert(AuthUser)
            .values(permission=permission, **kwargs)
            .returning(AuthUser.id)
        )
        await self._session.commit()
        return AuthUser(
            id=result.scalar_one(), permission=permission, **kwargs
        )
