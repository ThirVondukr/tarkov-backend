import httpx
import pytest
import yaml
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.get("/mode/offline")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_contents_of_patches_file(response: httpx.Response):
    with paths.resources.joinpath("config", "patches.yml").open() as f:
        expected = yaml.safe_load(f)
    assert response.json() == expected
