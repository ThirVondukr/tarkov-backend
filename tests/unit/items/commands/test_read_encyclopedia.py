import copy

from modules.items import handlers
from modules.items.actions import ReadEncyclopedia
from modules.items.handlers import Context


async def test_empty(context: Context):
    before = copy.deepcopy(context.profile.encyclopedia)
    await handlers.read_encyclopedia(
        ReadEncyclopedia(
            ids=[],
        ),
        context,
    )
    assert context.profile.encyclopedia == before


async def test_single(context: Context):
    context.profile.encyclopedia = {}
    await handlers.read_encyclopedia(ReadEncyclopedia(ids=["1"]), context)
    assert context.profile.encyclopedia == {"1": True}


async def test_multiple(context: Context):
    context.profile.encyclopedia = {}
    ids = [str(i) for i in range(100)]
    await handlers.read_encyclopedia(ReadEncyclopedia(ids=ids), context)
    assert context.profile.encyclopedia == {id_: True for id_ in ids}
