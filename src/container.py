from aioinject import Callable, Container, Singleton

from database.dependencies import get_session
from modules.accounts.services import AccountService
from modules.items.repository import create_template_repository
from modules.languages.services import LanguageService
from modules.launcher.services import EditionsService
from modules.profile.commands import ProfileCreateCommand
from modules.profile.services import ProfileManager, ProfileService


def create_container() -> Container:
    container = Container()
    container.register(Singleton(create_template_repository))
    container.register(Singleton(ProfileManager))

    container.register(Callable(get_session))

    container.register(Callable(LanguageService))
    container.register(Callable(EditionsService))
    container.register(Callable(ProfileService))
    container.register(Callable(ProfileCreateCommand))
    container.register(Callable(AccountService))
    return container
