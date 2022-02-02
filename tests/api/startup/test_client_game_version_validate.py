import httpx
import pytest
from fastapi import status

endpoint_url = "/client/game/version/validate"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_status_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_body_is_empty(response: httpx.Response):
    assert response.json() == {"data": None, "err": 0, "errmsg": None}
