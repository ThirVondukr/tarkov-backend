import paths


class EditionsService:
    def __init__(self) -> None:
        self.starting_profiles_path = paths.database.joinpath("starting_profiles")

    @property
    def available_editions(self) -> list[str]:
        starting_profiles_dir = self.starting_profiles_path.glob("*")
        return sorted(d.name for d in starting_profiles_dir if d.is_dir())
