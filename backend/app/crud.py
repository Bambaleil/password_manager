from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import get_password_hash
from app.models import Password


async def get_password_by_service_name(session: AsyncSession, service_name: str) -> Optional[Password]:
    result = await session.execute(
        select(Password).where(Password.service_name == service_name)
    )
    return result.scalars().first()


async def create_password(session: AsyncSession, service_name: str, password: str) -> Password:
    hashed_password = get_password_hash(password)
    db_password = Password(
        service_name=service_name,
        hashed_password=hashed_password
    )
    session.add(db_password)
    await session.commit()
    await session.refresh(db_password)
    return db_password


async def update_password(session: AsyncSession, db_password: Password, new_password: str) -> Password:
    db_password.hashed_password = get_password_hash(new_password)
    session.add(db_password)
    await session.commit()
    await session.refresh(db_password)
    return db_password
