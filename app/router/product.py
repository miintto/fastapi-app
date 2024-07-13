from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.service.product import ProductService

router = APIRouter(prefix="/products", tags=["Product"])


@router.get("", summary="상품 리스트")
async def product_list(
    service: ProductService = Depends(ProductService),
) -> JSONResponse:
    return JSONResponse(
        content=await service.get_product_list(), status_code=200
    )


@router.get("/{product_id}", summary="상품 상세")
async def product_detail(
    product_id: int,
    service: ProductService = Depends(ProductService),
) -> JSONResponse:
    return JSONResponse(
        content=await service.get_product(product_id), status_code=200
    )
