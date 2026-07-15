"""Routes d'authentification."""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import User
from app.infrastructure.database.repositories.base import BaseRepository
from app.interfaces.api.v1.dependencies import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_superadmin, ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.interfaces.api.v1.schemas.auth import (
    LoginRequest, LoginResponse, UserCreate, UserResponse,
)

router = APIRouter()


@router.post("/auth/login")
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    """Authentifie un utilisateur et définit le cookie de session."""
    user_repo = BaseRepository(User, db)
    user = await user_repo.get_by_field("email", data.email)

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    if not user.actif:
        raise HTTPException(status_code=401, detail="Compte désactivé")

    # Créer le token JWT
    token = create_access_token(
        {"sub": str(user.id), "email": user.email, "role": user.role},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Définir le cookie HttpOnly
    response.set_cookie(
        key="bridge_session",
        value=token,
        httponly=True,
        secure=False,  # True en production (HTTPS)
        samesite="strict",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user={"id": user.id, "email": user.email, "nom": user.nom, "role": user.role},
    )


@router.post("/auth/logout")
async def logout(response: Response):
    """Déconnecte l'utilisateur en supprimant le cookie."""
    response.delete_cookie(
        key="bridge_session",
        path="/",
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return {"message": "Déconnecté avec succès"}


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Récupère le profil de l'utilisateur connecté."""
    return UserResponse.model_validate(current_user)


@router.post("/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _superadmin: User = Depends(get_superadmin),
):
    """Crée un nouvel utilisateur admin (superadmin uniquement)."""
    user_repo = BaseRepository(User, db)

    # Vérifier l'unicité de l'email
    existing = await user_repo.get_by_field("email", data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    user_data = data.model_dump()
    user_data["password_hash"] = hash_password(user_data.pop("password"))
    user = await user_repo.create(user_data)
    return UserResponse.model_validate(user)


@router.get("/admin/users", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_user),
):
    """Liste tous les utilisateurs (admin)."""
    user_repo = BaseRepository(User, db)
    users, _ = await user_repo.list_all(skip=0, limit=100)
    return [UserResponse.model_validate(u) for u in users]

@router.get("/auth/logout")
async def logout_get(response: Response):
    """Déconnexion via GET (lien direct)."""
    response.delete_cookie(key="bridge_session", path="/", httponly=True, samesite="strict")
    response.headers["Location"] = "/admin/login"
    response.status_code = 302
    return response