from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.products import crud
from api_v1.products.schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import db_helper
from .dependencies import get_product_by_id


router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_all_products(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_all_products(session=session)


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    product = await crud.get_one_product(session=session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!"
    )


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate = Depends(get_product_by_id)):
    return product


@router.put("/{product_id}")
async def update_product(
        product_update: ProductUpdate,
        product: Product = Depends(get_product_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update
    )


@router.patch("/{product_id}")
async def update_product_partial(
        product_update: ProductUpdatePartial,
        product: Product = Depends(get_product_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_for_del: Product = Depends(get_product_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> None:
    await crud.delete_product(session=session, product=product_for_del)
