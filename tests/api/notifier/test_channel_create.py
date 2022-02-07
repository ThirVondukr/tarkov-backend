import httpx
import pytest
from starlette import status

from database.models import Account

endpoint_url = "/client/notifier/channel/create"


@pytest.fixture
async def response(authenticated_http_client: httpx.AsyncClient) -> httpx.Response:
    return await authenticated_http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_notifier_info(response: httpx.Response, base_url, account: Account):
    url = f"{base_url}/client/notifier/channel/{account.profile_id}"
    expected = {
        "notifier": {
            "server": f"{base_url}:443",
            "channel_id": "testChannel",
            "url": url,
        },
        "notifierServer": url,
    }
    assert response.json()["data"] == expected
