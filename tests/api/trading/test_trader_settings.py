import httpx
import orjson
import pytest
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/trading/api/traderSettings")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_list_of_trader_bases(response: httpx.Response):
    expected = []
    for base in paths.traders.rglob("base.json"):
        with base.open(encoding="utf8") as file:
            expected.append(orjson.loads(file.read()))

    assert response.json()["data"] == expected
