"""
Repository spécialisé pour les Projets.
Étend le BaseRepository avec des méthodes spécifiques.
"""

from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.infrastructure.database.models import Projet
from app.infrastructure.database.repositories.base import BaseRepository


class ProjetRepository(BaseRepository[Projet]):
    """Repository pour l'entité Projet."""

    def __init__(self, session: AsyncSession):
        super().__init__(Projet, session)

    async def get_by_slug(self, slug: str) -> Optional[Projet]:
        """Récupère un projet par son slug."""
        result = await self.session.execute(
            select(Projet)
            .where(Projet.slug == slug)
            .options(selectinload(Projet.temoignages))  # ← CORRIGÉ : temoignages au pluriel
        )
        return result.scalar_one_or_none()

    async def get_featured(self, limit: int = 6) -> List[Projet]:
        """Récupère les projets mis en avant."""
        result = await self.session.execute(
            select(Projet)
            .where(Projet.featured == True, Projet.statut == "publié")
            .order_by(Projet.date_publication.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_published(
        self, skip: int = 0, limit: int = 12, categorie: Optional[str] = None
    ) -> tuple[List[Projet], int]:
        """Récupère les projets publiés avec filtrage optionnel."""
        filters = {"statut": "publié"}
        if categorie:
            filters["categorie"] = categorie

        return await self.list_all(
            skip=skip,
            limit=limit,
            filters=filters,
            order_by="date_publication",
            order_desc=True,
        )

    async def duplicate(self, id: int) -> Optional[Projet]:
        """Duplique un projet existant."""
        original = await self.get_by_id(id)
        if not original:
            return None

        data = {
            "titre": f"{original.titre} (copie)",
            "description_courte": original.description_courte,
            "probleme_resolu": original.probleme_resolu,
            "solution_apportee": original.solution_apportee,
            "resultats_chiffres": original.resultats_chiffres,
            "technologies": original.technologies,
            "categorie": original.categorie,
            "donnees_simulateur_roi": original.donnees_simulateur_roi,
            "statut": "brouillon",
            "featured": False,
        }
        return await self.create(data)