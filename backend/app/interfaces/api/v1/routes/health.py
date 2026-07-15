"""
Endpoint de health check pour monitoring et uptime.
Utilisé par Render pour vérifier que l'application est en vie.
"""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check complet.
    Vérifie :
    - L'état de l'API
    - La connexion à la base de données
    - La version de l'application
    
    Returns:
        dict: Statut de santé de l'application
    """
    db_status = "ok"
    db_message = "Connectée"

    # Vérifier la connexion à la base de données
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
    except Exception as e:
        db_status = "error"
        db_message = f"Erreur: {str(e)[:100]}"

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "version": "4.0.0",
        "environment": "production" if __import__("os").getenv("RENDER") else "development",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "api": {
                "status": "ok",
                "message": "API opérationnelle"
            },
            "database": {
                "status": db_status,
                "message": db_message
            }
        }
    }


@router.get("/health/ping")
async def ping():
    """
    Health check minimal pour les tests de latence.
    Aucune vérification de base de données.
    """
    return {
        "ping": "pong",
        "timestamp": datetime.utcnow().isoformat()
    }