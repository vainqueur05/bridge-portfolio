"""
API publique pour la configuration du site ET toutes les données publiques.
Un seul endpoint pour tout charger : /api/v1/site-config
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import (
    Config, Projet, Article, Temoignage, Service, Technologie, LienSocial
)

router = APIRouter()


@router.get("/site-config")
async def get_site_config(db: AsyncSession = Depends(get_db)):
    """
    Endpoint unique qui charge TOUTE la configuration publique du site.
    
    Retourne :
    - identite : nom, titre, bio, photo, cv
    - apparence : theme, couleurs, logo
    - contact : email, telephone, whatsapp, adresse
    - seo : titre, description, mots-cles, og_image
    - modules : activation/désactivation des fonctionnalités
    - projets : tous les projets publiés
    - articles : tous les articles publiés
    - temoignages : tous les témoignages approuvés
    - services : tous les services actifs
    - liens_sociaux : tous les liens sociaux actifs
    - technologies : toutes les technologies
    """
    
    # === 1. CONFIGURATION (table config) ===
    result = await db.execute(select(Config))
    configs = result.scalars().all()
    
    config_dict = {}
    for c in configs:
        config_dict[c.cle] = c.valeur
    
    # === 2. PROJETS PUBLIÉS ===
    projets_result = await db.execute(
        select(Projet)
        .where(Projet.statut == "publié")
        .order_by(Projet.date_publication.desc())
        .limit(20)
    )
    projets = projets_result.scalars().all()
    
    projets_list = []
    for p in projets:
        projets_list.append({
            "id": p.id,
            "titre": p.titre,
            "slug": p.slug,
            "description_courte": p.description_courte,
            "probleme_resolu": p.probleme_resolu,
            "solution_apportee": p.solution_apportee,
            "resultats_chiffres": p.resultats_chiffres,
            "image_principale": p.image_principale,
            "galerie_images": p.galerie_images or [],
            "technologies": p.technologies or [],
            "lien_github": p.lien_github,
            "lien_site": p.lien_site,
            "categorie": p.categorie,
            "client_nom": p.client_nom,
            "featured": p.featured,
            "date_publication": str(p.date_publication) if p.date_publication else None,
            "temps_realisation": p.temps_realisation,
            "donnees_simulateur_roi": p.donnees_simulateur_roi,
            "created_at": str(p.created_at) if p.created_at else None,
        })
    
    # === 3. ARTICLES PUBLIÉS ===
    articles_result = await db.execute(
        select(Article)
        .where(Article.statut == "publié")
        .order_by(Article.date_publication.desc())
        .limit(10)
    )
    articles = articles_result.scalars().all()
    
    articles_list = []
    for a in articles:
        articles_list.append({
            "id": a.id,
            "titre": a.titre,
            "slug": a.slug,
            "extrait": a.extrait,
            "contenu": a.contenu,
            "image_couverture": a.image_couverture,
            "categorie": a.categorie,
            "tags": a.tags or [],
            "featured": a.featured,
            "date_publication": str(a.date_publication) if a.date_publication else None,
            "temps_lecture": a.temps_lecture,
            "projet_id": a.projet_id,
            "created_at": str(a.created_at) if a.created_at else None,
        })
    
    # === 4. TÉMOIGNAGES APPROUVÉS ===
    temoignages_result = await db.execute(
        select(Temoignage)
        .where(Temoignage.approuve == True)
        .order_by(Temoignage.date_temoignage.desc())
        .limit(20)
    )
    temoignages = temoignages_result.scalars().all()
    
    temoignages_list = []
    for t in temoignages:
        temoignages_list.append({
            "id": t.id,
            "nom_client": t.nom_client,
            "entreprise": t.entreprise,
            "contenu": t.contenu,
            "note": t.note,
            "photo_client": t.photo_client,
            "date_temoignage": str(t.date_temoignage) if t.date_temoignage else None,
            "projet_id": t.projet_id,
            "featured": t.featured,
            "video_url": t.video_url,
            "created_at": str(t.created_at) if t.created_at else None,
        })
    
    # === 5. SERVICES ACTIFS ===
    services_result = await db.execute(
        select(Service)
        .where(Service.actif == True)
        .order_by(Service.ordre.asc())
        .limit(20)
    )
    services = services_result.scalars().all()
    
    services_list = []
    for s in services:
        services_list.append({
            "id": s.id,
            "titre": s.titre,
            "description": s.description,
            "icone": s.icone,
            "tarif_indicatif": s.tarif_indicatif,
            "duree_estimee": s.duree_estimee,
            "processus": s.processus,
            "livrables": s.livrables,
            "badge": s.badge,
            "ordre": s.ordre,
            "created_at": str(s.created_at) if s.created_at else None,
        })
    
    # === 6. LIENS SOCIAUX ACTIFS ===
    liens_result = await db.execute(
        select(LienSocial)
        .where(LienSocial.actif == True)
        .order_by(LienSocial.ordre.asc())
        .limit(20)
    )
    liens = liens_result.scalars().all()
    
    liens_list = []
    for l in liens:
        liens_list.append({
            "id": l.id,
            "plateforme": l.plateforme,
            "url": l.url,
            "icone": l.icone,
            "texte_alternatif": l.texte_alternatif,
            "ordre": l.ordre,
        })
    
    # === 7. TECHNOLOGIES ===
    technos_result = await db.execute(
        select(Technologie).order_by(Technologie.nom.asc())
    )
    technos = technos_result.scalars().all()
    
    technos_list = []
    for tech in technos:
        technos_list.append({
            "id": tech.id,
            "nom": tech.nom,
            "icone_svg": tech.icone_svg,
            "categorie": tech.categorie,
            "niveau": tech.niveau,
            "doc_url": tech.doc_url,
        })
    
    # === RETOURNER TOUT ===
    return {
        # Identité du propriétaire
        "identite": {
            "nom": config_dict.get("identite_nom", "Vainqueur Kalema"),
            "titre": config_dict.get("identite_titre", "Développeur Full Stack & Consultant Digital"),
            "bio": config_dict.get("identite_bio", "Je construis des solutions SaaS sur mesure pour les entrepreneurs africains."),
            "photo": config_dict.get("identite_photo", "/static/uploads/profile.jpg"),
            "cv": config_dict.get("identite_cv", ""),
        },
        
        # Apparence du site
        "apparence": {
            "theme": config_dict.get("apparence_theme", "after-midnight"),
            "primaire": config_dict.get("apparence_primaire", "#00FF41"),
            "secondaire": config_dict.get("apparence_secondaire", "#FF4500"),
            "logo": config_dict.get("apparence_logo", ""),
            "favicon": config_dict.get("apparence_favicon", ""),
        },
        
        # Coordonnées
        "contact": {
            "email": config_dict.get("contact_email", "contact@bridgeafrika.com"),
            "telephone": config_dict.get("contact_telephone", "+243000000000"),
            "whatsapp": config_dict.get("contact_whatsapp", "+243895288981"),
            "adresse": config_dict.get("contact_adresse", "Kinshasa, RDC"),
        },
        
        # SEO
        "seo": {
            "titre": config_dict.get("seo_titre", "Bridge Afrika | Portfolio Arcade"),
            "description": config_dict.get("seo_description", "Développeur Full Stack & Consultant Digital"),
            "mots_cles": config_dict.get("seo_mots_cles", ""),
            "og_image": config_dict.get("seo_og_image", "/static/uploads/og-default.jpg"),
        },
        
        # Modules activés/désactivés
        "modules": {
            "blog": config_dict.get("modules_blog", "true") == "true",
            "temoignages": config_dict.get("modules_temoignages", "true") == "true",
            "simulateur": config_dict.get("modules_simulateur", "true") == "true",
            "bridgescan": config_dict.get("modules_bridgescan", "true") == "true",
            "agent_ia": config_dict.get("modules_agent_ia", "false") == "true",
        },
        
        # Données dynamiques
        "projets": projets_list,
        "articles": articles_list,
        "temoignages": temoignages_list,
        "services": services_list,
        "liens_sociaux": liens_list,
        "technologies": technos_list,
        
        # Stats calculées
        "stats": {
            "projets_total": len(projets_list),
            "projets_featured": len([p for p in projets_list if p.get("featured")]),
            "articles_total": len(articles_list),
            "temoignages_total": len(temoignages_list),
            "services_total": len(services_list),
            "liens_total": len(liens_list),
            "technologies_total": len(technos_list),
        },
    }