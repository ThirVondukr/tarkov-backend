import operator

import httpx
import pytest
from starlette import status

from modules.trading.manager import TraderManager


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/trading/api/traderSettings")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_list_of_trader_bases(
    trader_manager: TraderManager,
    response: httpx.Response,
):
    expected = [trader.base for trader in trader_manager.traders.values()]

    expected.sort(key=operator.itemgetter("_id"))
    assert response.json()["data"] == expected
