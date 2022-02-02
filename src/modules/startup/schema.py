from __future__ import annotations

import pydantic
from pydantic import BaseModel

import utils


class Backend(
    BaseModel,
    allow_population_by_field_name=True,
    alias_generator=utils.pascal,
):
    main: str
    messaging: str
    rag_fair: str
    trading: str

    @classmethod
    def from_root_url(cls, url: str) -> Backend:
        return cls(
            main=url,
            messaging=url,
            rag_fair=url,
            trading=url,
        )


class ClientGameConfig(
    BaseModel,
    allow_population_by_field_name=True,
    alias_generator=utils.camel,
):
    queued: bool = False
    ban_time: int = 0
    hash: str = "BAN0"
    lang: str = "en"
    nda_free: bool = False
    report_available: bool = True
    taxonomy: int = 6
    total_in_game: int = 0
    utc_time: int = pydantic.Field(default_factory=utils.timestamp, alias="utc_time")

    aid: str
    token: str
    active_profile_id: str
    nickname: str
    languages: dict[str, str]
    backend: Backend
