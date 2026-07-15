"""Routes API pour les Messages (CRM)."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Message
from app.infrastructure.database.repositories.base import BaseRepository
from app.interfaces.api.v1.schemas.message import (
    MessageCreate, MessageUpdate, MessageResponse, MessageListResponse,
)

router = APIRouter()


async def get_repo(db: AsyncSession = Depends(get_db)) -> BaseRepository[Message]:
    return BaseRepository(Message, db)


@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(data: MessageCreate, repo: BaseRepository[Message] = Depends(get_repo)):
    """Soumission publique d'un message depuis le formulaire de contact."""
    return MessageResponse.model_validate(await repo.create(data.model_dump()))


@router.get("/admin/messages", response_model=MessageListResponse)
async def list_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    statut_lead: Optional[str] = Query(None),
    lu: Optional[bool] = Query(None),
    repo: BaseRepository[Message] = Depends(get_repo),
):
    """Liste paginée des messages (admin)."""
    filters = {}
    if statut_lead:
        filters["statut_lead"] = statut_lead
    if lu is not None:
        filters["lu"] = lu

    items, total = await repo.list_all(
        skip=skip, limit=limit,
        filters=filters if filters else None,
        order_by="created_at", order_desc=True,
    )
    return MessageListResponse(
        total=total, page=skip // limit + 1, size=limit,
        items=[MessageResponse.model_validate(item) for item in items],
    )


@router.get("/admin/messages/{id}", response_model=MessageResponse)
async def get_message(id: int, repo: BaseRepository[Message] = Depends(get_repo)):
    item = await repo.get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    return MessageResponse.model_validate(item)


@router.patch("/admin/messages/{id}", response_model=MessageResponse)
async def update_message(id: int, data: MessageUpdate, repo: BaseRepository[Message] = Depends(get_repo)):
    """Met à jour le statut d'un message (admin)."""
    item = await repo.update(id, data.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    return MessageResponse.model_validate(item)


@router.delete("/admin/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: int, repo: BaseRepository[Message] = Depends(get_repo)):
    if not await repo.delete(id):
        raise HTTPException(status_code=404, detail="Message non trouvé")