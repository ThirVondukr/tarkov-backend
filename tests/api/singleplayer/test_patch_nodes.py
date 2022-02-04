import httpx
import pytest
import yaml
from starlette import status
from yaml import CSafeLoader

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.get("/mode/offlineNodes")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_patch_nodes_file(response: httpx.Response):
    with paths.config.joinpath("patch_nodes.yml").open(encoding="utf8") as f:
        expected = yaml.load(f, Loader=CSafeLoader)
    assert response.json() == expected
