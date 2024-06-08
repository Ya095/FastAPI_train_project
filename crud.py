import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post


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


async def main():
    async with db_helper.session_factory() as session:
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


if __name__ == "__main__":
    asyncio.run(main())
