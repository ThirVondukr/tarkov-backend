import httpx
import orjson
import pytest
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/settings")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_client_settings_file(response: httpx.Response):
    with paths.base.joinpath("client_settings.json").open(encoding="utf8") as f:
        expected = orjson.loads(f.read())

    assert response.json()["data"] == expected
