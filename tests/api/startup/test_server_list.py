import httpx
import pytest
from starlette import status

endpoint_url = "/client/server/list"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_server_info(response: httpx.Response, base_url):
    expected = {
        "ip": f"{base_url}:443",
        "port": 443,
    }
    assert response.json()["data"] == expected
