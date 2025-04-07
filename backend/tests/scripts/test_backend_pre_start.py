from unittest.mock import AsyncMock, patch

from sqlalchemy import select
import pytest
from sqlalchemy.dialects import sqlite
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend_pre_start import wait_for_db, logger


@pytest.mark.asyncio(loop_scope="session")
async def test_init_successful_connection() -> None:
    as_engine_mock = AsyncMock()
    as_session_mock = AsyncMock(spec=AsyncSession)

    as_session_mock.__aenter__.return_value = as_session_mock
    as_session_mock.execute = AsyncMock(return_value=True)

    with (
        patch(
            "app.backend_pre_start.AsyncSession", return_value=as_session_mock
        ),
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            await wait_for_db(as_engine_mock)
            connection_successful = True
        except Exception as error:
            logger.error(error)
            connection_successful = False

        assert connection_successful, (
            "The database connection should"
            " be successful and not raise an exception."
        )
        as_session_mock.execute.assert_awaited_once()

        produced_query = as_session_mock.execute.call_args[0][0]
        produced_query_sql = str(
            produced_query.compile(dialect=sqlite.dialect())
        )
        expected_query_sql = str(select(1).compile(dialect=sqlite.dialect()))

        assert (
            produced_query_sql == expected_query_sql
        ), "The session should execute a select statement once."
