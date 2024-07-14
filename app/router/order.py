from fastapi import APIRouter, Depends

from app.common.permissions import IsAuthenticated
from app.common.response import JSONResponse
from app.common.security.credential import HTTPAuthorizationCredentials
from app.schemas.order import OrderInfo
from app.service.order import OrderService

router = APIRouter(prefix="/orders", tags=["Order"])


@router.post("", summary="주문 요청")
async def order(
    body: OrderInfo,
    service: OrderService = Depends(OrderService),
    credentials: HTTPAuthorizationCredentials = Depends(IsAuthenticated()),
) -> JSONResponse:
    return JSONResponse(
        content=await service.create_order(body, credentials)
    )


@router.get("/{order_id}", summary="주문 조회")
async def search_order(
    order_id: int,
    service: OrderService = Depends(OrderService),
    credentials: HTTPAuthorizationCredentials = Depends(IsAuthenticated()),
) -> JSONResponse:
    return JSONResponse(content=await service.search_order(order_id))
