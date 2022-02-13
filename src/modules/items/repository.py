from __future__ import annotations

import itertools
from pathlib import Path
from typing import Iterable

import orjson
import pydantic

import paths

from .types import Template


async def create_template_repository(path: Path = paths.items) -> TemplateRepository:
    files = []
    for item_file in path.glob("*.json"):
        with item_file.open(encoding="utf8") as f:
            files.append(orjson.loads(f.read()))

    templates = list(itertools.chain.from_iterable(files))
    templates = pydantic.parse_obj_as(list[Template], templates)
    return TemplateRepository({tpl.id: tpl for tpl in templates})


class TemplateRepository:
    def __init__(self, templates: dict[str, Template]) -> None:
        self.templates = templates

    def get(self, template_id: str) -> Template:
        return self.templates[template_id]

    def find(
        self,
        name: str | None = None,
    ) -> Template:
        templates: Iterable[Template] = self.templates.values()
        if name is not None:
            templates = filter(lambda tpl: tpl.name == name, templates)

        templates_list = list(templates)

        if len(templates_list) == 0:
            raise ValueError("No items found")

        return templates_list[0]

    def container_size(self, template_id: str, slot: str) -> tuple[int, int]:
        container_tpl = self.get(template_id)
        grid = next(
            grid for grid in container_tpl.props["Grids"] if grid["_name"] == slot
        )
        return grid["_props"]["cellsH"], grid["_props"]["cellsV"]
