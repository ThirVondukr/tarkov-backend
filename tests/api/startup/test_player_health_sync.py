import httpx
import pytest
from starlette import status

endpoint_url = "/player/health/sync"


# async def test_unauthenticated(http_client: httpx.AsyncClient):
#     response = await http_client.post(endpoint_url)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
async def response(authenticated_http_client: httpx.AsyncClient) -> httpx.Response:
    return await authenticated_http_client.post(endpoint_url)


def test_status_ok(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_none(response: httpx.Response):
    assert response.json()["data"] is None
