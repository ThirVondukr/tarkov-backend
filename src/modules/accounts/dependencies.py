from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.dependencies import get_session
from database.models import Account
from modules.profile.dependencies import get_profile_id


async def get_account(
    profile_id: str = Depends(get_profile_id),
    session: AsyncSession = Depends(get_session),
) -> Account:
    stmt = select(Account).filter(Account.profile_id == profile_id)
    account = await session.scalar(stmt)
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return account
