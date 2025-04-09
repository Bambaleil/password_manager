import pytest
from httpx import AsyncClient

from app.models import PasswordTestData


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
