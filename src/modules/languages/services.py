from typing import Any, cast

import paths
from utils import read_json_file


class LanguageService:
    locales_dir = paths.locales

    async def languages(self) -> dict[str, str]:
        """
        Returns dictionary with available languages in short_name: name format

        :return: dict[str, str]
        """
        return {
            lang["ShortName"]: lang["Name"] for lang in await self.client_languages()
        }

    def available_languages(self) -> list[str]:
        return [path.name for path in self.locales_dir.iterdir() if path.is_dir()]

    async def menu_locale(self, language: str) -> dict[str, Any]:
        return await self._load_locale_file(language, "menu.json")

    async def client_locale(self, language: str) -> dict[str, Any]:
        return await self._load_locale_file(language, "locale.json")

    async def client_languages(self) -> list[dict[str, str]]:
        languages = []
        for language in self.available_languages():
            contents_json = await self._load_locale_file(language, f"{language}.json")
            languages.append(contents_json)
        return languages

    async def _load_locale_file(self, language: str, filename: str) -> dict[str, Any]:
        path = self.locales_dir.joinpath(language, filename)
        return cast(dict[str, Any], await read_json_file(path))
