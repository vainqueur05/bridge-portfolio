"""
Configuration de la base de données SQLAlchemy.
Supporte SQLite (dev) et PostgreSQL (prod) via une DATABASE_URL.
Utilise le pattern asynchrone pour FastAPI.
"""

import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

# Récupérer l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bridge_portfolio.db")

# Créer le moteur asynchrone
# SQLite nécessite check_same_thread=False
if "sqlite" in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,  # Mettre True pour debug SQL
        connect_args={"check_same_thread": False},
    )
else:
    # PostgreSQL
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,  # Vérifier la connexion avant de l'utiliser
    )

# Fabrique de sessions asynchrones
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Important pour éviter les erreurs après commit
)


# Base déclarative pour les modèles
class Base(DeclarativeBase):
    """Classe de base pour tous les modèles SQLAlchemy."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dépendance FastAPI pour obtenir une session de base de données.
    Gère automatiquement la fermeture de la session.
    
    Usage:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()