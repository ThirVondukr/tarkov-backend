from pydantic import BaseModel

from utils import pascal


class FriendListSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = pascal

    friends: list
    ignore: list
    in_ignore_list: list
