from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dependencies import get_session
from database.models import Account

from . import schema


class AccountService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_account(
        self,
        account_in: schema.AccountCreate,
    ) -> Account:
        account = Account(
            username=account_in.username,
            password=account_in.password,
            edition=account_in.edition,
        )
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def is_username_taken(self, username: str) -> bool:
        stmt = select(select(Account).filter(Account.username == username).exists())
        exists: bool = await self.session.scalar(stmt)
        return exists
