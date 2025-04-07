import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import UserCreate
from tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio(loop_scope="session")
async def test_create_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
