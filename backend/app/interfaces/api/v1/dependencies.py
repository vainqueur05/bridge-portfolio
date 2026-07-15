"""
Dépendances pour l'authentification et l'autorisation.
JWT stocké en cookie HttpOnly.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import User
from app.infrastructure.database.repositories.base import BaseRepository

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crée un token JWT avec expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Décode et vérifie un token JWT. Lève JWTError si invalide."""
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Récupère l'utilisateur courant à partir du cookie de session
    ou du header Authorization (pour les API).
    """
    token = None

    # 1. Essayer le cookie HttpOnly
    token = request.cookies.get("bridge_session")

    # 2. Fallback sur le header Bearer (pour tests API)
    if not token and credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    # Récupérer l'utilisateur depuis la DB
    user_repo = BaseRepository(User, db)
    user = await user_repo.get_by_id(int(user_id))

    if not user or not user.actif:
        raise HTTPException(status_code=401, detail="Utilisateur inactif ou supprimé")

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Vérifie que l'utilisateur a un rôle admin (superadmin, gestionnaire, redacteur)."""
    admin_roles = {"superadmin", "gestionnaire", "redacteur"}
    if current_user.role not in admin_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissions insuffisantes"
        )
    return current_user


async def get_superadmin(current_user: User = Depends(get_current_user)) -> User:
    """Vérifie que l'utilisateur est superadmin."""
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Réservé au superadmin")
    return current_user