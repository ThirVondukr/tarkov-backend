from typing import Iterable, cast

from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import MigrationContext, RevisionStep
from alembic.script import ScriptDirectory
from sqlalchemy.future import Connection

import settings
from database.base import Base, engine


def _run_migrations(connection: Connection) -> None:  # pragma: no cover
    alembic_cfg = Config(file_="alembic.ini")
    alembic_script = ScriptDirectory.from_config(alembic_cfg)

    def do_upgrade(revision: str, context: MigrationContext) -> Iterable[RevisionStep]:
        heads: str = cast(str, alembic_script.get_heads())
        return alembic_script._upgrade_revs(heads, revision)

    context = EnvironmentContext(alembic_cfg, alembic_script)
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        compare_type=True,
        fn=do_upgrade,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def migrate(
    run_migrations: bool = settings.database.run_migrations,
) -> None:  # pragma: no cover
    if not run_migrations:
        return

    async with engine.connect() as connection:
        await connection.run_sync(_run_migrations)
