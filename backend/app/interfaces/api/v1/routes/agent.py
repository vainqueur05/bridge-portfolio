"""
Agent IA conversationnel pour le portfolio Bridge Afrika.
Intelligent : contexte, mémoire, émotions, actions réelles.
"""

import random
import re
from typing import Optional
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()

# ============================================
# MODÈLES
# ============================================

class AgentRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=500)
    session_id: str = Field(default="guest")
    contexte: str = Field(default="general")
    page_actuelle: str = Field(default="/")  # Page où se trouve le visiteur


class AgentResponse(BaseModel):
    reponse: str
    suggestions: list[str]
    action: Optional[str] = None  # "redirect", "call", "email", "devis", "scan", None
    action_data: Optional[str] = None  # URL, numéro, email selon l'action
    emotion: str = "neutre"  # Pour le frontend (emoji/ton)


# ============================================
# BASE DE CONNAISSANCES ENRICHIE
# ============================================

CONNAISSANCES = {
    "salutation": {
        "patterns": ["bonjour", "salut", "hello", "hey", "coucou", "bjr", "slt", "yo", "bonsoir", "salutations"],
        "reponses": [
            "Bonjour ! Je suis l'assistant de Vainqueur Kalema. Que puis-je pour vous ?",
            "Hello ! Bienvenue chez Bridge Afrika. Une question ?",
            "Salut ! Je suis là pour vous aider. Dites-moi tout.",
        ],
        "suggestions": ["Quels services ?", "Voir les projets", "Parler à Vainqueur"],
        "emotion": "chaleureux",
    },
    "identite": {
        "patterns": ["qui es-tu", "tu es qui", "ton nom", "chatbot", "robot", "ia", "assistant", "vainqueur"],
        "reponses": [
            "Je suis l'assistant IA de Vainqueur Kalema, développeur full-stack à Lubumbashi. Je connais tous ses projets et services. Posez-moi n'importe quelle question !",
        ],
        "suggestions": ["Voir le portfolio", "Parler à Vainqueur", "Quels services ?"],
        "emotion": "fier",
    },
    "services": {
        "patterns": ["service", "offre", "prestation", "que faites", "quoi", "proposez", "solution", "produit"],
        "reponses": [
            "Bridge Afrika propose 4 services :\n\n🖥️ Création de SaaS sur mesure\n🔌 APIs RESTful performantes\n🤖 Automatisation WhatsApp/SMS\n🔍 Diagnostic numérique gratuit (BridgeScan)\n\nLequel vous intéresse ?",
        ],
        "suggestions": ["SaaS sur mesure", "Automatisation WhatsApp", "BridgeScan gratuit"],
        "emotion": "professionnel",
    },
    "saas": {
        "patterns": ["saas", "application", "logiciel", "plateforme", "web app", "appli", "site web"],
        "reponses": [
            "Je construis des SaaS complets avec Python + FastAPI. Architecture propre, dashboard admin, notifications WhatsApp, et déploiement cloud. J'ai déjà livré 6 SaaS en production : Hôtel Direct, Kelya, École Facile, Yebela, ALTER EGO, et Verba. Lequel voulez-vous découvrir ?",
        ],
        "suggestions": ["Voir Hôtel Direct", "Voir Kelya", "Combien ça coûte ?"],
        "emotion": "passionné",
    },
    "prix": {
        "patterns": ["prix", "tarif", "coût", "budget", "combien", "cher", "euro", "€", "$", "gratuit"],
        "reponses": [
            "Voici mes tarifs indicatifs :\n• Site vitrine : à partir de 800 €\n• SaaS simple : 2 500 - 5 000 €\n• SaaS complexe : 5 000 - 15 000 €\n• API sur mesure : à partir de 1 800 €\n• Audit BridgeScan : version light gratuite, complète 150 €\n\nChaque projet est unique. Voulez-vous un devis personnalisé ?",
        ],
        "suggestions": ["Demander un devis", "BridgeScan gratuit", "Voir des exemples"],
        "emotion": "transparent",
        "action": None,
    },
    "devis": {
        "patterns": ["devis", "estimation", "proposition", "offre", "personnalisé", "projet"],
        "reponses": [
            "Excellente idée ! Pour un devis personnalisé, décrivez-moi votre projet en quelques mots (type de projet, secteur, fonctionnalités souhaitées). Je transmettrai à Vainqueur qui vous répondra sous 24h.",
        ],
        "suggestions": ["Décrire mon projet", "Appeler WhatsApp", "Voir les prix"],
        "emotion": "enthousiaste",
        "action": "redirect",
        "action_data": "/contact",
    },
    "contact": {
        "patterns": ["contact", "parler", "appeler", "whatsapp", "email", "joindre", "tel", "téléphone"],
        "reponses": [
            "📞 WhatsApp : +243 895 288 981\n📧 Email : vainqueurkalema035@gmail.com\n💼 LinkedIn : linkedin.com/in/vainqueurkalema\n\nVoulez-vous que j'ouvre WhatsApp directement ?",
        ],
        "suggestions": ["Ouvrir WhatsApp", "Envoyer un email", "Formulaire de contact"],
        "emotion": "serviable",
        "action": "call",
        "action_data": "https://wa.me/243895288981",
    },
    "delai": {
        "patterns": ["delai", "temps", "durée", "semaine", "mois", "quand", "rapide", "long"],
        "reponses": [
            "Mes délais moyens :\n• Site vitrine : 2-3 semaines\n• SaaS MVP : 6-8 semaines\n• SaaS complet : 8-12 semaines\n• API : 4-6 semaines\n\nJe livre toujours dans les temps. Un projet urgent ? Parlons-en !",
        ],
        "suggestions": ["Projet urgent", "Voir le processus", "Démarrer maintenant"],
        "emotion": "rassurant",
    },
    "processus": {
        "patterns": ["processus", "méthode", "étape", "comment travaillez", "fonctionne", "méthodologie"],
        "reponses": [
            "Ma méthode en 5 étapes :\n\n1️⃣ Analyse de vos besoins (gratuit)\n2️⃣ Prototype & maquettes\n3️⃣ Développement itératif (vous voyez l'avancement)\n4️⃣ Tests & validation\n5️⃣ Déploiement & formation\n\nVous recevez un accès à un dashboard dédié pour suivre l'avancement en temps réel.",
        ],
        "suggestions": ["Combien ça coûte ?", "Délais moyens", "Voir un exemple"],
        "emotion": "méthodique",
    },
    "projets": {
        "patterns": ["projet", "exemple", "realisation", "portfolio", "travail", "référence", "cas", "étude"],
        "reponses": [
            "J'ai 7 projets majeurs à vous montrer : Hôtel Direct (réservation), Kelya (gestion salons), École Facile (gestion scolaire), Yebela (alertes citoyennes), ALTER EGO (agent IA freelance), Verba (portfolio agentique), et BridgeHub (cockpit SaaS). Lequel voulez-vous découvrir ?",
        ],
        "suggestions": ["Voir Hôtel Direct", "Voir Kelya", "Voir tous les projets"],
        "emotion": "fier",
        "action": "redirect",
        "action_data": "/projets",
    },
    "bridgescan": {
        "patterns": ["scan", "diagnostic", "audit", "analyse", "score", "site", "check", "santé"],
        "reponses": [
            "BridgeScan est mon outil de diagnostic numérique gratuit. Collez l'URL de votre site, et je vous donne un score sur 100 avec des recommandations. Voulez-vous essayer maintenant ?",
        ],
        "suggestions": ["Lancer BridgeScan", "Comment ça marche ?", "Voir un exemple"],
        "emotion": "enthousiaste",
        "action": "redirect",
        "action_data": "/#bridgescan",
    },
    "remerciement": {
        "patterns": ["merci", "thanks", "super", "parfait", "top", "génial", "bye", "aurevoir", "adieu"],
        "reponses": [
            "Avec plaisir ! Si vous avez d'autres questions, je suis là. Bonne journée !",
            "Content d'avoir pu vous aider. À bientôt chez Bridge Afrika !",
        ],
        "suggestions": ["Voir les projets", "BridgeScan gratuit", "Parler à Vainqueur"],
        "emotion": "chaleureux",
    },
    "fallback": {
        "patterns": [],
        "reponses": [
            "Très intéressant ! Je n'ai pas la réponse exacte, mais Vainqueur peut vous aider. Voulez-vous que je lui transmette votre message ?",
            "Je n'ai pas encore appris cela, mais je transmets votre question à Vainqueur. Il vous répondra personnellement.",
        ],
        "suggestions": ["Parler à Vainqueur", "Voir les services", "BridgeScan gratuit"],
        "emotion": "humble",
        "action": "email",
        "action_data": "mailto:vainqueurkalema035@gmail.com",
    },
}


# ============================================
# MOTEUR D'INTELLIGENCE
# ============================================

# Mémoire simple des sessions (en production, utiliser Redis)
MEMOIRE: dict[str, list[str]] = {}


def nettoyer_message(message: str) -> str:
    """Nettoie et normalise le message entrant."""
    message = message.lower().strip()
    message = re.sub(r'[^\w\sàâäéèêëîïôöùûüç€$%]', ' ', message)
    message = re.sub(r'\s+', ' ', message)
    return message


def calculer_score(message: str, patterns: list[str]) -> float:
    """Calcule un score de correspondance entre le message et les patterns."""
    score = 0.0
    for pattern in patterns:
        if pattern in message:
            # Mot-clé exact : +0.5
            score += 0.5
        # Correspondance partielle
        if len(pattern) > 3 and pattern[:4] in message:
            score += 0.2
    return score


def detecter_emotion(message: str) -> str:
    """Détecte l'émotion du visiteur."""
    urgents = ["urgent", "vite", "maintenant", "deadline", "asap", "immédiat"]
    frustres = ["pas clair", "compliqué", "difficile", "problème", "bug"]
    curieux = ["comment", "pourquoi", "explique", "détail"]
    enthousiastes = ["super", "génial", "top", "parfait", "excellent"]

    if any(m in message for m in urgents):
        return "urgent"
    if any(m in message for m in frustres):
        return "frustré"
    if any(m in message for m in curieux):
        return "curieux"
    if any(m in message for m in enthousiastes):
        return "enthousiaste"
    return "neutre"


def trouver_meilleure_reponse(message: str, historique: list[str]) -> dict:
    """
    Trouve la réponse la plus pertinente en analysant :
    1. Le message actuel
    2. Le contexte de la conversation (historique)
    3. Les patterns de chaque connaissance
    """
    message_clean = nettoyer_message(message)
    meilleure_cat = "fallback"
    meilleur_score = 0.0

    for categorie, data in CONNAISSANCES.items():
        if categorie == "fallback":
            continue
        score = calculer_score(message_clean, data["patterns"])
        if score > meilleur_score:
            meilleur_score = score
            meilleure_cat = categorie

    # Si le score est trop faible, vérifier le contexte de la conversation
    if meilleur_score < 0.3 and len(historique) >= 2:
        contexte = " ".join(historique[-2:])
        for categorie, data in CONNAISSANCES.items():
            if categorie == "fallback":
                continue
            score_contexte = calculer_score(contexte, data["patterns"])
            if score_contexte > meilleur_score:
                meilleur_score = score_contexte
                meilleure_cat = categorie

    return CONNAISSANCES[meilleure_cat]


# ============================================
# ENDPOINT
# ============================================

@router.post("/agent/chat", response_model=AgentResponse)
async def agent_chat(data: AgentRequest, request: Request):
    """
    Agent conversationnel intelligent.
    Comprend le contexte, se souvient des conversations, détecte les émotions.
    """
    # Récupérer ou initialiser l'historique de la session
    session_id = data.session_id
    if session_id not in MEMOIRE:
        MEMOIRE[session_id] = []
    historique = MEMOIRE[session_id]

    # Ajouter le message à l'historique
    historique.append(data.message)
    # Garder les 10 derniers messages max
    if len(historique) > 10:
        historique = historique[-10:]
        MEMOIRE[session_id] = historique

    # Trouver la meilleure réponse
    reponse_data = trouver_meilleure_reponse(data.message, historique)

    # Adapter la réponse selon l'émotion détectée
    emotion_visiteur = detecter_emotion(data.message)
    reponse_texte = random.choice(reponse_data["reponses"])

    # Si visiteur frustré, être plus empathique
    if emotion_visiteur == "frustré":
        reponse_texte = "Je comprends votre frustration. " + reponse_texte

    # Si visiteur urgent, proposer action directe
    if emotion_visiteur == "urgent":
        reponse_data["action"] = "call"
        reponse_data["action_data"] = "https://wa.me/243895288981"

    # Si visiteur sur la page projets, contextualiser
    if data.page_actuelle.startswith("/projets"):
        reponse_data["suggestions"].append("Voir un autre projet")

    # Suggestions aléatoires mais pertinentes
    suggestions = reponse_data["suggestions"].copy()
    random.shuffle(suggestions)

    return AgentResponse(
        reponse=reponse_texte,
        suggestions=suggestions[:3],
        action=reponse_data.get("action"),
        action_data=reponse_data.get("action_data"),
        emotion=reponse_data.get("emotion", "neutre"),
    )


@router.get("/agent/stats")
async def agent_stats():
    """Statistiques simples de l'agent."""
    total_sessions = len(MEMOIRE)
    total_messages = sum(len(h) for h in MEMOIRE.values())
    return {
        "sessions_actives": total_sessions,
        "messages_echanges": total_messages,
        "memoire_ok": True,
    }