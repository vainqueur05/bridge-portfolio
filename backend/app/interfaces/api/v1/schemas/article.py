"""Schémas Pydantic pour les Articles."""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    titre: str = Field(..., min_length=3, max_length=200)
    slug: Optional[str] = Field(None, max_length=200)
    extrait: Optional[str] = Field(None, max_length=500)
    contenu: Optional[str] = None
    image_couverture: Optional[str] = None
    categorie: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    statut: str = Field(default="brouillon", pattern="^(brouillon|publié|archivé)$")
    featured: bool = False
    date_publication: Optional[date] = None
    temps_lecture: Optional[int] = Field(None, ge=1, le=60)
    projet_id: Optional[int] = None


class ArticleCreate(ArticleBase):
    titre: str = Field(..., min_length=3, max_length=200)


class ArticleUpdate(BaseModel):
    titre: Optional[str] = Field(None, min_length=3, max_length=200)
    slug: Optional[str] = None
    extrait: Optional[str] = None
    contenu: Optional[str] = None
    image_couverture: Optional[str] = None
    categorie: Optional[str] = None
    tags: Optional[List[str]] = None
    statut: Optional[str] = Field(None, pattern="^(brouillon|publié|archivé)$")
    featured: Optional[bool] = None
    date_publication: Optional[date] = None
    temps_lecture: Optional[int] = None
    projet_id: Optional[int] = None


class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ArticleListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[ArticleResponse]