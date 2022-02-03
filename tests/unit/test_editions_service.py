import pytest

import paths
from modules.launcher.services import EditionsService


@pytest.fixture
def editions_service():
    return EditionsService()


def test_path(editions_service):
    assert editions_service.starting_profiles_path == paths.database.joinpath(
        "starting_profiles"
    )


def test_available_editions(editions_service):
    expected = [
        d.name
        for d in paths.database.joinpath("starting_profiles").iterdir()
        if d.is_dir()
    ]
    assert editions_service.available_editions == expected
