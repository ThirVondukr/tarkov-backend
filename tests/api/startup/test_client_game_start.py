from unittest import mock

import httpx
import pytest
from fastapi import status

return_time = 1643561156.3655324


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    with mock.patch("time.time", return_value=return_time):
        return await http_client.post("/client/game/start")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_current_time(response: httpx.Response):
    assert response.json()["data"] == {"utc_time": int(return_time / 1000)}
