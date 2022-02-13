from typing import Annotated

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.models import Account
from modules.profile.dependencies import get_profile_id


@inject
async def get_account(
    session: Annotated[AsyncSession, Inject],
    profile_id: str = Depends(get_profile_id),
) -> Account:
    stmt = select(Account).filter(Account.profile_id == profile_id)
    account: Account = await session.scalar(stmt)
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return account
