import httpx
import pytest
from starlette import status

endpoint_url = "/client/game/profile/select"


@pytest.fixture
async def response(authenticated_http_client: httpx.AsyncClient) -> httpx.Response:
    return await authenticated_http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_server_data(response: httpx.Response, base_url: str):
    expected = {
        "notifierServer": "",
        "notifier": {
            "server": f"{base_url}:443",
            "channel_id": "testChannel",
            "url": "",
            "notifierServer": "",
            "ws": "",
        },
    }
    assert response.json()["data"] == expected
