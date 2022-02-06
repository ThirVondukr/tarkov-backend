import httpx
import orjson
import pytest
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/account/customization")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_list_of_all_item_ids(response: httpx.Response):
    ids = []
    customization_files = paths.customization.glob("*.json")
    for file in customization_files:
        with file.open() as f:
            contents = orjson.loads(f.read())
            if contents["_type"] == "Item":
                ids.append(contents["_id"])

    assert sorted(response.json()["data"]) == sorted(ids)
