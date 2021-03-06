from pathlib import Path

import httpx
import orjson
import pytest
from starlette import status

from modules.profile.types import Profile

url = "/client/game/profile/list"


async def test_no_session_id(
    http_client: httpx.AsyncClient,
):
    """
    Should raise 401 Unauthorized if no session_id is provided
    """
    response = await http_client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_profile_is_not_created_yet(authenticated_http_client: httpx.AsyncClient):
    """
    Should return empty list if profile is not yet created
    """
    response = await authenticated_http_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []


@pytest.mark.usefixtures("create_profile")
async def test_returns_profile_if_exists(
    authenticated_http_client: httpx.AsyncClient,
    profile_dir: Path,
):
    response = await authenticated_http_client.post(url)

    path = profile_dir.joinpath("character.json")
    character = Profile.parse_file(path).json(by_alias=True, exclude_unset=True)
    assert response.json()["data"] == [orjson.loads(character)]
