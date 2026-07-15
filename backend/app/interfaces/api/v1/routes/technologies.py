"""Routes API pour les Technologies."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Technologie
from app.infrastructure.database.repositories.base import BaseRepository

router = APIRouter()


@router.get("/technologies")
async def list_technologies(db: AsyncSession = Depends(get_db)):
    """Liste toutes les technologies."""
    repo = BaseRepository(Technologie, db)
    items, _ = await repo.list_all(skip=0, limit=100, order_by="nom", order_desc=False)
    return [{"id": t.id, "nom": t.nom, "categorie": t.categorie, "niveau": t.niveau, "doc_url": t.doc_url, "icone_svg": t.icone_svg} for t in items]