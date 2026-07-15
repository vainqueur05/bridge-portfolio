"""Routes API pour les Liens Sociaux."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import LienSocial
from app.infrastructure.database.repositories.base import BaseRepository

router = APIRouter()


@router.get("/liens-sociaux")
async def list_liens(
    actif: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """Liste les liens sociaux actifs, triés par ordre."""
    repo = BaseRepository(LienSocial, db)
    filters = {"actif": True} if actif else {}
    items, _ = await repo.list_all(skip=0, limit=50, filters=filters, order_by="ordre", order_desc=False)
    return [{"id": item.id, "plateforme": item.plateforme, "url": item.url, "icone": item.icone, "ordre": item.ordre} for item in items]


@router.post("/admin/liens-sociaux", status_code=201)
async def create_lien(data: dict, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(LienSocial, db)
    lien = await repo.create(data)
    return {"id": lien.id, "plateforme": lien.plateforme, "url": lien.url, "icone": lien.icone, "ordre": lien.ordre}


@router.put("/admin/liens-sociaux/{id}")
async def update_lien(id: int, data: dict, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(LienSocial, db)
    lien = await repo.update(id, data)
    if not lien:
        raise HTTPException(404, "Lien non trouvé")
    return {"success": True}


@router.delete("/admin/liens-sociaux/{id}")
async def delete_lien(id: int, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(LienSocial, db)
    if not await repo.delete(id):
        raise HTTPException(404, "Lien non trouvé")
    return {"success": True}  