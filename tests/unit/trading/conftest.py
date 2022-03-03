import pytest

import paths


@pytest.fixture
def trader_ids() -> list[str]:
    return list(path.stem for path in paths.traders.iterdir())
