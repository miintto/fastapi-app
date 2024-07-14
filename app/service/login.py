from datetime import datetime, timezone

from bcrypt import checkpw
from fastapi import Depends, HTTPException

from app.model.auth import AuthUser
from app.model.repository.auth import AuthUserRepository
from app.schemas.auth import LoginInfo


class LoginService:
    def __init__(self, user: AuthUserRepository = Depends(AuthUserRepository)):
        self.user = user

    async def login(self, data: LoginInfo) -> AuthUser:
        user = await self.user.find_user_by_email(email=data.email)
        if not user:
            raise HTTPException(status_code=400)
        elif not checkpw(data.password.encode(), user.password.encode()):
            raise HTTPException(status_code=400)

        user.last_login = datetime.now(timezone.utc)
        await self.user.save()
        return user
