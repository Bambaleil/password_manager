from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from sqlmodel import SQLModel

from app.core.config import settings

async_engine: AsyncEngine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=True
)


async def init_db(session: AsyncSession) -> None:
    async with session.bind.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
