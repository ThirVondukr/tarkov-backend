from pathlib import Path

import httpx
import pytest
from fastapi import status


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.get("/launcher/server/connect")


@pytest.fixture
async def response_json(response: httpx.Response) -> dict:
    return response.json()


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_contain_server_name(
    server_name,
    response_json: dict,
):
    assert response_json["name"] == server_name


def test_backend_url(response_json, base_url):
    assert response_json["backendUrl"] == base_url


def test_edition_list(response_json: dict):
    starting_profiles_dir = Path("resources/database/starting_profiles").glob("*")
    available_editions = sorted(d.name for d in starting_profiles_dir)
    assert response_json["editions"] == available_editions
