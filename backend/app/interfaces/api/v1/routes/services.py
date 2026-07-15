"""Routes API pour les Services."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Service
from app.infrastructure.database.repositories.base import BaseRepository
from app.interfaces.api.v1.schemas.service import (
    ServiceCreate, ServiceUpdate, ServiceResponse,
)

router = APIRouter()


async def get_repo(db: AsyncSession = Depends(get_db)) -> BaseRepository[Service]:
    return BaseRepository(Service, db)


@router.get("/services", response_model=list[ServiceResponse])
async def list_services(
    actif_only: bool = Query(True),
    repo: BaseRepository[Service] = Depends(get_repo),
):
    """Liste tous les services actifs, triés par ordre."""
    filters = {"actif": True} if actif_only else {}
    items, _ = await repo.list_all(
        skip=0, limit=50, filters=filters,
        order_by="ordre", order_desc=False,
    )
    return [ServiceResponse.model_validate(item) for item in items]


@router.get("/services/{id}", response_model=ServiceResponse)
async def get_service(id: int, repo: BaseRepository[Service] = Depends(get_repo)):
    item = await repo.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Service non trouvé")
    return ServiceResponse.model_validate(item)


@router.post("/admin/services", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(data: ServiceCreate, repo: BaseRepository[Service] = Depends(get_repo)):
    item = await repo.create(data.model_dump())
    return ServiceResponse.model_validate(item)


@router.put("/admin/services/{id}", response_model=ServiceResponse)
async def update_service(id: int, data: ServiceUpdate, repo: BaseRepository[Service] = Depends(get_repo)):
    item = await repo.update(id, data.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=404, detail="Service non trouvé")
    return ServiceResponse.model_validate(item)


@router.delete("/admin/services/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(id: int, repo: BaseRepository[Service] = Depends(get_repo)):
    if not await repo.delete(id):
        raise HTTPException(status_code=404, detail="Service non trouvé")