import time

import aiofiles
from fastapi import Depends
import orjson
from sqlalchemy.ext.asyncio import AsyncSession

import paths
from database.dependencies import get_session
from database.models import Account
from modules.profile.schema import ProfileCreate
from modules.profile.services import ProfileService
from modules.profile.types import Profile


class ProfileCreateCommand:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        profile_service: ProfileService = Depends(),
    ) -> None:
        self.session = session
        self.profile_service = profile_service

    async def execute(
        self,
        account: Account,
        profile_create: ProfileCreate,
    ) -> None:
        character = await self._create_character(account, profile_create)

        account.profile_nickname = profile_create.nickname
        account.should_wipe = False
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)

        profile_path = paths.profiles.joinpath(account.profile_id)
        profile_path.mkdir(exist_ok=True)
        with profile_path.joinpath("character.json").open("wb") as f:
            f.write(orjson.dumps(character.dict(by_alias=True)))

    async def _create_character(
        self, account: Account, profile_create: ProfileCreate
    ) -> Profile:
        starting_character = paths.database.joinpath(
            "starting_profiles", account.edition, "character.json"
        )
        async with aiofiles.open(starting_character, encoding="utf8") as f:
            character = Profile.parse_obj(orjson.loads(await f.read()))

        character.aid = account.profile_id
        character.id = f"pmc{account.profile_id}"
        character.savage = f"scav{account.profile_id}"

        character.info.nickname = profile_create.nickname
        character.info.lower_nickname = profile_create.nickname.lower()
        character.info.side = profile_create.side

        character.info.voice = profile_create.voice_id
        character.customization.head = profile_create.head_id

        character.info.registration_date = int(time.time())

        return character
