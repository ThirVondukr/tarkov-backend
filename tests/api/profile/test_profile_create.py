import uuid
from pathlib import Path

import httpx
import orjson
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.models import Account
from utils import generate_id

endpoint_url = "/client/game/profile/create"

pytestmark = [pytest.mark.usefixtures("profile_dir", "freeze_time")]


@pytest.fixture(params=["Usec", "Bear"])
def side(request) -> str:
    return request.param


@pytest.fixture
def nickname() -> str:
    return str(uuid.uuid4())


@pytest.fixture
def head_id() -> str:
    return generate_id()


@pytest.fixture
def voice_id():
    return generate_id()


@pytest.fixture
async def response(
    authenticated_http_client: httpx.AsyncClient,
    account: Account,
    side: str,
    nickname: str,
    head_id: str,
    voice_id: str,
):
    return await authenticated_http_client.post(
        endpoint_url,
        json={
            "side": side,
            "nickname": nickname,
            "headId": head_id,
            "voiceId": voice_id,
        },
    )


async def test_should_update_account_model(
    session: AsyncSession,
    account: Account,
    response: httpx.Response,
    nickname: str,
):
    await session.refresh(account)

    assert response.status_code == status.HTTP_200_OK
    assert account.profile_nickname == nickname
    assert account.should_wipe is False


async def test_should_create_profile_file(
    response: httpx.Response,
    profile_dir: Path,
    account: Account,
    nickname: str,
    freeze_time: float,
    head_id: str,
    voice_id: str,
):
    character_path = profile_dir.joinpath("character.json")
    assert character_path.exists()
    with character_path.open(encoding="utf8") as f:
        character = orjson.loads(f.read())

    assert character["_id"] == f"pmc{account.profile_id}"
    assert character["aid"] == account.profile_id
    assert character["savage"] == f"scav{account.profile_id}"

    assert character["Info"]["Nickname"] == nickname
    assert character["Info"]["LowerNickname"] == nickname.lower()

    assert character["Info"]["Voice"] == voice_id
    assert character["Info"]["RegistrationDate"] == int(freeze_time)

    assert character["Customization"]["Head"] == head_id
