import sys
from pathlib import Path

if getattr(sys, "frozen", False):  # pragma: no cover
    application_path = Path(sys.executable).parent
else:
    application_path = Path(__file__).parent.parent

resources = application_path.joinpath("resources")

database = application_path.joinpath("resources/database")
locales = database.joinpath("locales")

certificates = application_path.joinpath("resources/certs")

sqlite_db_path = resources.joinpath("db.sqlite3")
