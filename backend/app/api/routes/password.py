from typing import Annotated

from fastapi import APIRouter, Depends
from app.api.deps import AsSessionDep
from app.crud import get_password_by_service_name, create_password, update_password
from app.models import PasswordCreate, PasswordResponse

router = APIRouter()


@router.post("/{service_name}", response_model=PasswordResponse)
async def create_or_update_password(
        service_name: str,
        password_data: Annotated[PasswordCreate, Depends()],
        session: AsSessionDep
) -> PasswordResponse:
    existing = await get_password_by_service_name(session, service_name)

    if existing:
        await update_password(session, db_password=existing, new_password=password_data.password)
    else:
        await create_password(session, service_name=service_name, password=password_data.password)

    return PasswordResponse(service_name=service_name, password=password_data.password)
