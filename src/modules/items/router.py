from fastapi import APIRouter, Depends

import paths
from modules.items.repository import TemplateRepository
from modules.items.types import Template
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute
from utils import read_json_file

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Items"],
)


@router.post(
    "/client/items",
    response_model=Success[dict[str, Template]],
    response_model_exclude_unset=True,
)
async def client_items(
    template_repository: TemplateRepository = Depends(),
) -> Success[dict[str, Template]]:
    return Success(data=template_repository.templates)


@router.post("/client/handbook/templates", response_model=Success[dict[str, list]])
async def handbook_templates() -> Success[dict[str, list]]:
    template_paths = paths.database.joinpath("templates").rglob("*.json")

    return Success(
        data={path.stem: await read_json_file(path) for path in template_paths}
    )
