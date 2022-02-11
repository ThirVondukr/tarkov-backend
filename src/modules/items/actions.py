from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


class ReadEncyclopedia(BaseModel):
    Action: Literal["ReadEncyclopedia"] = "ReadEncyclopedia"
    ids: list[str]


class Move(BaseModel):
    class To(BaseModel):
        id: str
        container: str
        location: dict

    Action: Literal["Move"]
    item: str
    to: To


Action = Annotated[Union[ReadEncyclopedia, Move], Field(discriminator="Action")]
