import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from core.models import db_helper, User, Profile, Post, Order, Product


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print("found user", user)
    return user


async def create_user_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name
    )
    session.add(profile)
    await session.commit()
    return profile


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def main_relations(session: AsyncSession,):
    # await create_user(session, username="John")
    # await create_user(session, username="Sam")

    user_john = await get_user_by_username(session, "John")
    user_sam = await get_user_by_username(session, "Sam")

    await create_posts(
        session,
        user_sam.id,
        "SQL 1.0", "Sql 2.0"
    )
    await create_posts(
        session,
        user_john.id,
        "Some 1.0", "Some 2.0"
    )


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)  # регистрирует объект order в сессии, указывая, что он должен быть добавлен в бд
    await session.commit()  # сохраняет все изменения, зарегистрированные в сессии, в бд
    return order


async def create_product(session: AsyncSession, name: str, price: int, description: str) -> Product:
    product = Product(name=name, price=price, description=description)
    session.add(product)
    await session.commit()
    return product


async def demo_m2m(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode="promo")

    mouse = await create_product(session, "mouse", 450, "gaming mouse")
    keyboard = await create_product(session, "keyboard", 800, "gaming keyboard")
    display = await create_product(session, "display", 15000, "office display")

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(
            selectinload(Order.product),
        ),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.product),
        ),
    )

    order_one.product.append(mouse)
    order_one.product.append(keyboard)
    order_promo.product.append(display)
    order_promo.product.append(keyboard)

    await session.commit()


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
