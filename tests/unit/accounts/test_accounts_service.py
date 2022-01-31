import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.schema import AccountCreate
from accounts.services import AccountService
from database.models import Account


@pytest.fixture
def account_service(session):
    return AccountService(session=session)


async def test_taken_username(
    account_service: AccountService,
    session: AsyncSession,
):
    account = Account(username="username", password="password", edition="Standard")
    session.add(account)
    await session.commit()
    await session.refresh(account)

    assert await account_service.is_username_taken(account.username)


async def test_not_taken_username(
    account_service: AccountService,
):
    for _ in range(10):
        assert not await account_service.is_username_taken(str(uuid.uuid4()))


async def test_can_create_account(
    account_service: AccountService,
    session: AsyncSession,
):
    account_in = AccountCreate(
        username="username", password="password", edition="Standard"
    )
    account = await account_service.create_account(account_in)
    assert account

    account_in_db = await session.get(Account, account.id)
    assert account is account_in_db
