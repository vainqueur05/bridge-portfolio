"""Schémas Pydantic pour les Services."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    titre: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = None
    icone: Optional[str] = Field(None, max_length=50)
    tarif_indicatif: Optional[str] = Field(None, max_length=100)
    duree_estimee: Optional[str] = Field(None, max_length=100)
    processus: Optional[str] = None
    livrables: Optional[str] = None
    badge: Optional[str] = Field(None, pattern="^(Populaire|Nouveau|Best-seller)$")
    ordre: int = 0
    actif: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    titre: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = None
    icone: Optional[str] = None
    tarif_indicatif: Optional[str] = None
    duree_estimee: Optional[str] = None
    processus: Optional[str] = None
    livrables: Optional[str] = None
    badge: Optional[str] = None
    ordre: Optional[int] = None
    actif: Optional[bool] = None


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}