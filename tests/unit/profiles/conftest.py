from pathlib import Path

import pytest

import paths
from database.models import Account
from modules.profile.services import ProfileManager


@pytest.fixture
def profile_manager() -> ProfileManager:
    return ProfileManager()


@pytest.fixture
def profile_path(account: Account) -> Path:
    return paths.profiles.joinpath(account.profile_id, "character.json")
