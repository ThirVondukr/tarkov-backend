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
        language_dirs = [d for d in self.locales_dir.iterdir() if d.is_dir()]

        for lang_dir in language_dirs:
            async with aiofiles.open(
                lang_dir.joinpath(f"{lang_dir.name}.json"),
                encoding="utf8",
            ) as file:
                contents = await file.read()
            contents_json = orjson.loads(contents)
            data[contents_json["ShortName"]] = contents_json["Name"]

        return data

    def available_languages(self) -> list[str]:
        return [path.name for path in self.locales_dir.iterdir() if path.is_dir()]

    async def game_locale(self, lang: str) -> dict[str, Any]:
        path = self.locales_dir.joinpath(lang, "menu.json")
        async with aiofiles.open(path, encoding="utf8") as file:
            contents = await file.read()
        return cast(dict[str, Any], orjson.loads(contents))
