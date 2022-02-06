from operator import itemgetter

import httpx
import orjson
import pytest
from starlette import status

import paths

endpoint_url = "/client/hideout/production/scavcase/recipes"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_list_of_scavcase_recipes(response: httpx.Response):
    recipe_paths = paths.database.joinpath("hideout", "scavcase").rglob("*.json")
    expected = [orjson.loads(p.read_text(encoding="utf8")) for p in recipe_paths]
    expected.sort(key=itemgetter("_id"))

    data = response.json()["data"]
    data.sort(key=itemgetter("_id"))

    assert data == expected
