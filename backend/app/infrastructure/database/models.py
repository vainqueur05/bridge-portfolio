"""
Tous les modèles SQLAlchemy de l'application Bridge Afrika Portfolio.
Architecture Domain-Driven Design avec relations optimisées.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .session import Base


# ============================================
# CONFIGURATION
# ============================================

class Config(Base):
    """
    Table de configuration clé-valeur.
    Permet de stocker tous les paramètres sans modifier le code.
    """
    __tablename__ = "config"

    cle = Column(String(100), primary_key=True, index=True)
    valeur = Column(Text, nullable=True)
    description = Column(
        String(255), nullable=True, comment="Description humaine de la clé"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )

    def __repr__(self):
        return f"<Config(cle='{self.cle}')>"


# ============================================
# UTILISATEURS & LOGS
# ============================================

class User(Base):
    """Utilisateurs de l'administration avec rôles hiérarchiques."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String(200), unique=True, nullable=False, index=True
    )
    password_hash = Column(String(200), nullable=False)
    nom = Column(String(150), nullable=True)
    role = Column(
        String(30),
        default="observateur",
        comment="superadmin, redacteur, gestionnaire, support, observateur, commercial"
    )
    actif = Column(Boolean, default=True)
    totp_secret = Column(String(100), nullable=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    # Relations
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"


class Log(Base):
    """Journal d'activité complet pour l'audit trail."""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action = Column(String(100), nullable=False)
    entite = Column(String(100), nullable=True)
    entite_id = Column(Integer, nullable=True)
    ancienne_valeur = Column(JSON, nullable=True)
    nouvelle_valeur = Column(JSON, nullable=True)
    ip = Column(String(45), nullable=True)
    timestamp = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    # Relations
    user = relationship("User", back_populates="logs")

    def __repr__(self):
        return f"<Log(action='{self.action}', user_id={self.user_id})>"


# ============================================
# PROJETS
# ============================================

class Projet(Base):
    """Projets réalisés - Portfolio principal."""
    __tablename__ = "projets"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description_courte = Column(Text, nullable=True)
    probleme_resolu = Column(Text, nullable=True)
    solution_apportee = Column(Text, nullable=True)
    resultats_chiffres = Column(Text, nullable=True)
    image_principale = Column(String(500), nullable=True)
    galerie_images = Column(JSON, nullable=True)
    technologies = Column(JSON, nullable=True)
    lien_github = Column(String(300), nullable=True)
    lien_site = Column(String(300), nullable=True)
    categorie = Column(
        String(50), nullable=True, comment="SaaS, Réservation, WhatsApp, API"
    )
    client_nom = Column(String(200), nullable=True)
    statut = Column(
        String(20), default="brouillon", comment="brouillon, publié, archivé"
    )
    featured = Column(Boolean, default=False)
    date_publication = Column(Date, nullable=True)
    temps_realisation = Column(String(50), nullable=True)
    donnees_simulateur_roi = Column(JSON, nullable=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    updated_at = Column(
        DateTime, onupdate=func.now(), nullable=True
    )

    # Relations
    temoignages = relationship(
        "Temoignage", back_populates="projet", cascade="all, delete-orphan"
    )
    articles = relationship(
        "Article", back_populates="projet", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Projet(titre='{self.titre}', statut='{self.statut}')>"


# ============================================
# ARTICLES
# ============================================

class Article(Base):
    """Articles de blog et études de cas."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    extrait = Column(Text, nullable=True)
    contenu = Column(Text, nullable=True, comment="Markdown")
    image_couverture = Column(String(500), nullable=True)
    categorie = Column(String(50), nullable=True)
    tags = Column(JSON, nullable=True)
    statut = Column(
        String(20), default="brouillon", comment="brouillon, publié, archivé"
    )
    featured = Column(Boolean, default=False)
    date_publication = Column(Date, nullable=True)
    temps_lecture = Column(
        Integer, nullable=True, comment="Minutes de lecture auto-calculées"
    )
    projet_id = Column(
        Integer, ForeignKey("projets.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    updated_at = Column(
        DateTime, onupdate=func.now(), nullable=True
    )

    # Relations
    projet = relationship("Projet", back_populates="articles")

    def __repr__(self):
        return f"<Article(titre='{self.titre}', statut='{self.statut}')>"


# ============================================
# TÉMOIGNAGES
# ============================================

class Temoignage(Base):
    """Témoignages clients avec notation."""
    __tablename__ = "temoignages"

    id = Column(Integer, primary_key=True, index=True)
    nom_client = Column(String(150), nullable=False)
    entreprise = Column(String(200), nullable=True)
    contenu = Column(Text, nullable=False)
    note = Column(Integer, nullable=True, comment="1-5 étoiles")
    photo_client = Column(String(500), nullable=True)
    date_temoignage = Column(Date, nullable=True)
    projet_id = Column(
        Integer, ForeignKey("projets.id", ondelete="SET NULL"), nullable=True
    )
    approuve = Column(Boolean, default=False)
    featured = Column(Boolean, default=False)
    video_url = Column(String(500), nullable=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    # Relations
    projet = relationship("Projet", back_populates="temoignages")

    def __repr__(self):
        return f"<Temoignage(client='{self.nom_client}', note={self.note})>"


# ============================================
# SERVICES
# ============================================

class Service(Base):
    """Services proposés par Bridge Afrika."""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    icone = Column(String(50), nullable=True, comment="Bootstrap Icons")
    tarif_indicatif = Column(String(100), nullable=True)
    duree_estimee = Column(String(100), nullable=True)
    processus = Column(Text, nullable=True)
    livrables = Column(Text, nullable=True)
    badge = Column(
        String(50), nullable=True, comment="Populaire, Nouveau, Best-seller"
    )
    ordre = Column(Integer, default=0)
    actif = Column(Boolean, default=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    def __repr__(self):
        return f"<Service(titre='{self.titre}', badge='{self.badge}')>"


# ============================================
# TECHNOLOGIES
# ============================================

class Technologie(Base):
    """Stack technique maîtrisée."""
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    icone_svg = Column(Text, nullable=True, comment="SVG inline")
    categorie = Column(
        String(50), nullable=True, comment="Backend, Frontend, Database, DevOps"
    )
    niveau = Column(
        String(30), nullable=True, comment="Débutant, Intermédiaire, Avancé, Expert"
    )
    doc_url = Column(String(300), nullable=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    def __repr__(self):
        return f"<Technologie(nom='{self.nom}', niveau='{self.niveau}')>"


# ============================================
# LIENS SOCIAUX
# ============================================

class LienSocial(Base):
    """Liens vers les réseaux sociaux et profils."""
    __tablename__ = "liens_sociaux"

    id = Column(Integer, primary_key=True, index=True)
    plateforme = Column(
        String(50), nullable=True, comment="GitHub, LinkedIn, WhatsApp, etc."
    )
    url = Column(String(300), nullable=False)
    icone = Column(String(50), nullable=True, comment="Bootstrap Icons")
    texte_alternatif = Column(String(100), nullable=True)
    actif = Column(Boolean, default=True)
    ordre = Column(Integer, default=0)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    def __repr__(self):
        return f"<LienSocial(plateforme='{self.plateforme}')>"


# ============================================
# MESSAGES (CRM)
# ============================================

class Message(Base):
    """Messages des visiteurs et leads CRM."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), nullable=True)
    email = Column(String(200), nullable=True)
    telephone = Column(String(30), nullable=True)
    contenu = Column(Text, nullable=True)
    source = Column(
        String(50), nullable=True, comment="formulaire, whatsapp, bridgescan, agent_ia"
    )
    projet_interesse = Column(String(200), nullable=True)
    statut_lead = Column(
        String(30), default="nouveau",
        comment="nouveau, contacte, negociation, gagne, perdu"
    )
    lu = Column(Boolean, default=False)
    repondu = Column(Boolean, default=False)
    note_interne = Column(Text, nullable=True)
    date_dernier_contact = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    def __repr__(self):
        return f"<Message(nom='{self.nom}', statut='{self.statut_lead}')>"


# ============================================
# MÉDIAS
# ============================================

class Media(Base):
    """Fichiers uploadés avec métadonnées."""
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, index=True)
    nom_fichier = Column(String(300), nullable=False)
    chemin = Column(String(500), nullable=False)
    type_mime = Column(String(100), nullable=True)
    taille_bytes = Column(Integer, nullable=True)
    largeur = Column(Integer, nullable=True)
    hauteur = Column(Integer, nullable=True)
    dossier = Column(
        String(50), default="general",
        comment="projets, blog, temoignages, profil, general"
    )
    titre_alt = Column(String(200), nullable=True)
    created_at = Column(
        DateTime, default=func.now(), server_default=func.now()
    )

    def __repr__(self):
        return f"<Media(fichier='{self.nom_fichier}', dossier='{self.dossier}')>"


# ============================================
# ABONNÉS NEWSLETTER
# ============================================

class AbonneNewsletter(Base):
    """Abonnés à la newsletter."""
    __tablename__ = "abonnes_newsletter"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    prenom = Column(String(100), nullable=True)
    actif = Column(Boolean, default=True)
    date_inscription = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    date_desinscription = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<AbonneNewsletter(email='{self.email}')>"