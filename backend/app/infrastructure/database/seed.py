"""
Script de seeding pour les données de développement.
Reflète l'écosystème réel de Bridge Afrika.
À exécuter une seule fois : python -m app.infrastructure.database.seed
"""

import asyncio
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import async_session_maker, engine, Base
from app.infrastructure.database.models import (
    Config, Projet, Article, Temoignage, Service, Technologie, LienSocial, User
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
            Config(cle="identite_nom", valeur="Vainqueur Kalema", description="Nom complet"),
            Config(cle="identite_titre", valeur="Développeur Full Stack & Architecte SaaS", description="Titre professionnel"),
            Config(cle="identite_bio", valeur="Je construis des ponts numériques entre l'Afrique et le futur. 6 SaaS en production, 47+ clients satisfaits, 0 compromis sur la qualité.", description="Bio courte"),
            Config(cle="identite_photo", valeur="/static/uploads/profil.jpg", description="Photo de profil"),
            Config(cle="contact_email", valeur="vainqueurkalema035@gmail.com", description="Email de contact"),
            Config(cle="contact_telephone", valeur="+243 895 288 981", description="Téléphone"),
            Config(cle="contact_whatsapp", valeur="+243895288981", description="WhatsApp"),
            Config(cle="apparence_theme", valeur="after-midnight", description="Thème par défaut"),
            Config(cle="apparence_primaire", valeur="#B80F3C", description="Couleur primaire"),
            Config(cle="apparence_secondaire", valeur="#E8A8A0", description="Couleur secondaire"),
            Config(cle="apparence_accent", valeur="#D4AF37", description="Couleur d'accent"),
            Config(cle="modules_blog", valeur="true", description="Activer le blog"),
            Config(cle="modules_temoignages", valeur="true", description="Activer les témoignages"),
            Config(cle="modules_bridgescan", valeur="true", description="Activer BridgeScan"),
            Config(cle="modules_agent_ia", valeur="true", description="Activer l'agent IA"),
            Config(cle="maintenance_mode", valeur="false", description="Mode maintenance"),
            Config(cle="seo_titre", valeur="Vainqueur Kalema | Développeur SaaS - Bridge Afrika", description="Meta titre"),
            Config(cle="seo_description", valeur="Portfolio de Vainqueur Kalema, développeur full stack à Lubumbashi. Spécialiste SaaS, APIs, automatisation pour l'Afrique.", description="Meta description"),
        ]
        session.add_all(configs)

        # ============================================
        # 2. UTILISATEUR ADMIN
        # ============================================
        admin = User(
            email="vainqueurkalema035@gmail.com",
            password_hash=pwd_context.hash("00kalema"),
            nom="Vainqueur Kalema",
            role="superadmin",
            actif=True,
        )
        session.add(admin)

        # ============================================
        # 3. TECHNOLOGIES (Stack complète)
        # ============================================
        technologies = [
            Technologie(nom="Python", categorie="Backend", niveau="Expert", doc_url="https://python.org"),
            Technologie(nom="FastAPI", categorie="Backend", niveau="Expert", doc_url="https://fastapi.tiangolo.com"),
            Technologie(nom="Flask", categorie="Backend", niveau="Avancé", doc_url="https://flask.palletsprojects.com"),
            Technologie(nom="PostgreSQL", categorie="Database", niveau="Avancé", doc_url="https://postgresql.org"),
            Technologie(nom="SQLite", categorie="Database", niveau="Expert", doc_url="https://sqlite.org"),
            Technologie(nom="Redis", categorie="Database", niveau="Intermédiaire", doc_url="https://redis.io"),
            Technologie(nom="HTML5", categorie="Frontend", niveau="Expert", doc_url="https://developer.mozilla.org"),
            Technologie(nom="CSS3", categorie="Frontend", niveau="Expert", doc_url="https://developer.mozilla.org"),
            Technologie(nom="Tailwind CSS", categorie="Frontend", niveau="Expert", doc_url="https://tailwindcss.com"),
            Technologie(nom="JavaScript", categorie="Frontend", niveau="Avancé", doc_url="https://developer.mozilla.org"),
            Technologie(nom="Alpine.js", categorie="Frontend", niveau="Avancé", doc_url="https://alpinejs.dev"),
            Technologie(nom="Docker", categorie="DevOps", niveau="Intermédiaire", doc_url="https://docker.com"),
            Technologie(nom="Git", categorie="DevOps", niveau="Expert", doc_url="https://git-scm.com"),
            Technologie(nom="Render", categorie="DevOps", niveau="Avancé", doc_url="https://render.com"),
            Technologie(nom="WhatsApp API", categorie="Intégration", niveau="Expert", doc_url="https://developers.facebook.com"),
            Technologie(nom="Africa's Talking", categorie="Intégration", niveau="Avancé", doc_url="https://africastalking.com"),
        ]
        session.add_all(technologies)

        # ============================================
        # 4. SERVICES
        # ============================================
        services = [
            Service(
                titre="Création de SaaS",
                description="Je conçois et développe des applications SaaS complètes, de l'idée au déploiement. Architecture propre, scalable, pensée pour durer 10 ans.",
                icone="bi-cloud-arrow-up",
                tarif_indicatif="À partir de 2 500 €",
                duree_estimee="6-12 semaines",
                processus="1. Audit du besoin\n2. Architecture & maquettes\n3. Développement agile\n4. Tests & déploiement\n5. Maintenance 6 mois offerte",
                livrables="Application déployée, code source, documentation, formation admin, support 6 mois",
                badge="Populaire",
                ordre=1,
            ),
            Service(
                titre="APIs sur mesure",
                description="Conception d'APIs RESTful performantes, documentées et sécurisées. Prêtes à intégrer WhatsApp, SMS, Mobile Money.",
                icone="bi-diagram-3",
                tarif_indicatif="À partir de 1 800 €",
                duree_estimee="4-8 semaines",
                processus="1. Spécification OpenAPI\n2. Développement FastAPI\n3. Tests unitaires & intégration\n4. Documentation Swagger\n5. Déploiement",
                livrables="API documentée, tests, collection Postman, guide d'intégration, support 3 mois",
                badge="Best-seller",
                ordre=2,
            ),
            Service(
                titre="Automatisation WhatsApp",
                description="Automatisez votre relation client avec des bots WhatsApp intelligents. Commandes, réservations, notifications : tout par SMS.",
                icone="bi-whatsapp",
                tarif_indicatif="À partir de 1 500 €",
                duree_estimee="3-6 semaines",
                processus="1. Définition des scénarios\n2. Développement du bot\n3. Intégration WhatsApp Cloud API\n4. Tests utilisateurs\n5. Formation & suivi",
                livrables="Bot déployé, scénarios documentés, tableau de bord admin, support 2 mois",
                badge="Nouveau",
                ordre=3,
            ),
            Service(
                titre="Diagnostic Numérique (BridgeScan)",
                description="Audit complet de votre présence en ligne. Je scanne votre site et vous livre un rapport avec score et recommandations.",
                icone="bi-search",
                tarif_indicatif="Gratuit (version light) / 150 € (complet)",
                duree_estimee="24h",
                processus="1. Scan automatique\n2. Analyse manuelle\n3. Rapport détaillé\n4. Recommandations priorisées\n5. Roadmap personnalisée",
                livrables="Rapport PDF, score détaillé, plan d'action, devis estimatif",
                badge=None,
                ordre=4,
            ),
        ]
        session.add_all(services)

        # ============================================
        # 5. PROJETS (Les 6 SaaS réels + BridgeHub)
        # ============================================
        projets_data = [
            {
                "titre": "Hôtel Direct",
                "slug": "hotel-direct",
                "description_courte": "SaaS de réservation hôtelière 24h/24 avec QR code et WhatsApp.",
                "probleme_resolu": "Les hôtels perdent 40% de clients la nuit car personne ne répond au téléphone.",
                "solution_apportee": "Une page de réservation en ligne disponible 24h/24, couplée à un système de QR code et des confirmations WhatsApp automatiques.",
                "resultats_chiffres": "95% des demandes nocturnes captées. +30% de réservations en 3 mois.",
                "technologies": ["Python", "FastAPI", "SQLite", "Tailwind CSS", "Alpine.js", "WhatsApp API"],
                "categorie": "Réservation",
                "client_nom": "Projet interne Bridge Afrika",
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 7, 1),
                "temps_realisation": "7 jours",
            },
            {
                "titre": "Kelya",
                "slug": "kelya-gestion-salons",
                "description_courte": "Gestion invisible pour salons de coiffure. Zéro app, 100% WhatsApp.",
                "probleme_resolu": "Les salons de coiffure gèrent leurs rendez-vous sur papier. 70% de no-show sans rappel.",
                "solution_apportee": "Un système de gestion par SMS/WhatsApp : prise de RDV, rappels automatiques, caisse, statistiques. Le coiffeur ne change rien à ses habitudes.",
                "resultats_chiffres": "-70% de rendez-vous oubliés. +25% de chiffre d'affaires pour le salon pilote.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "WhatsApp API", "Africa's Talking", "PWA"],
                "categorie": "WhatsApp",
                "client_nom": "Projet interne Bridge Afrika",
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 3, 15),
                "temps_realisation": "8 semaines",
            },
            {
                "titre": "École Facile",
                "slug": "ecole-facile",
                "description_courte": "Gestion scolaire invisible. Les parents reçoivent tout par SMS.",
                "probleme_resolu": "Les écoles congolaises gèrent tout sur papier. Les parents ne savent rien avant la fin du trimestre.",
                "solution_apportee": "Un dashboard web pour l'école + des SMS automatiques pour les parents : notes, absences, paiements, convocations. Zéro application.",
                "resultats_chiffres": "100% des parents informés en temps réel. Paiements en hausse de 40%.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "PWA", "Africa's Talking", "WeasyPrint"],
                "categorie": "SaaS",
                "client_nom": "Projet interne Bridge Afrika",
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 4, 1),
                "temps_realisation": "10 semaines",
            },
            {
                "titre": "Yebela v2 + RIPOSTE",
                "slug": "yebela-riposte",
                "description_courte": "Plateforme nationale d'alerte citoyenne. SMS, appels vocaux, anges gardiens.",
                "probleme_resolu": "Les citoyens n'ont aucun moyen rapide de signaler un danger. Les forces de l'ordre sont injoignables.",
                "solution_apportee": "Un système d'alerte par SMS et appels vocaux qui déclenche une chaîne de solidarité (anges gardiens de niveau 1, 2, 3) en moins de 60 secondes.",
                "resultats_chiffres": "Temps d'alerte réduit de 45 minutes à 45 secondes. Pilote validé à Lubumbashi.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Africa's Talking", "WebSocket"],
                "categorie": "SaaS",
                "client_nom": "Projet interne Bridge Afrika",
                "statut": "brouillon",
                "featured": False,
                "date_publication": None,
                "temps_realisation": "En cours",
            },
            {
                "titre": "ALTER EGO",
                "slug": "alter-ego",
                "description_courte": "Assistant commercial IA pour freelances. Négocie et envoie des devis 24h/24.",
                "probleme_resolu": "Les freelances passent 30% de leur temps à répondre aux prospects au lieu de coder.",
                "solution_apportee": "Un agent IA connecté à WhatsApp, Email et Messenger qui qualifie les leads, négocie selon des règles strictes, génère des devis PDF et récolte des témoignages.",
                "resultats_chiffres": "80% des premiers contacts gérés sans intervention humaine. Temps commercial divisé par 5.",
                "technologies": ["Python", "FastAPI", "SQLite", "Hugging Face", "WhatsApp API", "WeasyPrint"],
                "categorie": "WhatsApp",
                "client_nom": "Projet interne Bridge Afrika",
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 5, 1),
                "temps_realisation": "6 semaines",
            },
            {
                "titre": "Verba",
                "slug": "verba-portfolio-agentique",
                "description_courte": "Le premier portfolio agentique d'Afrique. Il écrit pour le visiteur en temps réel.",
                "probleme_resolu": "Les copywriters peinent à démontrer leur talent. Un portfolio statique ne prouve rien.",
                "solution_apportee": "Un portfolio qui intègre un traducteur de style en direct : le visiteur colle son texte, l'IA le réécrit dans le style du copywriter. Démonstration vivante du talent.",
                "resultats_chiffres": "3x plus de demandes de devis qu'un portfolio classique. 200+ traductions générées le premier mois.",
                "technologies": ["Python", "FastAPI", "SQLite", "Mistral 7B", "WhatsApp API", "Tailwind CSS"],
                "categorie": "SaaS",
                "client_nom": "Abel, Copywriter Pro",
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 6, 15),
                "temps_realisation": "7 jours",
            },
            {
                "titre": "BridgeHub",
                "slug": "bridgehub",
                "description_courte": "Centre de contrôle unifié pour tout l'écosystème Bridge Afrika.",
                "probleme_resolu": "Gérer 6 SaaS indépendants prend 2h par jour. Impossible d'avoir une vue d'ensemble.",
                "solution_apportee": "Un cockpit unique qui se connecte à chaque SaaS via des APIs internes sécurisées. Vue globale, actions groupées, logs centralisés, santé en temps réel.",
                "resultats_chiffres": "Temps d'administration divisé par 10. Visibilité totale sur l'écosystème.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "HMAC", "Chart.js"],
                "categorie": "Dashboard",
                "client_nom": "Projet interne Bridge Afrika",
                "statut": "brouillon",
                "featured": False,
                "date_publication": None,
                "temps_realisation": "En cours",
            },
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
            {
                "nom_client": "Marie K.",
                "entreprise": "Hôtel Le Cristal, Lubumbashi",
                "contenu": "Hôtel Direct a sauvé mon établissement. Avant, je perdais des clients chaque nuit. Maintenant, ils réservent à 3h du matin sans que je lève le petit doigt. Le QR code dans le hall est devenu notre signature.",
                "note": 5,
                "projet_id": projets[0].id,
                "approuve": True,
                "featured": True,
                "date_temoignage": date(2026, 7, 10),
            },
            {
                "nom_client": "Maman Chantal",
                "entreprise": "Salon Chantal Coiffure, Lubumbashi",
                "contenu": "Kelya a changé ma vie. Mes coiffeuses envoient juste un SMS et tout est enregistré. Les clientes reçoivent un rappel automatique. Je n'ai plus jamais perdu un rendez-vous.",
                "note": 5,
                "projet_id": projets[1].id,
                "approuve": True,
                "featured": True,
                "date_temoignage": date(2026, 4, 20),
            },
            {
                "nom_client": "Directeur Kabamba",
                "entreprise": "Collège Saint-Exupéry, Likasi",
                "contenu": "École Facile a transformé notre relation avec les parents. Ils reçoivent les notes par SMS, les convocations, les reçus de paiement. Plus aucun parent ne dit 'je ne savais pas'.",
                "note": 5,
                "projet_id": projets[2].id,
                "approuve": True,
                "featured": True,
                "date_temoignage": date(2026, 5, 10),
            },
            {
                "nom_client": "Abel M.",
                "entreprise": "Copywriter Pro, Kinshasa",
                "contenu": "Verba est mon meilleur commercial. Les clients potentiels testent le traducteur en direct, voient la magie opérer, et m'engagent dans la foulée. Vainqueur est un génie de l'IA appliquée.",
                "note": 5,
                "projet_id": projets[5].id,
                "approuve": True,
                "featured": False,
                "date_temoignage": date(2026, 6, 20),
            },
            {
                "nom_client": "Jean-Pierre M.",
                "entreprise": "Freelance Designer, Lubumbashi",
                "contenu": "ALTER EGO gère mes prospects mieux que je ne le ferais moi-même. Il est poli, professionnel, et ne dort jamais. J'ai gagné 3 clients le premier mois sans décrocher mon téléphone.",
                "note": 5,
                "projet_id": projets[4].id,
                "approuve": True,
                "featured": False,
                "date_temoignage": date(2026, 5, 25),
            },
            {
                "nom_client": "Maire Adjoint Katuba",
                "entreprise": "Commune de Katuba, Lubumbashi",
                "contenu": "Yebela est une révolution pour la sécurité de nos citoyens. Le système d'anges gardiens est parfaitement adapté à nos réalités. Nous espérons un déploiement national.",
                "note": 5,
                "projet_id": projets[3].id,
                "approuve": True,
                "featured": False,
                "date_temoignage": date(2026, 6, 1),
            },
        ]

        for data in temoignages_data:
            temoignage = Temoignage(**data)
            session.add(temoignage)

        # ============================================
        # 7. ARTICLES DE BLOG
        # ============================================
        articles_data = [
            {
                "titre": "Comment Hôtel Direct a été construit en 7 jours",
                "slug": "construction-hotel-direct-7-jours",
                "extrait": "Retour d'expérience sur le développement éclair d'un SaaS de réservation hôtelière avec FastAPI et Tailwind CSS.",
                "contenu": "## Le défi\n\nUn hôtel de Lubumbashi perdait 40% de ses clients la nuit. En 7 jours, j'ai conçu et déployé une solution complète.\n\n## La stack\n\nFastAPI, SQLite, Tailwind CSS, Alpine.js, WhatsApp Cloud API.\n\n## Le résultat\n\n95% des demandes nocturnes sont maintenant captées automatiquement.",
                "categorie": "Étude de cas",
                "tags": ["FastAPI", "Tailwind CSS", "WhatsApp", "Hôtellerie"],
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 7, 5),
                "temps_lecture": 7,
                "projet_id": projets[0].id,
            },
            {
                "titre": "Pourquoi j'ai choisi FastAPI pour tous mes SaaS",
                "slug": "pourquoi-fastapi-saas-afrique",
                "extrait": "FastAPI est devenu mon framework de prédilection. Voici les 7 raisons qui ont motivé ce choix stratégique.",
                "contenu": "## Performance\n\nFastAPI est aussi rapide que Node.js, mais avec la sécurité de typage de Python.\n\n## Documentation automatique\n\nSwagger intégré, pas de configuration.\n\n## Asynchrone natif\n\nParfait pour les intégrations WhatsApp et SMS.",
                "categorie": "Tutoriel",
                "tags": ["FastAPI", "Python", "Architecture", "SaaS"],
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 6, 1),
                "temps_lecture": 5,
                "projet_id": None,
            },
            {
                "titre": "L'Internet Invisible : quand WhatsApp remplace les apps",
                "slug": "internet-invisible-whatsapp-apps",
                "extrait": "En Afrique, le futur du numérique ne passe pas par les stores d'applications. Il passe par WhatsApp et les SMS.",
                "contenu": "## Le constat\n\n90% des Africains utilisent WhatsApp. Moins de 20% téléchargent des applications.\n\n## La solution\n\nConcevoir des services qui s'intègrent dans les usages existants. Pas d'installation. Pas de mot de passe. Juste un numéro de téléphone.",
                "categorie": "Réflexion",
                "tags": ["WhatsApp", "Afrique", "UX", "No-code"],
                "statut": "publié",
                "featured": False,
                "date_publication": date(2026, 5, 15),
                "temps_lecture": 6,
                "projet_id": None,
            },
            {
                "titre": "BridgeHub : comment j'ai unifié mes 6 SaaS en un seul cockpit",
                "slug": "bridgehub-cockpit-saas",
                "extrait": "Gérer 6 projets en parallèle était un cauchemar. Voici comment j'ai construit un centre de contrôle unique.",
                "contenu": "## Le problème\n\n6 SaaS, 6 dashboards, 6 jeux de logs. 2h par jour rien que pour checker.\n\n## La solution\n\nUn CommandCenter qui se connecte à chaque SaaS via des APIs internes signées HMAC.",
                "categorie": "Étude de cas",
                "tags": ["Architecture", "SaaS", "API", "DevOps"],
                "statut": "brouillon",
                "featured": False,
                "date_publication": None,
                "temps_lecture": 8,
                "projet_id": projets[6].id,
            },
            {
                "titre": "Clean Architecture avec FastAPI : mon retour après 7 projets",
                "slug": "clean-architecture-fastapi-retour-experience",
                "extrait": "J'ai appliqué la Clean Architecture sur tous mes SaaS. Voici ce qui marche, ce qui casse, et ce que je ne referais pas.",
                "contenu": "## Les 4 couches\n\nDomain, Application, Infrastructure, Interfaces. Chaque couche a un rôle précis.\n\n## Ce qui marche\n\nLes use cases en classes avec execute(). Les repositories en abstractions. L'indépendance totale du framework.\n\n## Ce que j'ai appris\n\nNe pas sur-architecturer au début. Laisser les abstractions émerger du code.",
                "categorie": "Tutoriel",
                "tags": ["FastAPI", "Clean Architecture", "Python", "Best Practices"],
                "statut": "publié",
                "featured": True,
                "date_publication": date(2026, 4, 10),
                "temps_lecture": 10,
                "projet_id": None,
            },
        ]

        for data in articles_data:
            article = Article(**data)
            session.add(article)

        # ============================================
        # 8. LIENS SOCIAUX
        # ============================================
        liens = [
            LienSocial(plateforme="GitHub", url="https://github.com/vainqueurkalema", icone="bi-github", texte_alternatif="Mon code open source", ordre=1),
            LienSocial(plateforme="LinkedIn", url="https://linkedin.com/in/vainqueurkalema", icone="bi-linkedin", texte_alternatif="Mon profil professionnel", ordre=2),
            LienSocial(plateforme="WhatsApp", url="https://wa.me/243895288981", icone="bi-whatsapp", texte_alternatif="Contactez-moi directement", ordre=3),
            LienSocial(plateforme="Email", url="mailto:vainqueurkalema035@gmail.com", icone="bi-envelope", texte_alternatif="M'envoyer un email", ordre=4),
            LienSocial(plateforme="YouTube", url="https://youtube.com/@bridgeafrika", icone="bi-youtube", texte_alternatif="Tutoriels et démos", ordre=5),
        ]
        session.add_all(liens)

        # ============================================
        # COMMIT FINAL
        # ============================================
        await session.commit()
        print("✅ Seeding terminé avec succès !")
        print(f"   📊 {len(configs)} configurations")
        print(f"   👤 1 admin (vainqueurkalema035@gmail.com / 00kalema)")
        print(f"   🛠️ {len(services)} services")
        print(f"   💻 {len(technologies)} technologies")
        print(f"   🗂️ {len(projets_data)} projets :")
        for p in projets_data:
            emoji = "🟢" if p["statut"] == "publié" else "🟡"
            print(f"      {emoji} {p['titre']}")
        print(f"   ⭐ {len(temoignages_data)} témoignages")
        print(f"   📝 {len(articles_data)} articles")
        print(f"   🔗 {len(liens)} liens sociaux")
        print(f"\n🎯 Écosystème Bridge Afrika prêt à être présenté au monde !")


async def main():
    """Point d'entrée principal. Les tables sont créées par Alembic (alembic upgrade head)."""
    await seed_database()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())