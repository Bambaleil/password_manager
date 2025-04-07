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
    stop=(
            stop_after_attempt(max_attempt_number=attempt)
            | stop_after_delay(max_delay=max_tries)
    ),
    wait=wait_fixed(wait=wait_second),
    before=before_log(logger=logger, log_level=logging.INFO),
    after=after_log(logger=logger, log_level=logging.DEBUG),
)
async def init(async_engine: AsyncEngine) -> None:
    try:
        async with AsyncSession(async_engine) as as_session:
            await as_session.execute(select(1))
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing service")
    await init(async_engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
