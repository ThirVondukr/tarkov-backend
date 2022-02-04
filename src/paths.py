import sys
from pathlib import Path

if getattr(sys, "frozen", False):  # pragma: no cover
    application_path = Path(sys.executable).parent
else:
    application_path = Path(__file__).parent.parent

resources = application_path.joinpath("resources")
config = resources.joinpath("config")
certificates = resources.joinpath("certs")

database = application_path.joinpath("resources/database")
customization = database.joinpath("customization")
locales = database.joinpath("locales")
items = database.joinpath("items")


sqlite_db_path = resources.joinpath("db.sqlite3")
