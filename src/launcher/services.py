from pathlib import Path

import paths


class EditionsService:
    def __init__(
        self,
        starting_profiles_path: Path = paths.database.joinpath("starting_profiles"),
    ):
        self.starting_profiles_path = starting_profiles_path

    @property
    def available_editions(self) -> list[str]:
        starting_profiles_dir = self.starting_profiles_path.glob("*")
        return sorted(d.name for d in starting_profiles_dir)
