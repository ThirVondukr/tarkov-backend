import httpx
import pytest
from fastapi import status

from database.models import Account


@pytest.fixture
async def response(
    http_client: httpx.AsyncClient,
    account: Account,
):
    return await http_client.post(
        "/launcher/profile/get",
        json={
            "email": account.username,
            "password": account.password,
        },
    )


def test_status_ok(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_profile(response: httpx.Response, account: Account):
    expected = {
        "id": account.id,
        "nickname": account.username,
        "email": account.username,
        "password": account.password,
        "edition": account.edition,
        "wipe": account.should_wipe,
    }
    assert response.json() == expected
