import logging
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlmodel import select
from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)
from app.core.db import async_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

attempt = 5
max_tries = 60 * 5
wait_second = 1


@retry(
    stop=(stop_after_attempt(attempt) | stop_after_delay(max_tries)),
    wait=wait_fixed(wait_second),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.DEBUG),
)
async def wait_for_db(engine: AsyncEngine) -> None:
    try:
        async with AsyncSession(engine) as session:
            await session.execute(select(1))
    except Exception as e:
        logger.error("Database not ready: %s", e)
        raise


async def main() -> None:
    logger.info("Waiting for the database to become available...")
    await wait_for_db(async_engine)
    logger.info("Database is available!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
