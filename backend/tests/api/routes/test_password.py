import pytest
from httpx import AsyncClient

from app.models import PasswordTestData
from tests.factories.password_data_factory import PasswordDataFactory


@pytest.mark.asyncio
async def test_create_or_update_password(
    async_client: AsyncClient, password_data: PasswordTestData
):
    service_name = password_data.service_name

    response = await async_client.post(
        f"/api/v1/password/{service_name}",
        json={"password": password_data.password},
    )
    assert response.status_code == 200

    new_password = "UpdatedPass123!"
    response = await async_client.post(
        f"/api/v1/password/{service_name}", json={"password": new_password}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_password(
    async_client: AsyncClient, password_data: PasswordTestData
):
    service_name = password_data.service_name
    await async_client.post(
        f"/api/v1/password/{service_name}",
        json={"password": password_data.password},
    )

    response = await async_client.get(f"/api/v1/password/{service_name}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_passwords(
    async_client: AsyncClient, password_data_factory: PasswordDataFactory
):
    keyword = "bulk-keyword"
    service_names = [f"{keyword}-{i}.com" for i in range(3)]

    for name in service_names:
        data = password_data_factory()
        await async_client.post(
            f"/api/v1/password/{name}", json={"password": data.password}
        )

    response = await async_client.get(
        f"/api/v1/password/?service_name={keyword}&skip=0&limit=10"
    )
    assert response.status_code == 200
