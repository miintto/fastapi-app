from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.config.security.jwt import JWTProvider
from app.schemas.auth import LoginInfo, RegisterInfo
from app.service.login import LoginService
from app.service.register import RegisterService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", summary="회원가입")
async def register(
    body: RegisterInfo,
    service: RegisterService = Depends(RegisterService),
    jwt: JWTProvider = Depends(JWTProvider),
) -> JSONResponse:
    user = await service.register(body)
    return JSONResponse(content=jwt.encode(user), status_code=200)


@router.post("/login", summary="로그인")
async def login(
    body: LoginInfo,
    service: LoginService = Depends(LoginService),
    jwt: JWTProvider = Depends(JWTProvider),
) -> JSONResponse:
    user = await service.login(body)
    return JSONResponse(content=jwt.encode(user), status_code=200)
