import uuid
from pathlib import Path

import pytest

import paths
from database.models import Account
from modules.profile.services import ProfileManager
from modules.profile.types import Profile
from tests.utils import tmp_dir
from utils import generate_id, read_json_file

pytestmark = [pytest.mark.usefixtures("profile")]


async def test_read(
    profile_manager: ProfileManager,
    account: Account,
    profile_path: Path,
):
    profile = await profile_manager._read_profile(account.profile_id)
    assert isinstance(profile, Profile)

    expected = Profile.parse_file(profile_path)
    assert profile == expected


async def test_save(
    profile_manager: ProfileManager,
    account: Account,
    profile_path: Path,
):
    previous_profile = await read_json_file(profile_path)
    profile = await profile_manager._read_profile(account.profile_id)

    new_profile_id = generate_id()
    expected_path = paths.profiles.joinpath(new_profile_id, "character.json")
    with tmp_dir(expected_path.parent):
        await profile_manager._save_profile(new_profile_id, profile)
        assert expected_path.exists()

        saved_profile = await read_json_file(expected_path)
    for k, v in previous_profile.items():
        assert saved_profile[k] == v


async def test_context_manager_read(
    profile_manager: ProfileManager,
    account: Account,
    profile_path: Path,
):
    assert account.profile_id not in profile_manager.profiles
    async with profile_manager.profile(account.profile_id) as profile:
        assert profile == Profile.parse_file(profile_path)


async def test_context_manager_save(
    profile_manager: ProfileManager,
    account: Account,
    profile_path: Path,
):
    async with profile_manager.profile(account.profile_id) as profile:
        profile.id = "New id"

    profile_on_disk = Profile.parse_file(profile_path)
    assert profile == profile_on_disk
    assert profile.id == profile_on_disk.id == "New id"


async def test_context_manager_should_not_save_on_exception(
    profile_manager: ProfileManager,
    account: Account,
    profile_path: Path,
):
    test_id = str(uuid.uuid4())
    profile_before = Profile.parse_file(profile_path)

    with pytest.raises(Exception):
        async with profile_manager.profile(account.profile_id) as profile:
            profile.id = test_id
            raise Exception

    assert Profile.parse_file(profile_path) == profile_before

    async with profile_manager.profile(account.profile_id) as profile:
        assert profile.id != test_id
