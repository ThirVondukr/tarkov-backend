import asyncio
import contextlib
import shutil
import uuid
from collections import defaultdict
from typing import AsyncIterator

import aiofiles
import orjson
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import paths
from database.dependencies import get_session
from database.models import Account
from utils import Singleton, read_json_file

from .types import Profile


class ProfileService:
    starting_profiles_path = paths.database.joinpath("starting_profiles")

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def is_nickname_taken(self, nickname: str) -> bool:
        stmt = select(
            select(Account).filter(Account.profile_nickname == nickname).exists()
        )
        username_taken: bool = await self.session.scalar(stmt)
        return username_taken


class _ProfileManager:
    profiles_path = paths.profiles

    def __init__(self) -> None:
        self.profiles: dict[str, Profile] = {}
        self.locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def _read_profile(self, profile_id: str) -> Profile:
        path = self.profiles_path.joinpath(profile_id, "character.json")
        profile = await read_json_file(path)
        return Profile.parse_obj(profile)

    async def _save_profile(self, profile_id: str, profile: Profile) -> None:
        profile_dir = self.profiles_path.joinpath(profile_id)
        profile_data = profile.dict(by_alias=True)

        temp_path = profile_dir.joinpath(str(uuid.uuid4()))
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(temp_path, "wb") as file:
            await file.write(orjson.dumps(profile_data))

        shutil.copy(temp_path, profile_dir.joinpath("character.json"))
        temp_path.unlink()

    @contextlib.asynccontextmanager
    async def profile(
        self,
        profile_id: str,
        readonly: bool = False,
    ) -> AsyncIterator[Profile]:
        async with self.locks[profile_id]:
            if profile_id not in self.profiles:  # pragma: no branch
                self.profiles[profile_id] = await self._read_profile(profile_id)

            profile = self.profiles[profile_id]
            try:
                yield profile

                if not readonly:  # pragma: no branch
                    await self._save_profile(
                        profile_id=profile_id,
                        profile=profile,
                    )
            except Exception:
                del self.profiles[profile_id]
                raise


class ProfileManager(_ProfileManager, Singleton):
    pass
