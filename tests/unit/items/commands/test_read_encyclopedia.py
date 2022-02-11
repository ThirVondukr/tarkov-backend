import copy

import pytest

from modules.items.actions import ReadEncyclopedia
from modules.items.commands import ReadEncyclopediaCommand


@pytest.fixture
def command():
    return ReadEncyclopediaCommand({})


async def test_empty(command):
    before = copy.deepcopy(command.encyclopedia)
    await command.execute(
        ReadEncyclopedia(
            ids=[],
        )
    )
    assert command.encyclopedia == before


async def test_single(command):
    await command.execute(ReadEncyclopedia(ids=["1"]))
    assert command.encyclopedia == {"1": True}


async def test_multiple(command):
    ids = [str(i) for i in range(100)]
    await command.execute(ReadEncyclopedia(ids=ids))
    assert command.encyclopedia == {id_: True for id_ in ids}
