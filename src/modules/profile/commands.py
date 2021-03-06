import time
from typing import Annotated

import aiofiles
import orjson
from aioinject import Inject
from sqlalchemy.ext.asyncio import AsyncSession

import paths
from database.models import Account
from modules.profile.schema import ProfileCreate
from modules.profile.services import ProfileService
from modules.profile.types import Profile
from utils import generate_id


class ProfileCreateCommand:
    def __init__(
        self,
        session: Annotated[AsyncSession, Inject],
        profile_service: Annotated[ProfileService, Inject],
    ) -> None:
        self.session = session
        self.profile_service = profile_service

    async def execute(
        self,
        account: Account,
        profile_create: ProfileCreate,
    ) -> Profile:
        character = await self._create_character(account, profile_create)

        account.profile_nickname = profile_create.nickname
        account.should_wipe = False
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)

        profile_path = paths.profiles.joinpath(account.profile_id)
        profile_path.mkdir(exist_ok=True)
        async with aiofiles.open(profile_path.joinpath("character.json"), "wb") as file:
            await file.write(
                orjson.dumps(character.dict(by_alias=True, exclude_unset=True))
            )

        return character

    async def _create_character(
        self, account: Account, profile_create: ProfileCreate
    ) -> Profile:
        starting_character = paths.database.joinpath(
            "starting_profiles", account.edition, "character.json"
        )
        async with aiofiles.open(starting_character, encoding="utf8") as f:
            data = orjson.loads(await f.read())
            data["Inventory"] = await self._starting_inventory(
                account.edition, profile_create.side
            )
            character = Profile.parse_obj(data)

        character.aid = account.profile_id
        character.id = f"pmc{account.profile_id}"
        character.savage = f"scav{account.profile_id}"

        character.info.nickname = profile_create.nickname
        character.info.lower_nickname = profile_create.nickname.lower()
        character.info.side = profile_create.side

        character.info.voice = profile_create.voice_id
        character.customization.head = profile_create.head_id

        character.info.registration_date = str(int(time.time()))

        return character

    async def _starting_inventory(self, edition: str, side: str) -> dict:
        path = paths.database.joinpath(
            "starting_profiles", edition, f"inventory_{side.lower()}.json"
        )
        async with aiofiles.open(path) as f:
            inventory = orjson.loads(await f.read())
            self._regenerate_inventory(inventory)
            assert isinstance(inventory, dict)
            return inventory

    @staticmethod
    def _regenerate_inventory(inventory: dict) -> None:
        ids_map = {}
        for item in inventory["items"]:
            new_id = generate_id()
            ids_map[item["_id"]] = new_id
            item["_id"] = new_id

        for item in inventory["items"]:
            if "parentId" not in item:
                continue
            item["parentId"] = ids_map[item["parentId"]]

        keys = [
            "equipment",
            "questRaidItems",
            "questStashItems",
            "sortingTable",
            "stash",
        ]
        for key in keys:
            inventory[key] = ids_map[inventory[key]]
