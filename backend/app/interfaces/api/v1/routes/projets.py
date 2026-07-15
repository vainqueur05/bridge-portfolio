"""
Routes API pour la gestion des Projets.
CRUD complet + actions spéciales.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.repositories.projet_repository import ProjetRepository
from app.interfaces.api.v1.schemas.projet import (
    ProjetCreate,
    ProjetUpdate,
    ProjetResponse,
    ProjetListResponse,
)

router = APIRouter()


# Dépendance pour injecter le repository
async def get_projet_repository(db: AsyncSession = Depends(get_db)) -> ProjetRepository:
    return ProjetRepository(db)


@router.get("/projets", response_model=ProjetListResponse)
async def list_projets(
    skip: int = Query(0, ge=0, description="Offset de pagination"),
    limit: int = Query(20, ge=1, le=100, description="Nombre d'éléments par page"),
    statut: Optional[str] = Query(None, description="Filtrer par statut"),
    categorie: Optional[str] = Query(None, description="Filtrer par catégorie"),
    featured: Optional[bool] = Query(None, description="Projets mis en avant"),
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """
    Liste paginée des projets avec filtres optionnels.
    Accessible publiquement (projets publiés) et en admin (tous).
    """
    filters = {}
    if statut:
        filters["statut"] = statut
    if categorie:
        filters["categorie"] = categorie
    if featured is not None:
        filters["featured"] = featured

    items, total = await repo.list_all(
        skip=skip,
        limit=limit,
        filters=filters if filters else None,
        order_by="created_at",
        order_desc=True,
    )

    return ProjetListResponse(
        total=total,
        page=skip // limit + 1,
        size=limit,
        items=[ProjetResponse.model_validate(item) for item in items],
    )


@router.get("/projets/{id}", response_model=ProjetResponse)
async def get_projet(
    id: int,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Récupère un projet par son ID."""
    projet = await repo.get_by_id(id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return ProjetResponse.model_validate(projet)


@router.get("/projets/slug/{slug}", response_model=ProjetResponse)
async def get_projet_by_slug(
    slug: str,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Récupère un projet par son slug (URL-friendly)."""
    projet = await repo.get_by_slug(slug)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return ProjetResponse.model_validate(projet)


@router.post("/admin/projets", response_model=ProjetResponse, status_code=status.HTTP_201_CREATED)
async def create_projet(
    data: ProjetCreate,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Crée un nouveau projet (admin)."""
    # Vérifier l'unicité du slug
    if data.slug:
        existing = await repo.get_by_field("slug", data.slug)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Un projet avec le slug '{data.slug}' existe déjà",
            )

    projet = await repo.create(data.model_dump(exclude_unset=True))
    return ProjetResponse.model_validate(projet)


@router.put("/admin/projets/{id}", response_model=ProjetResponse)
async def update_projet(
    id: int,
    data: ProjetUpdate,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Met à jour un projet existant (admin)."""
    projet = await repo.update(id, data.model_dump(exclude_unset=True))
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return ProjetResponse.model_validate(projet)


@router.delete("/admin/projets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_projet(
    id: int,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Supprime définitivement un projet (admin)."""
    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Projet non trouvé")


@router.patch("/admin/projets/{id}/archiver", response_model=ProjetResponse)
async def archiver_projet(
    id: int,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Archive un projet (soft delete)."""
    projet = await repo.soft_delete(id, "statut", "archivé")
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return ProjetResponse.model_validate(projet)


@router.patch("/admin/projets/{id}/featured", response_model=ProjetResponse)
async def toggle_featured(
    id: int,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Bascule le statut 'featured' d'un projet."""
    projet = await repo.get_by_id(id)
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    updated = await repo.update(id, {"featured": not projet.featured})
    return ProjetResponse.model_validate(updated)


@router.post("/admin/projets/{id}/dupliquer", response_model=ProjetResponse, status_code=status.HTTP_201_CREATED)
async def dupliquer_projet(
    id: int,
    repo: ProjetRepository = Depends(get_projet_repository),
):
    """Duplique un projet existant."""
    nouveau = await repo.duplicate(id)
    if not nouveau:
        raise HTTPException(status_code=404, detail="Projet source non trouvé")
    return ProjetResponse.model_validate(nouveau)