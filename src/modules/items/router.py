from typing import Annotated

import orjson
import pydantic
from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Depends, Request
from starlette.background import BackgroundTasks

import paths
from modules.items.actions import AnyAction, ItemsMovingResponse
from modules.items.handlers import ActionHandler
from modules.items.repository import TemplateRepository
from modules.items.types import Template
from modules.profile.dependencies import get_profile_id
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
@inject
async def client_items(
    template_repository: Annotated[TemplateRepository, Inject],
) -> Success[dict[str, Template]]:
    return Success(data=template_repository.templates)


@router.post("/client/handbook/templates", response_model=Success[dict[str, list]])
async def handbook_templates() -> Success[dict[str, list]]:
    template_paths = paths.database.joinpath("templates").rglob("*.json")

    return Success(
        data={path.stem: await read_json_file(path) for path in template_paths}
    )


@router.post("/client/game/profile/items/moving")
@inject
async def items_moving(
    request: Request,
    executor: Annotated[ActionHandler, Inject],
    background_tasks: BackgroundTasks,
    profile_id: str = Depends(get_profile_id),
) -> Success[ItemsMovingResponse]:
    data = await request.json()
    print(orjson.dumps(data))
    actions = pydantic.parse_obj_as(list[AnyAction], data["data"])

    profile_changes = await executor.execute(
        actions=actions,
        profile_id=profile_id,
        background_tasks=background_tasks,
    )
    return Success(
        data=ItemsMovingResponse(
            profile_changes={
                profile_id: profile_changes,
            }
        )
    )
