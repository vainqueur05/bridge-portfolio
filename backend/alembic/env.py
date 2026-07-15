"""
Alembic environment configuration.
Configuration asynchrone pour SQLAlchemy 2.0+.
"""

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Charger les variables d'environnement
load_dotenv()

# Importer les modèles pour que Base.metadata soit complet
from app.infrastructure.database.models import Base
from app.infrastructure.database.session import DATABASE_URL

# Alembic Config object
config = context.config

# Setter l'URL de la base de données dans la config Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpréter le fichier de config pour le logging Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata pour autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Exécute les migrations en mode 'offline'.
    Utile pour générer des scripts SQL sans connexion à la base.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Exécute les migrations sur une connexion synchrone.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Exécute les migrations en mode asynchrone.
    """
    configuration = config.get_section(config.config_ini_section, {})
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # --- CORRECTION : Créer les tables manquantes AVANT la migration ---
        # Cela garantit que si une table existe déjà, elle ne sera pas recréée.
        # checkfirst=True évite l'erreur "table already exists".
        await connection.run_sync(Base.metadata.create_all)
        # ----------------------------------------------------------------
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())