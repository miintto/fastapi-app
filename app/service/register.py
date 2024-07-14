from bcrypt import gensalt, hashpw
from fastapi import Depends, HTTPException

from app.model.auth import AuthUser, UserPermission
from app.model.repository.auth import AuthUserRepository
from app.schemas.auth import RegisterInfo


class RegisterService:
    def __init__(self, user: AuthUserRepository = Depends(AuthUserRepository)):
        self.user = user

    async def register(self, data: RegisterInfo) -> AuthUser:
        if await self.user.find_user_by_email(email=data.email):
            raise HTTPException(status_code=400)
        elif data.password != data.password_check:
            raise HTTPException(status_code=400)

        hashed_pw = hashpw(password=data.password.encode(), salt=gensalt())
        return await self.user.create(
            email=data.email,
            password=hashed_pw.decode(),
            permission=UserPermission.NORMAL,
        )
