from typing import Literal

from pydantic import BaseModel

import utils


class ProfileCreate(BaseModel, alias_generator=utils.camel):
    side: Literal["Usec", "Bear"]
    nickname: str
    head_id: str
    voice_id: str
