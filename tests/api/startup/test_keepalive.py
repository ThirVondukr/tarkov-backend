import httpx
import pytest
from starlette import status


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/game/keepalive")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_body(response: httpx.Response):
    assert response.json() == {"err": 0, "errmsg": None, "data": {"msg": "ok"}}
