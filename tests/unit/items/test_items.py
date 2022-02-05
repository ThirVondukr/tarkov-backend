from pathlib import Path

import orjson
import pydantic
import pytest

import paths
from modules.items.types import Item


@pytest.fixture(
    params=[
        d for d in paths.database.joinpath("starting_profiles").iterdir() if d.is_dir()
    ]
)
def starting_profile_dir(request) -> Path:
    return request.param


def test_can_parse_starting_profile_items(starting_profile_dir):
    starting_inventories = [
        starting_profile_dir.joinpath("inventory_bear.json"),
        starting_profile_dir.joinpath("inventory_usec.json"),
    ]
    for inventory in starting_inventories:
        with inventory.open(encoding="utf8") as file:
            contents = orjson.loads(file.read())

        pydantic.parse_obj_as(list[Item], contents["items"])
