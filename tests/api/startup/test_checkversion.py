import httpx
import pytest
from starlette import status

endpoint_url = "/client/checkVersion"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_ok(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_version_is_valid(response: httpx.Response):
    assert response.json()["data"] == {"isvalid": True, "latestVersion": ""}
