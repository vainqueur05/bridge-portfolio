"""Routes API pour les Témoignages."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Temoignage
from app.infrastructure.database.repositories.base import BaseRepository
from app.interfaces.api.v1.schemas.temoignage import (
    TemoignageCreate, TemoignageUpdate, TemoignageResponse, TemoignageListResponse,
)

router = APIRouter()


async def get_repo(db: AsyncSession = Depends(get_db)) -> BaseRepository[Temoignage]:
    return BaseRepository(Temoignage, db)


@router.get("/temoignages", response_model=TemoignageListResponse)
async def list_temoignages(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    approuve: Optional[bool] = Query(None),
    featured: Optional[bool] = Query(None),
    repo: BaseRepository[Temoignage] = Depends(get_repo),
):
    """Liste paginée des témoignages."""
    filters = {}
    if approuve is not None:
        filters["approuve"] = approuve
    if featured is not None:
        filters["featured"] = featured

    items, total = await repo.list_all(
        skip=skip, limit=limit,
        filters=filters if filters else None,
        order_by="created_at", order_desc=True,
    )
    return TemoignageListResponse(
        total=total, page=skip // limit + 1, size=limit,
        items=[TemoignageResponse.model_validate(item) for item in items],
    )


@router.get("/temoignages/{id}", response_model=TemoignageResponse)
async def get_temoignage(id: int, repo: BaseRepository[Temoignage] = Depends(get_repo)):
    item = await repo.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Témoignage non trouvé")
    return TemoignageResponse.model_validate(item)


@router.post("/admin/temoignages", response_model=TemoignageResponse, status_code=status.HTTP_201_CREATED)
async def create_temoignage(data: TemoignageCreate, repo: BaseRepository[Temoignage] = Depends(get_repo)):
    item = await repo.create(data.model_dump())
    return TemoignageResponse.model_validate(item)


@router.put("/admin/temoignages/{id}", response_model=TemoignageResponse)
async def update_temoignage(id: int, data: TemoignageUpdate, repo: BaseRepository[Temoignage] = Depends(get_repo)):
    item = await repo.update(id, data.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=404, detail="Témoignage non trouvé")
    return TemoignageResponse.model_validate(item)


@router.delete("/admin/temoignages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_temoignage(id: int, repo: BaseRepository[Temoignage] = Depends(get_repo)):
    if not await repo.delete(id):
        raise HTTPException(status_code=404, detail="Témoignage non trouvé")


@router.patch("/admin/temoignages/{id}/approuve", response_model=TemoignageResponse)
async def toggle_approuve(id: int, repo: BaseRepository[Temoignage] = Depends(get_repo)):
    item = await repo.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Témoignage non trouvé")
    updated = await repo.update(id, {"approuve": not item.approuve})
    return TemoignageResponse.model_validate(updated)