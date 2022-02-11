from typing import Any

from pydantic import BaseModel, Extra, Field

from utils import camel, pascal


class InsuredItem(BaseModel, alias_generator=camel):
    tid: str
    item_id: str


class _BaseConfigModel(BaseModel):
    class Config:
        alias_generator = pascal
        extra = Extra.forbid
        allow_population_by_field_name = True


class Profile(_BaseConfigModel):
    class Info(_BaseConfigModel):
        nickname: str
        lower_nickname: str
        side: str
        voice: str
        level: int
        experience: int
        registration_date: str
        game_version: str
        account_type: int
        member_category: int
        locked_move_commands: bool = Field(alias="lockedMoveCommands")
        savage_lock_time: int
        last_time_played_as_savage: int
        settings: dict
        need_wipe: bool
        global_wipe: bool
        nickname_change_date: int
        bans: list

    class Customization(_BaseConfigModel):
        head: str
        body: str
        feet: str
        hands: str

    id: str = Field(alias="_id")
    aid: str = Field(alias="aid")
    savage: str = Field(alias="savage")
    info: Info
    customization: Customization
    health: dict
    inventory: Any
    skills: dict
    stats: dict
    encyclopedia: dict[str, bool]
    condition_counters: dict
    backend_counters: dict
    insured_items: list[InsuredItem]
    hideout: dict
    bonuses: list
    notes: dict
    quests: list
    traders_info: dict
    ragfair_info: dict
    wish_list: list
