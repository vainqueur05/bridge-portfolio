"""Schémas Pydantic pour les Messages (CRM)."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class MessageCreate(BaseModel):
    """Création d'un message depuis le formulaire public."""
    nom: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    telephone: Optional[str] = Field(None, max_length=30)
    contenu: str = Field(..., min_length=10, max_length=2000)
    source: str = Field(default="formulaire", pattern="^(formulaire|whatsapp|bridgescan|agent_ia)$")
    projet_interesse: Optional[str] = Field(None, max_length=200)


class MessageUpdate(BaseModel):
    """Mise à jour admin d'un message."""
    statut_lead: Optional[str] = Field(None, pattern="^(nouveau|contacte|negociation|gagne|perdu)$")
    lu: Optional[bool] = None
    repondu: Optional[bool] = None
    note_interne: Optional[str] = None
    date_dernier_contact: Optional[datetime] = None


class MessageResponse(BaseModel):
    id: int
    nom: Optional[str]
    email: Optional[str]
    telephone: Optional[str]
    contenu: Optional[str]
    source: Optional[str]
    projet_interesse: Optional[str]
    statut_lead: str
    lu: bool
    repondu: bool
    note_interne: Optional[str]
    date_dernier_contact: Optional[datetime]
    created_at: datetime
    model_config = {"from_attributes": True}


class MessageListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[MessageResponse]