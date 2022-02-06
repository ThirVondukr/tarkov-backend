from operator import itemgetter

import httpx
import orjson
import pytest
from starlette import status

import paths

endpoint_url = "/client/hideout/areas"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_list_of_all_areas(response: httpx.Response):
    areas = []
    for path in paths.database.joinpath("hideout", "areas").rglob("*.json"):
        with path.open(encoding="utf8") as f:
            areas.append(orjson.loads(f.read()))

    expected = sorted(areas, key=itemgetter("_id"))
    data = sorted(response.json()["data"], key=itemgetter("_id"))
    assert data == expected
