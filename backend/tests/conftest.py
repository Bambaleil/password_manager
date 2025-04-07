import asyncio
import sys
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete

from app.core.db import async_engine
from app.main import app
from app.models import User

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(loop_scope="session", scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as as_session:
        yield as_session
        async with AsyncSession(async_engine) as cleanup_session:
            await cleanup_session.execute(delete(User))
            await cleanup_session.commit()


@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as as_client:
        yield as_client
