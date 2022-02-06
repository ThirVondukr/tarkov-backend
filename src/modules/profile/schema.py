from typing import Literal

from pydantic import BaseModel, Field

import utils


class ProfileCreate(BaseModel, alias_generator=utils.camel):
    side: Literal["Usec", "Bear"]
    nickname: str
    head_id: str
    voice_id: str


class ProfileSelect(BaseModel, allow_population_by_field_name=True):
    class Notifier(BaseModel, allow_population_by_field_name=True):
        server: str
        channel_id: str
        url: str
        notifier_server: str = Field(alias="notifierServer")
        ws: str

    notifier_server: str = Field(alias="notifierServer")
    notifier: Notifier
