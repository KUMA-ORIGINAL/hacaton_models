from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from models import User


async def get_user(db_session: AsyncSession, user_id: int):
    user = (await db_session.scalars(select(User).where(User.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_users(db_session: AsyncSession, skip: int = 0, limit: int = 100):
    # users = await db_session.scalars(select(User))
    users = await User.select().offset(skip).limit(limit).all()
    return users


async def create_user(db_session: AsyncSession, user: schemas.UserCreate):
    db_user = User(
        tg_username=user.tg_username,
        tg_first_name=user.tg_first_name,
        tg_last_name=user.tg_last_name,
        phone_number=user.phone_number,
        email=user.email)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user
