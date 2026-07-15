"""Routes API pour les Articles."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.repositories.base import BaseRepository
from app.infrastructure.database.models import Article
from app.interfaces.api.v1.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleListResponse,
)

router = APIRouter()


async def get_article_repository(db: AsyncSession = Depends(get_db)) -> BaseRepository[Article]:
    return BaseRepository(Article, db)


@router.get("/articles", response_model=ArticleListResponse)
async def list_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    statut: Optional[str] = Query(None),
    categorie: Optional[str] = Query(None),
    repo: BaseRepository[Article] = Depends(get_article_repository),
):
    """Liste paginée des articles."""
    filters = {}
    if statut:
        filters["statut"] = statut
    if categorie:
        filters["categorie"] = categorie

    items, total = await repo.list_all(
        skip=skip, limit=limit, filters=filters if filters else None,
        order_by="date_publication", order_desc=True,
    )

    return ArticleListResponse(
        total=total,
        page=skip // limit + 1,
        size=limit,
        items=[ArticleResponse.model_validate(item) for item in items],
    )


@router.get("/articles/{id}", response_model=ArticleResponse)
async def get_article(id: int, repo: BaseRepository[Article] = Depends(get_article_repository)):
    article = await repo.get_by_id(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return ArticleResponse.model_validate(article)


@router.post("/admin/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    data: ArticleCreate,
    repo: BaseRepository[Article] = Depends(get_article_repository),
):
    article = await repo.create(data.model_dump(exclude_unset=True))
    return ArticleResponse.model_validate(article)


@router.put("/admin/articles/{id}", response_model=ArticleResponse)
async def update_article(
    id: int,
    data: ArticleUpdate,
    repo: BaseRepository[Article] = Depends(get_article_repository),
):
    article = await repo.update(id, data.model_dump(exclude_unset=True))
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return ArticleResponse.model_validate(article)


@router.delete("/admin/articles/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, repo: BaseRepository[Article] = Depends(get_article_repository)):
    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Article non trouvé")