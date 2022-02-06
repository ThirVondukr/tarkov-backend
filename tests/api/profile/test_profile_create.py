import uuid
from pathlib import Path

import httpx
import orjson
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import paths
from database.models import Account
from utils import generate_id

endpoint_url = "/client/game/profile/create"

pytestmark = [pytest.mark.usefixtures("profile_dir")]


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


def test_should_create_profile_file(
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


def test_should_add_inventory(
    response: httpx.Response,
    profile_dir: Path,
    account: Account,
    side: str,
):
    starting_inventory_path = paths.database.joinpath(
        "starting_profiles",
        account.edition,
        f"inventory_{side.lower()}.json",
    )
    with starting_inventory_path.open(encoding="utf8") as f:
        starting_inventory = orjson.loads(f.read())

    with profile_dir.joinpath("character.json").open(encoding="utf8") as f:
        character = orjson.loads(f.read())
    inventory = character["Inventory"]

    exclude_keys = ("_id", "parentId")

    assert len(starting_inventory["items"]) == len(inventory["items"])
    for starting_item, item in zip(starting_inventory["items"], inventory["items"]):
        assert starting_item["_id"] != item["_id"]
        if "parentId" in starting_item or "parentId" in item:
            assert starting_item["parentId"] != item["parentId"]

        starting_item = {
            k: v for k, v in starting_item.items() if k not in exclude_keys
        }
        item = {k: v for k, v in item.items() if k not in exclude_keys}
        assert starting_item == item

    all_ids = set(item["_id"] for item in inventory["items"])
    assert inventory["equipment"] in all_ids
    assert inventory["questRaidItems"] in all_ids
    assert inventory["questStashItems"] in all_ids
    assert inventory["sortingTable"] in all_ids
    assert inventory["stash"] in all_ids
