"""Routes admin pour la configuration."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Config, User
from app.interfaces.api.v1.dependencies import get_current_admin

router = APIRouter()


class ConfigItem(BaseModel):
    cle: str
    valeur: str | None = None


class ConfigBatch(BaseModel):
    configs: List[ConfigItem]


@router.put("/admin/config/batch")
async def update_config_batch(
    data: ConfigBatch,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Met à jour plusieurs clés de configuration à la fois."""
    for item in data.configs:
        result = await db.execute(select(Config).where(Config.cle == item.cle))
        config = result.scalar_one_or_none()
        
        if config:
            config.valeur = item.valeur
        else:
            db.add(Config(cle=item.cle, valeur=item.valeur))
    
    await db.commit()
    return {"success": True, "updated": len(data.configs)}


@router.get("/admin/config")
async def get_all_config(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Récupère toutes les configurations (admin)."""
    result = await db.execute(select(Config))
    configs = result.scalars().all()
    return [{"cle": c.cle, "valeur": c.valeur, "description": c.description} for c in configs]