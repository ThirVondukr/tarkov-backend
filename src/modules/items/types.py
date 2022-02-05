import enum
from typing import Any, Literal, Optional

import pydantic
from pydantic import BaseModel, Extra, Field

import utils


class Template(
    BaseModel,
    alias_generator=utils.underscore_prefix,
    extra=Extra.forbid,
):
    id: str
    name: str
    parent: str
    type: Literal["Item", "Node"]
    props: dict[str, Any]
    proto: Optional[str]


class Rotation(enum.Enum):
    Horizontal = 0
    Vertical = 1


class Location(BaseModel):
    class Config:
        extra = Extra.forbid
        use_enum_values = True

    is_searched: bool = Field(alias="isSearched", default=False)
    rotation: Rotation = Field(alias="r", default=Rotation.Horizontal)
    x: int
    y: int

    @pydantic.validator("rotation", pre=True, always=True)
    def coerce_to_enum(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        return Rotation[value]


class Item(BaseModel):
    id: str = Field(alias="_id")
    template_id: str = Field(alias="_tpl")
    parent_id: str | None = Field(alias="parentId")
    slot_id: str | None = Field(alias="slotId")
    location: Location | int | None
    upd: dict = Field(default_factory=dict)
