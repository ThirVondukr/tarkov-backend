from pathlib import Path

import pytest

import paths
from database.models import Account
from modules.profile.services import _ProfileManager


@pytest.fixture
def profile_manager() -> _ProfileManager:
    return _ProfileManager()


@pytest.fixture
def profile_path(account: Account) -> Path:
    return paths.profiles.joinpath(account.profile_id, "character.json")
