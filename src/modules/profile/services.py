from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import paths
from database.dependencies import get_session
from database.models import Account


class ProfileService:
    starting_profiles_path = paths.database.joinpath("starting_profiles")
    profiles_path = paths.profiles

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def is_nickname_taken(self, nickname: str) -> bool:
        stmt = select(
            select(Account).filter(Account.profile_nickname == nickname).exists()
        )
        username_taken: bool = await self.session.scalar(stmt)
        return username_taken
