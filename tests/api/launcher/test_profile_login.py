import httpx
import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Account

endpoint_url = "/launcher/profile/login"


@pytest.fixture
async def response_failed(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(
        endpoint_url,
        json={
            "email": "",
            "password": "",
        },
    )


@pytest.fixture
async def response_ok(
    http_client: httpx.AsyncClient,
    session: AsyncSession,
    account: Account,
) -> httpx.Response:
    return await http_client.post(
        endpoint_url,
        json={
            "email": account.username,
            "password": account.password,
        },
    )


async def test_failed_returns_200(response_failed: httpx.Response):
    assert response_failed.status_code == status.HTTP_200_OK


async def test_failed_response(response_failed: httpx.Response):
    assert response_failed.content == b"FAILED"


async def test_ok_response(response_ok: httpx.Response):
    assert response_ok.content == b"OK"
