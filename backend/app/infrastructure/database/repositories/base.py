"""
Repository de base avec opérations CRUD génériques.
Pattern Repository pour découpler la logique métier de l'ORM.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

# Type variable pour le modèle SQLAlchemy
ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Repository générique avec les opérations CRUD de base.
    
    Usage:
        class ProjetRepository(BaseRepository[Projet]):
            def __init__(self, session: AsyncSession):
                super().__init__(Projet, session)
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: dict) -> ModelType:
        """Crée une nouvelle entité."""
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Récupère une entité par son ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Récupère une entité par un champ spécifique."""
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, field) == value)
        )
        return result.scalar_one_or_none()

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = True,
    ) -> tuple[List[ModelType], int]:
        """
        Liste paginée avec filtres optionnels.
        
        Returns:
            tuple: (liste des entités, nombre total)
        """
        query = select(self.model)

        # Appliquer les filtres
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)

        # Compter le total avant pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Appliquer le tri
        if order_by and hasattr(self.model, order_by):
            order_col = getattr(self.model, order_by)
            query = query.order_by(order_col.desc() if order_desc else order_col.asc())

        # Pagination
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        items = result.scalars().all()

        return list(items), total

    async def update(self, id: int, data: dict) -> Optional[ModelType]:
        """Met à jour une entité et retourne l'instance mise à jour."""
        # Filtrer les champs None pour ne pas écraser avec des valeurs nulles
        update_data = {k: v for k, v in data.items() if v is not None}

        if update_data:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**update_data)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.scalar_one_or_none()

        # Si rien à mettre à jour, retourner l'existant
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        """Supprime une entité (hard delete)."""
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.flush()
            return True
        return False

    async def soft_delete(self, id: int, status_field: str = "statut", status_value: str = "archivé") -> bool:
        """Suppression logique en changeant le statut."""
        return await self.update(id, {status_field: status_value}) is not None

    async def exists(self, id: int) -> bool:
        """Vérifie si une entité existe."""
        result = await self.session.execute(
            select(func.count()).select_from(self.model).where(self.model.id == id)
        )
        return result.scalar() > 0