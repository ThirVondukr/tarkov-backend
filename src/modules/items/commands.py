from modules.items.actions import Action, ReadEncyclopedia
from modules.profile.types import Profile


class ReadEncyclopediaCommand:
    def __init__(self, encyclopedia: dict[str, bool]) -> None:
        self.encyclopedia = encyclopedia

    async def execute(self, action: ReadEncyclopedia) -> None:
        for template_id in action.ids:
            self.encyclopedia[template_id] = True


class CommandExecutor:
    def __init__(
        self,
        profile: Profile,
    ):
        self.profile = profile

    async def execute(self, actions: list[Action]) -> None:
        for action in actions:
            if isinstance(action, ReadEncyclopedia):
                command = ReadEncyclopediaCommand(self.profile.encyclopedia)
                await command.execute(action)
            else:
                raise Exception("Action not handled", action)
