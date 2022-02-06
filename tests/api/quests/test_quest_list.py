import httpx
import orjson
import pytest
from starlette import status

import paths

endpoint_url = "/client/quest/list"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_quests_file(response: httpx.Response):
    path = paths.database.joinpath("quests", "quests.json")
    expected = orjson.loads(path.read_text(encoding="utf8"))
    assert response.json()["data"] == expected
