import httpx
import pytest
from fastapi import status

pytestmark = [pytest.mark.asyncio]


@pytest.fixture
async def response(http_client) -> httpx.Response:
    return await http_client.get("/")


async def test_status_ok(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


async def test_returns_hello_world(response: httpx.Response):
    assert response.json() == {"msg": "Hello World!"}
