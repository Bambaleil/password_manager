import asyncio
import sys
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete

from app.core.db import async_engine
from app.main import app
from app.models import Password, PasswordTestData  # type: ignore
from tests.factories.password_data_factory import PasswordDataFactory

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(loop_scope="session", scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as as_session:
        yield as_session
        async with AsyncSession(async_engine) as cleanup_session:
            await cleanup_session.execute(delete(Password))
            await cleanup_session.commit()


@pytest_asyncio.fixture(loop_scope="session", scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as as_client:
        yield as_client


@pytest.fixture(scope="session")
def password_data_factory() -> PasswordDataFactory:
    return PasswordDataFactory()


@pytest.fixture
def password_data(
    password_data_factory: PasswordDataFactory,
) -> PasswordTestData:
    return password_data_factory()


@pytest.fixture(autouse=True)
async def initialize_cache():
    FastAPICache.init(InMemoryBackend())
