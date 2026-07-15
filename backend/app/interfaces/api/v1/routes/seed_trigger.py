"""Route temporaire pour lancer le seed manuellement."""

from fastapi import APIRouter
from app.infrastructure.database.seed import seed_database

router = APIRouter()


@router.get("/seed-now")
async def trigger_seed():
    """Lance le seed. À supprimer après usage."""
    try:
        await seed_database()
        return {"status": "ok", "message": "Seed lancé avec succès"}
    except Exception as e:
        return {"status": "error", "message": str(e)}