import uuid
import zlib

import httpx
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Account

endpoint_url = "/launcher/profile/register"


async def test_taken_username(
    http_client: httpx.AsyncClient,
    session: AsyncSession,
):
    """
    Endpoint should return "FAILED" if username is taken
    """

    account = Account(
        username=str(uuid.uuid4()),
        password="password",
        edition="Standard",
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)

    response = await http_client.post(
        endpoint_url,
        json={
            "email": account.username,
            "password": "",
            "edition": "",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert zlib.decompress(response.content) == b"FAILED"


async def test_create_account(
    http_client: httpx.AsyncClient,
    session: AsyncSession,
):
    username = str(uuid.uuid4())
    response = await http_client.post(
        endpoint_url,
        json={"email": username, "password": "password", "edition": "Standard"},
    )
    assert zlib.decompress(response.content) == b"OK"

    stmt = select(Account).filter(Account.username == username)
    account = await session.scalar(stmt)
    assert account is not None
    assert account.username == username
