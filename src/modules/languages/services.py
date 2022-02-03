from typing import Any, cast

import aiofiles
import orjson

import paths


class LanguageService:
    locales_dir = paths.locales

    async def languages(self) -> dict[str, str]:
        """
        Returns dictionary with available languages in short_name: name format

        :return: dict[str, str]
        """
        data = {}

        for language in self.available_languages():
            contents_json = await self._load_locale_file(language, f"{language}.json")
            data[contents_json["ShortName"]] = contents_json["Name"]

        return data

    def available_languages(self) -> list[str]:
        return [path.name for path in self.locales_dir.iterdir() if path.is_dir()]

    async def menu_locale(self, language: str) -> dict[str, Any]:
        return await self._load_locale_file(language, "menu.json")

    async def client_locale(self, language: str) -> dict[str, Any]:
        return await self._load_locale_file(language, "locale.json")

    async def _load_locale_file(self, language: str, filename: str) -> dict[str, Any]:
        path = self.locales_dir.joinpath(language, filename)
        async with aiofiles.open(path, encoding="utf8") as file:
            contents = await file.read()
        return cast(dict[str, Any], orjson.loads(contents))
