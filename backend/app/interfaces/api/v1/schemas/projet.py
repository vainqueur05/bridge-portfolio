"""
Schémas Pydantic pour la validation des données Projet.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, field_validator
import re


class ProjetBase(BaseModel):
    """Champs communs à tous les schémas Projet."""
    titre: str = Field(..., min_length=3, max_length=200, description="Titre du projet")
    slug: Optional[str] = Field(None, max_length=200, description="Slug URL (auto-généré si vide)")
    description_courte: Optional[str] = Field(None, max_length=500)
    probleme_resolu: Optional[str] = None
    solution_apportee: Optional[str] = None
    resultats_chiffres: Optional[str] = None
    image_principale: Optional[str] = Field(None, max_length=500)
    galerie_images: Optional[List[str]] = Field(None, max_length=10)
    technologies: Optional[List[str]] = None
    lien_github: Optional[str] = Field(None, max_length=300)
    lien_site: Optional[str] = Field(None, max_length=300)
    categorie: Optional[str] = Field(None, max_length=50, pattern="^(SaaS|Réservation|WhatsApp|API)$")
    client_nom: Optional[str] = Field(None, max_length=200)
    statut: str = Field(default="brouillon", pattern="^(brouillon|publié|archivé)$")
    featured: bool = False
    date_publication: Optional[date] = None
    temps_realisation: Optional[str] = Field(None, max_length=50)
    donnees_simulateur_roi: Optional[dict] = None

    @field_validator('slug', mode='before')
    @classmethod
    def generate_slug(cls, v, info):
        """Auto-génère le slug à partir du titre si non fourni."""
        if not v and 'titre' in info.data:
            titre = info.data['titre']
            v = re.sub(r'[^\w\s-]', '', titre.lower())
            v = re.sub(r'[-\s]+', '-', v).strip('-')
        return v


class ProjetCreate(ProjetBase):
    """Schéma pour la création d'un projet."""
    titre: str = Field(..., min_length=3, max_length=200)


class ProjetUpdate(BaseModel):
    """Schéma pour la mise à jour partielle d'un projet."""
    titre: Optional[str] = Field(None, min_length=3, max_length=200)
    slug: Optional[str] = Field(None, max_length=200)
    description_courte: Optional[str] = None
    probleme_resolu: Optional[str] = None
    solution_apportee: Optional[str] = None
    resultats_chiffres: Optional[str] = None
    image_principale: Optional[str] = None
    galerie_images: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    lien_github: Optional[str] = None
    lien_site: Optional[str] = None
    categorie: Optional[str] = None
    client_nom: Optional[str] = None
    statut: Optional[str] = Field(None, pattern="^(brouillon|publié|archivé)$")
    featured: Optional[bool] = None
    date_publication: Optional[date] = None
    temps_realisation: Optional[str] = None
    donnees_simulateur_roi: Optional[dict] = None


class ProjetResponse(ProjetBase):
    """Schéma pour la réponse API (lecture)."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProjetListResponse(BaseModel):
    """Schéma pour la liste paginée de projets."""
    total: int
    page: int
    size: int
    items: List[ProjetResponse]