import functools

from aioinject import Callable, Container, Singleton

from database.dependencies import get_session
from modules.accounts.services import AccountService
from modules.items.handlers import ActionHandler
from modules.items.repository import create_template_repository
from modules.languages.services import LanguageService
from modules.launcher.services import EditionsService
from modules.profile.commands import ProfileCreateCommand
from modules.profile.services import ProfileManager, ProfileService
from modules.trading.manager import create_trader_manager


@functools.lru_cache(maxsize=1)
def create_container() -> Container:
    container = Container()
    container.register(Singleton(create_template_repository))
    container.register(Singleton(ProfileManager))
    container.register(Singleton(create_trader_manager))

    container.register(Callable(get_session))
    container.register(Callable(ActionHandler))
    container.register(Callable(LanguageService))
    container.register(Callable(EditionsService))
    container.register(Callable(ProfileService))
    container.register(Callable(ProfileCreateCommand))
    container.register(Callable(AccountService))
    return container
