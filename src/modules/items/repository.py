from __future__ import annotations

import itertools
from pathlib import Path

import orjson
import pydantic

import paths
from utils import Singleton

from .types import Template


class TemplateRepository(Singleton):
    path = paths.items

    def __init__(self) -> None:
        self.templates = self._load_files(self.path)

    @staticmethod
    def _load_files(path: Path) -> dict[str, Template]:
        files = []
        for item_file in path.glob("*.json"):
            with item_file.open(encoding="utf8") as f:
                files.append(orjson.loads(f.read()))
        templates = list(itertools.chain.from_iterable(files))
        templates = pydantic.parse_obj_as(list[Template], templates)
        return {tpl.id: tpl for tpl in templates}
