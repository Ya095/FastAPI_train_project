from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from core.models import Product
from api_v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


async def get_all_products(session: AsyncSession) -> list[Product]:
    smtp = select(Product).order_by(Product.id)
    result: Result = await session.execute(smtp)
    products = result.scalars().all()

    return list(products)


async def get_one_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def crete_product(session: AsyncSession, product_id: ProductCreate) -> Product:
    product = Product(**product_id.model_dump())
    session.add(product)
    await session.commit()
    # await session.reset(product)

    return product


# Полное обновление объекта (метод put), частичное - patch
async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False
) -> Product:
    for key, value in product_update.model_dump(exclude_unset=partial).items():  # model_dump() - получить словарь данных
        setattr(product, key, value)

    await session.commit()
    return product


async def delete_product(
        session: AsyncSession,
        product: Product
) -> None:
    await session.delete(product)
    await session.commit()
