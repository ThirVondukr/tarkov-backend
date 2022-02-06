from operator import itemgetter

import httpx
import orjson
import pytest
from starlette import status

import paths

endpoint_url = "/client/hideout/production/recipes"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_list_of_recipes(response: httpx.Response):
    recipe_paths = paths.database.joinpath("hideout", "production").rglob("*.json")
    expected = [orjson.loads(path.read_text(encoding="utf8")) for path in recipe_paths]
    expected = sorted(expected, key=itemgetter("_id"))
    data = sorted(response.json()["data"], key=itemgetter("_id"))

    assert data == expected
