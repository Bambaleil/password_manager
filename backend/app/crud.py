from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import encrypt_password
from app.models import Password


async def get_password_by_service_name(
    session: AsyncSession, service_name: str
) -> Optional[Password]:
    result = await session.execute(
        select(Password).where(Password.service_name == service_name)
    )
    return result.scalars().first()


async def create_password(
    session: AsyncSession, service_name: str, password: str
) -> Password:
    encrypted_password = encrypt_password(password)
    db_password = Password(
        service_name=service_name, encrypted_password=encrypted_password
    )
    session.add(db_password)
    await session.commit()
    await session.refresh(db_password)
    return db_password


async def update_password(
    session: AsyncSession, db_password: Password, new_password: str
) -> Password:
    db_password.encrypted_password = encrypt_password(new_password)
    session.add(db_password)
    await session.commit()
    await session.refresh(db_password)
    return db_password


async def search_passwords_by_service_name(
    session: AsyncSession, service_name: str, skip: int = 0, limit: int = 0
) -> tuple[list[Password], int]:
    filter_condition = Password.service_name.ilike(  # type: ignore
        f"%{service_name}%"
    )

    count_stmt = (
        select(func.count()).select_from(Password).where(filter_condition)
    )
    count_result = await session.execute(count_stmt)
    count = count_result.scalar_one()

    query = select(Password).where(filter_condition).offset(skip)

    if limit > 0:
        query = query.limit(limit)

    result = await session.execute(query)
    passwords = result.scalars().all()

    return passwords, count
