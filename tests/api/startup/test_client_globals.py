import httpx
import orjson
import pytest
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/globals")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_contents_of_globals_file(response: httpx.Response):
    with paths.base.joinpath("globals.json").open(encoding="utf8") as f:
        contents = orjson.loads(f.read())
    assert response.json()["data"] == contents
