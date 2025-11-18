import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

# --- This is the new part ---
# Add app directory to sys.path so we can import our modules
# This assumes 'alembic.ini' is in the 'backend/' folder, alongside the 'app/' folder
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models import Base  # Import your models' Base
from app.core.config import settings # Import your settings
# --- End new part ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- This is the new part ---
# Set the sqlalchemy.url from our settings object
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
# --- End new part ---

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# --- This line is modified ---
target_metadata = Base.metadata
# --- End modified part ---

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True # Detect column type changes
    )

    with context.begin_transaction():
        context.run_migrations()

# --- This whole section is replaced for async ---
def do_run_migrations(connection):
    """Helper function to run migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True # Detect column type changes
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Create an async engine from our settings
    connectable = create_async_engine(settings.DATABASE_URL)

    async with connectable.connect() as connection:
        # Run migrations synchronously within the async connection
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()
# --- End replaced section ---

if context.is_offline_mode():
    run_migrations_offline()
else:
    # --- This line is modified for async ---
    asyncio.run(run_migrations_online())
    # --- End modified part ---