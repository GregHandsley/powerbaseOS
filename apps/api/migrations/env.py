from __future__ import annotations
import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.models import __init__ as models_init  
from app.models import Base
from app.models.facility import Facility  # noqa
from app.models.side import Side  # noqa
from app.models.rack import Rack  # noqa
from app.models.timeslot import Timeslot  # noqa
from app.models.user import User, Role, user_roles_table  # noqa
from app.models.event import Event  # noqa: F401
from app.models.job import Job  # noqa: F401

target_metadata = Base.metadata

config = context.config

# Make fileConfig tolerant of minimal INI files
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except KeyError:
        # missing [formatters]/[handlers]/[loggers]
        pass

from app.core.settings import get_settings
settings = get_settings()

# target_metadata is set above with Base.metadata

def _configure_url():
    config.set_main_option("sqlalchemy.url", settings.database_url_async)

def run_migrations_offline():
    _configure_url()
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    _configure_url()
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())

run_migrations()