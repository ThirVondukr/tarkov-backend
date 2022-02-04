from fastapi import APIRouter, Depends

from modules.items.repository import TemplateRepository
from modules.items.types import Template
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

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
