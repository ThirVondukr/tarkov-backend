from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from modules.items.types import Location


class ReadEncyclopedia(BaseModel):
    Action: Literal["ReadEncyclopedia"] = "ReadEncyclopedia"
    ids: list[str]


class To(BaseModel):
    id: str
    container: str = Field(description="Item.slot_id")
    location: Location


class Move(BaseModel):
    Action: Literal["Move"]
    item: str
    to: To


Action = Annotated[Union[ReadEncyclopedia, Move], Field(discriminator="Action")]
