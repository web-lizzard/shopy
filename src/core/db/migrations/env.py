import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from core.configuration import configuration
from core.db import Base


# Alembic Config object, which provides access to the values from the .ini file
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add model's MetaData object here for 'autogenerate' support

target_metadata = Base.metadata

# Other options from the config can be accessed as:
# my_important_option = config.get_main_option("my_important_option")


def run_migrations_offline() -> None:
    # This configures the context with just a URL and not an Engine,
    # though an Engine is acceptable here as well.
    # By skipping the Engine creation we don't even need a DBAPI to be available.

    # Calls to context.execute() here emit the given string to the script output.
    url = configuration.database.url
    context.configure(
        url=str(url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def _run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def _run_async_migrations() -> None:
    # In this scenario we need to create an Engine and associate a connection with the context.
    settings = config.get_section(config.config_ini_section, {})
    settings["sqlalchemy.url"] = str(configuration.database.url)
    connectable = async_engine_from_config(
        settings,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(_run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
