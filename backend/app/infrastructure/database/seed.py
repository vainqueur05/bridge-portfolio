"""
Script de seeding pour les données de développement.
Reflète l'écosystème réel de Bridge Afrika.
À exécuter une seule fois : python -m app.infrastructure.database.seed
"""

import asyncio
from datetime import date

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import async_session_maker, engine
from app.infrastructure.database.models import (
    Config, Projet, Article, Temoignage, Service, Technologie, LienSocial, User
)


async def seed_database():
    """Remplit la base de données avec les données réelles de Bridge Afrika."""
    async with async_session_maker() as session:
        # Vérifier si déjà seedé
        from sqlalchemy import select, func
        result = await session.execute(select(func.count()).select_from(Projet))
        if result.scalar() > 0:
            print("✅ Base déjà seedée, on skip.")
            return

        print("🌱 Début du seeding de l'écosystème Bridge Afrika...")

        # ============================================
        # 1. CONFIGURATION
        # ============================================
        configs = [
            Config(cle="identite_nom", valeur="Vainqueur Kalema"),
            Config(cle="identite_titre", valeur="Développeur Full Stack & Architecte SaaS - Fondateur de Bridge Afrika"),
            Config(cle="identite_bio", valeur="Je construis des ponts numériques entre l'Afrique et le monde. 7 SaaS en production. Basé à Lubumbashi, RDC."),
            Config(cle="identite_photo", valeur="/static/uploads/profil.jpg"),
            Config(cle="contact_email", valeur="vainqueurkalema035@gmail.com"),
            Config(cle="contact_telephone", valeur="+243 895 288 981"),
            Config(cle="contact_whatsapp", valeur="+243895288981"),
            Config(cle="contact_adresse", valeur="Lubumbashi, RDC"),
            Config(cle="apparence_theme", valeur="after-midnight"),
            Config(cle="apparence_primaire", valeur="#E65100"),
            Config(cle="apparence_secondaire", valeur="#D4AF37"),
            Config(cle="modules_blog", valeur="true"),
            Config(cle="modules_temoignages", valeur="true"),
            Config(cle="modules_bridgescan", valeur="true"),
            Config(cle="modules_agent_ia", valeur="true"),
            Config(cle="maintenance_mode", valeur="false"),
            Config(cle="seo_titre", valeur="Vainqueur Kalema | Développeur SaaS - Bridge Afrika"),
            Config(cle="seo_description", valeur="Portfolio de Vainqueur Kalema, développeur Full Stack à Lubumbashi. Spécialiste SaaS, APIs et automatisation pour l'Afrique."),
        ]
        session.add_all(configs)

        # ============================================
        # 2. UTILISATEUR ADMIN
        # ============================================
        admin = User(
            email="vainqueurkalema035@gmail.com",
            password_hash=bcrypt.hashpw("00kalema".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            nom="Vainqueur Kalema",
            role="superadmin",
            actif=True,
        )
        session.add(admin)

        # ============================================
        # 3. TECHNOLOGIES
        # ============================================
        technologies = [
            Technologie(nom="Python", categorie="Backend", niveau="Expert"),
            Technologie(nom="FastAPI", categorie="Backend", niveau="Expert"),
            Technologie(nom="PostgreSQL", categorie="Database", niveau="Avancé"),
            Technologie(nom="SQLite", categorie="Database", niveau="Expert"),
            Technologie(nom="Tailwind CSS", categorie="Frontend", niveau="Expert"),
            Technologie(nom="JavaScript", categorie="Frontend", niveau="Avancé"),
            Technologie(nom="Alpine.js", categorie="Frontend", niveau="Avancé"),
            Technologie(nom="Docker", categorie="DevOps", niveau="Intermédiaire"),
            Technologie(nom="Git", categorie="DevOps", niveau="Expert"),
            Technologie(nom="WhatsApp API", categorie="Intégration", niveau="Expert"),
            Technologie(nom="Africa's Talking", categorie="Intégration", niveau="Avancé"),
        ]
        session.add_all(technologies)

        # ============================================
        # 4. SERVICES
        # ============================================
        services = [
            Service(titre="Création de SaaS", description="Applications SaaS complètes, de l'idée au déploiement.", icone="bi-cloud-arrow-up", tarif_indicatif="À partir de 2 500 €", duree_estimee="6-12 semaines", badge="Populaire", ordre=1),
            Service(titre="APIs sur mesure", description="APIs RESTful performantes, documentées et sécurisées.", icone="bi-diagram-3", tarif_indicatif="À partir de 1 800 €", duree_estimee="4-8 semaines", badge="Best-seller", ordre=2),
            Service(titre="Automatisation WhatsApp", description="Bots WhatsApp intelligents pour votre relation client.", icone="bi-whatsapp", tarif_indicatif="À partir de 1 500 €", duree_estimee="3-6 semaines", badge="Nouveau", ordre=3),
            Service(titre="Diagnostic Numérique", description="Audit complet de votre présence en ligne.", icone="bi-search", tarif_indicatif="Gratuit / 150 €", duree_estimee="24h", ordre=4),
        ]
        session.add_all(services)

        # ============================================
        # 5. PROJETS
        # ============================================
        projets_data = [
            {"titre": "Hôtel Direct", "slug": "hotel-direct", "description_courte": "SaaS de réservation hôtelière 24h/24 avec QR code et WhatsApp.", "categorie": "Réservation", "statut": "publié", "featured": True, "date_publication": date(2026, 7, 1), "technologies": ["Python", "FastAPI", "Tailwind CSS", "WhatsApp API"]},
            {"titre": "Kelya", "slug": "kelya-gestion-salons", "description_courte": "Gestion invisible pour salons de coiffure. Zéro app, 100% WhatsApp.", "categorie": "WhatsApp", "statut": "publié", "featured": True, "date_publication": date(2026, 3, 15), "technologies": ["Python", "FastAPI", "WhatsApp API"]},
            {"titre": "École Facile", "slug": "ecole-facile", "description_courte": "Gestion scolaire invisible. Les parents reçoivent tout par SMS.", "categorie": "SaaS", "statut": "publié", "featured": True, "date_publication": date(2026, 4, 1), "technologies": ["Python", "FastAPI", "Africa's Talking"]},
            {"titre": "ALTER EGO", "slug": "alter-ego", "description_courte": "Assistant commercial IA pour freelances. Négocie 24h/24.", "categorie": "WhatsApp", "statut": "publié", "featured": True, "date_publication": date(2026, 5, 1), "technologies": ["Python", "FastAPI", "Hugging Face", "WhatsApp API"]},
            {"titre": "Verba", "slug": "verba-portfolio-agentique", "description_courte": "Le premier portfolio agentique d'Afrique.", "categorie": "SaaS", "statut": "publié", "featured": True, "date_publication": date(2026, 6, 15), "technologies": ["Python", "FastAPI", "Mistral 7B"]},
            {"titre": "Yebela v2", "slug": "yebela-riposte", "description_courte": "Plateforme nationale d'alerte citoyenne.", "categorie": "SaaS", "statut": "brouillon", "featured": False, "technologies": ["Python", "FastAPI", "Redis", "Africa's Talking"]},
            {"titre": "BridgeHub", "slug": "bridgehub", "description_courte": "Centre de contrôle unifié pour l'écosystème Bridge Afrika.", "categorie": "Dashboard", "statut": "brouillon", "featured": False, "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis"]},
        ]

        projets = []
        for data in projets_data:
            projet = Projet(**data)
            session.add(projet)
            projets.append(projet)

        await session.flush()

        # ============================================
        # 6. TÉMOIGNAGES
        # ============================================
        temoignages_data = [
            {"nom_client": "Marie K.", "entreprise": "Hôtel Le Cristal", "contenu": "Hôtel Direct a sauvé mon établissement. Les clients réservent à 3h du matin sans que je lève le petit doigt.", "note": 5, "projet_id": projets[0].id, "approuve": True, "featured": True},
            {"nom_client": "Maman Chantal", "entreprise": "Salon Chantal Coiffure", "contenu": "Kelya a changé ma vie. Mes coiffeuses envoient juste un SMS et tout est enregistré.", "note": 5, "projet_id": projets[1].id, "approuve": True, "featured": True},
            {"nom_client": "Directeur Kabamba", "entreprise": "Collège Saint-Exupéry", "contenu": "École Facile a transformé notre relation avec les parents. Plus aucun parent ne dit 'je ne savais pas'.", "note": 5, "projet_id": projets[2].id, "approuve": True, "featured": True},
            {"nom_client": "Abel M.", "entreprise": "Copywriter Pro", "contenu": "Verba est mon meilleur commercial. Vainqueur est un génie de l'IA appliquée.", "note": 5, "projet_id": projets[4].id, "approuve": True, "featured": False},
            {"nom_client": "Jean-Pierre M.", "entreprise": "Freelance Designer", "contenu": "ALTER EGO gère mes prospects mieux que je ne le ferais moi-même.", "note": 5, "projet_id": projets[3].id, "approuve": True, "featured": False},
        ]
        for data in temoignages_data:
            session.add(Temoignage(**data))

        # ============================================
        # 7. ARTICLES
        # ============================================
        articles_data = [
            {"titre": "Comment Hôtel Direct a été construit en 7 jours", "slug": "construction-hotel-direct-7-jours", "extrait": "Retour d'expérience sur le développement éclair d'un SaaS.", "categorie": "Étude de cas", "tags": ["FastAPI", "Tailwind CSS"], "statut": "publié", "featured": True, "date_publication": date(2026, 7, 5), "temps_lecture": 7},
            {"titre": "Pourquoi j'ai choisi FastAPI pour tous mes SaaS", "slug": "pourquoi-fastapi-saas-afrique", "extrait": "Les 7 raisons qui ont motivé ce choix stratégique.", "categorie": "Tutoriel", "tags": ["FastAPI", "Python"], "statut": "publié", "featured": True, "date_publication": date(2026, 6, 1), "temps_lecture": 5},
            {"titre": "L'Internet Invisible : quand WhatsApp remplace les apps", "slug": "internet-invisible-whatsapp-apps", "extrait": "En Afrique, le futur passe par WhatsApp et les SMS.", "categorie": "Réflexion", "tags": ["WhatsApp", "Afrique"], "statut": "publié", "featured": False, "date_publication": date(2026, 5, 15), "temps_lecture": 6},
            {"titre": "Clean Architecture avec FastAPI", "slug": "clean-architecture-fastapi-retour-experience", "extrait": "Ce qui marche, ce qui casse, ce que je ne referais pas.", "categorie": "Tutoriel", "tags": ["FastAPI", "Architecture"], "statut": "publié", "featured": True, "date_publication": date(2026, 4, 10), "temps_lecture": 10},
        ]
        for data in articles_data:
            session.add(Article(**data))

        # ============================================
        # 8. LIENS SOCIAUX
        # ============================================
        liens = [
            LienSocial(plateforme="GitHub", url="https://github.com/vainqueurkalema", icone="bi-github", ordre=1),
            LienSocial(plateforme="LinkedIn", url="https://linkedin.com/in/vainqueurkalema", icone="bi-linkedin", ordre=2),
            LienSocial(plateforme="WhatsApp", url="https://wa.me/243895288981", icone="bi-whatsapp", ordre=3),
            LienSocial(plateforme="Email", url="mailto:vainqueurkalema035@gmail.com", icone="bi-envelope", ordre=4),
        ]
        session.add_all(liens)

        await session.commit()
        print("✅ Seeding terminé avec succès !")
        print(f"   👤 1 admin (vainqueurkalema035@gmail.com / 00kalema)")
        print(f"   🛠️ {len(services)} services")
        print(f"   💻 {len(technologies)} technologies")
        print(f"   🗂️ {len(projets_data)} projets")
        print(f"   ⭐ {len(temoignages_data)} témoignages")
        print(f"   📝 {len(articles_data)} articles")
        print(f"   🔗 {len(liens)} liens sociaux")


async def main():
    await seed_database()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())