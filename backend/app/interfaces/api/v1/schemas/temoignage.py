"""Schémas Pydantic pour les Témoignages."""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class TemoignageBase(BaseModel):
    nom_client: str = Field(..., min_length=2, max_length=150)
    entreprise: Optional[str] = Field(None, max_length=200)
    contenu: str = Field(..., min_length=10, max_length=2000)
    note: Optional[int] = Field(None, ge=1, le=5)
    photo_client: Optional[str] = None
    date_temoignage: Optional[date] = None
    projet_id: Optional[int] = None
    approuve: bool = False
    featured: bool = False
    video_url: Optional[str] = Field(None, max_length=500)


class TemoignageCreate(TemoignageBase):
    pass


class TemoignageUpdate(BaseModel):
    nom_client: Optional[str] = Field(None, min_length=2, max_length=150)
    entreprise: Optional[str] = None
    contenu: Optional[str] = Field(None, min_length=10, max_length=2000)
    note: Optional[int] = Field(None, ge=1, le=5)
    photo_client: Optional[str] = None
    date_temoignage: Optional[date] = None
    projet_id: Optional[int] = None
    approuve: Optional[bool] = None
    featured: Optional[bool] = None
    video_url: Optional[str] = None


class TemoignageResponse(TemoignageBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class TemoignageListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[TemoignageResponse]