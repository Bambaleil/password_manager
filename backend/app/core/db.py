from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
# from sqlmodel import select

# from app import crud
from app.core.config import settings
# from app.models import User, UserCreate

async_engine: AsyncEngine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=True
)


async def init_db(session: AsyncSession) -> None:
    result = await session.execute(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    )
    user = result.scalars().first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await crud.create_user(session=session, user_create=user_in)
