import uuid

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Account

endpoint_url = "/client/game/profile/nickname/validate"


async def test_returns_error_if_too_short(http_client: httpx.AsyncClient):
    for i in range(4):
        response = await http_client.post(endpoint_url, content="_" * i)
        assert response.json() == {
            "data": None,
            "err": 256,
            "errmsg": "The nickname is too short",
        }


async def test_returns_error_if_taken(
    http_client: httpx.AsyncClient,
    account: Account,
    session: AsyncSession,
):
    account.profile_nickname = str(uuid.uuid4())
    session.add(account)
    await session.commit()
    await session.refresh(account)

    response = await http_client.post(endpoint_url, content=account.profile_nickname)
    assert response.json() == {
        "data": None,
        "err": 255,
        "errmsg": "The nickname is already in use",
    }


async def test_success(http_client: httpx.AsyncClient):
    response = await http_client.post(endpoint_url, content=str(uuid.uuid4()))
    assert response.json() == {"data": {"status": "ok"}, "err": 0, "errmsg": None}
