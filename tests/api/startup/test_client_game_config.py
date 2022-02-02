import uuid

import httpx
import pytest
from fastapi import status

endpoint_url = "/client/game/config"


@pytest.fixture
def session_id() -> str:
    return str(uuid.uuid4())


@pytest.fixture
async def response(
    http_client: httpx.AsyncClient,
    session_id: str,
) -> httpx.Response:
    return await http_client.post(endpoint_url, cookies={"PHPSESSID": session_id})


def test_status_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_backend_urls(response: httpx.Response):
    expected_url = "https://test:443"
    assert response.json()["data"]["backend"] == {
        "Main": expected_url,
        "Messaging": expected_url,
        "RagFair": expected_url,
        "Trading": expected_url,
    }


def test_ids(response: httpx.Response, session_id: str):
    data = response.json()["data"]
    assert data["aid"] == session_id
    assert data["token"] == session_id
    assert data["activeProfileId"] == f"user{session_id}pmc"
