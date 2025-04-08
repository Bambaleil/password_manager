import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_password
from app.crud import (
    create_password,
    get_password_by_service_name,
    update_password,
    search_passwords_by_service_name,
)
from app.models import PasswordTestData
from tests.factories.password_data_factory import PasswordDataFactory


@pytest.mark.asyncio
async def test_create_password(
    db: AsyncSession, password_data: PasswordTestData
):
    """
    Tests password creation:
    - Verifies that the data is correctly saved in the database.
    - Verifies the decryption of the encrypted password.
    """
    service_name = password_data.service_name
    raw_password = password_data.password

    password_obj = await create_password(db, service_name, raw_password)

    assert password_obj.service_name == service_name
    assert decrypt_password(password_obj.encrypted_password) == raw_password

    db_obj = await get_password_by_service_name(db, service_name)
    assert db_obj is not None
    assert decrypt_password(db_obj.encrypted_password) == raw_password


@pytest.mark.asyncio
async def test_update_password(
    db: AsyncSession, password_data: PasswordTestData
):
    """
    Tests password update:
    - Verifies that the password is correctly updated.
    - Ensures that the new password is different from the old one.
    """
    service_name = password_data.service_name
    old_password = password_data.password

    created = await create_password(db, service_name, old_password)
    new_password = "newSecret123!"

    updated = await update_password(db, created, new_password)

    assert decrypt_password(updated.encrypted_password) == new_password
    assert decrypt_password(updated.encrypted_password) != old_password


@pytest.mark.asyncio
async def test_get_password_by_service_name(
    db: AsyncSession, password_data: PasswordTestData
):
    """
    Tests retrieving a password by service name:
    - Verifies the correctness of the password search by service name.
    """
    service_name = password_data.service_name
    password = password_data.password

    await create_password(db, service_name, password)
    found = await get_password_by_service_name(db, service_name)

    assert found is not None
    assert found.service_name == service_name


@pytest.mark.asyncio
async def test_search_passwords_by_service_name(
    db: AsyncSession, password_data_factory: PasswordDataFactory
):
    """
    Tests searching passwords by service name using a keyword:
    - Verifies that all found services contain the keyword in the name.
    - Verifies the correct count of found services.
    """
    keyword = "test"
    service_names = [f"my-{keyword}-{i}.com" for i in range(5)]

    for name in service_names:
        data = password_data_factory()
        await create_password(db, name, data.password)

    results, total = await search_passwords_by_service_name(db, keyword)

    assert total == len(service_names)
    assert all(keyword in p.service_name for p in results)
