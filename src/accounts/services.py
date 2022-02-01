from typing import Optional

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
        model: schema.AccountCreate,
    ) -> Account:
        account = Account(
            username=model.username,
            password=model.password,
            edition=model.edition,
        )
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def login(self, model: schema.AccountLogin) -> Optional[Account]:
        stmt = select(Account).filter(
            Account.username == model.username,
            Account.password == model.password,
        )
        account: Optional[Account] = await self.session.scalar(stmt)
        return account

    async def is_username_taken(self, username: str) -> bool:
        stmt = select(select(Account).filter(Account.username == username).exists())
        exists: bool = await self.session.scalar(stmt)
        return exists
