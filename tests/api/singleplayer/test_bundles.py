import httpx
import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def response(http_client: AsyncClient) -> httpx.Response:
    return await http_client.get("/singleplayer/bundles")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_empty_list(response: httpx.Response):
    assert response.json() == []
