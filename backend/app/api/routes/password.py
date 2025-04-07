from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import AsSessionDep
from app.core.security import decrypt_password
from app.crud import (
    get_password_by_service_name,
    create_password,
    update_password,
    search_passwords_by_service_name,
)
from app.models import PasswordCreate, PasswordResponse, PasswordsResponse

router = APIRouter()


@router.post("/{service_name}", response_model=PasswordResponse)
async def create_or_update_password(
    service_name: str,
    password_data: Annotated[PasswordCreate, Depends()],
    session: AsSessionDep,
) -> PasswordResponse:
    existing = await get_password_by_service_name(
        session=session, service_name=service_name
    )

    if existing:
        await update_password(
            session=session,
            db_password=existing,
            new_password=password_data.password,
        )
    else:
        await create_password(
            session=session,
            service_name=service_name,
            password=password_data.password,
        )

    return PasswordResponse(
        service_name=service_name, password=password_data.password
    )


@router.get("/{service_name}", response_model=PasswordResponse)
async def get_password(
    service_name: str,
    session: AsSessionDep,
) -> PasswordResponse:
    existing = await get_password_by_service_name(
        session=session, service_name=service_name
    )
    if not existing:
        raise HTTPException(
            status_code=400,
            detail="Not service in database",
        )
    password = decrypt_password(existing.encrypted_password)
    return PasswordResponse(service_name=service_name, password=password)


@router.get("/", response_model=PasswordsResponse)
async def get_passwords(
    service_name: str, session: AsSessionDep, skip: int = 0, limit: int = 0
):
    results, count = await search_passwords_by_service_name(
        session=session, service_name=service_name, skip=skip, limit=limit
    )

    passwords = [
        PasswordResponse(
            service_name=p.service_name,
            password=decrypt_password(p.encrypted_password),
        )
        for p in results
    ]

    return PasswordsResponse(data=passwords, count=count)
