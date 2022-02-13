from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field

from modules.items.types import Item, Location
from utils import camel


class ReadEncyclopedia(BaseModel):
    Action: Literal["ReadEncyclopedia"] = "ReadEncyclopedia"
    ids: list[str]


class To(BaseModel):
    id: str
    container: str = Field(description="Item.slot_id")
    location: Location | None


class Move(BaseModel):
    Action: Literal["Move"] = "Move"
    item: str
    to: To


class Split(BaseModel):
    Action: Literal["Split"] = "Split"
    item: str
    container: To
    count: int


class Remove(BaseModel):
    Action: Literal["Remove"] = "Remove"
    item: str


Action = Annotated[
    Union[
        ReadEncyclopedia,
        Move,
        Remove,
        Split,
    ],
    Field(discriminator="Action"),
]


class ProfileChanges(BaseModel):
    class Config:
        alias_generator = camel
        allow_population_by_field_name = True

    class Items(BaseModel):
        new: list[Item] = Field(default_factory=list)
        change: list[Item] = Field(default_factory=list)
        del_: list[Item] = Field(default_factory=list, alias="del")

    experience: int = 0
    items: Items = Field(default_factory=Items)
    quests: list = Field(default_factory=list)
    rag_fair_offers: list = Field(default_factory=list)
    trader_relations: dict[str, Any] = Field(default_factory=dict)
    builds: list = Field(default_factory=list)
    production: dict[str, Any] = Field(default_factory=dict)
    skills: dict


class ItemsMovingResponse(BaseModel):
    class Config:
        alias_generator = camel
        allow_population_by_field_name = True

    warnings: list = Field(default_factory=list)
    profile_changes: dict[str, ProfileChanges]
