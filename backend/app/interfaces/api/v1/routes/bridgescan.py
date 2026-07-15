"""
BridgeScan - Analyse stratégique de projet.
Évalue la viabilité d'un projet numérique pour le marché africain et global.
"""

import asyncio
import random
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class BridgeScanRequest(BaseModel):
    projet: str = Field(
        ...,
        min_length=15,
        max_length=800,
        description="Décrivez votre projet, votre cible, et le problème que vous résolvez."
    )
    budget: str = Field(
        ...,
        pattern="^(moins de 500\$|500\$ - 1500\$|1500\$ - 5000\$|5000\$ - 15000\$|15000\$ \+|sur devis)$",
        description="Fourchette budgétaire en dollars."
    )
    urgence: str = Field(
        ...,
        pattern="^(exploratoire|standard|prioritaire|critique)$",
        description="Niveau d'urgence du projet."
    )
    secteur: str = Field(
        default="non spécifié",
        pattern="^(transport|santé|éducation|finance|commerce|agriculture|logistique|non spécifié)$",
        description="Secteur d'activité principal."
    )
    localisation: str = Field(
        default="non spécifié",
        pattern="^(locale|nationale|régionale|continentale|mondiale)$",
        description="Portée géographique du projet."
    )


class BridgeScanResponse(BaseModel):
    score: int
    faisabilite: str
    estimation_temps: str
    estimation_budget: str
    recommandations: list[str]
    technologies_suggeres: list[str]
    risques: list[str]
    potentiel_marche: str


@router.post("/bridgescan/analyze", response_model=BridgeScanResponse)
async def analyze_project(data: BridgeScanRequest):
    """
    Analyse un projet et retourne un score de faisabilité réaliste,
    calibré pour le marché africain et international.
    """
    await asyncio.sleep(1.2)
    
    # Analyse de la clarté du projet (nombre de mots significatifs)
    mots_cles = [m for m in data.projet.lower().split() if len(m) > 3]
    clarte = int(min(len(mots_cles) * 1.8, 30))  # ← int ici
    
    # Bonus selon le budget (en dollars)
    bonus_budget = {
        "moins de 500$": -5,
        "500$ - 1500$": 5,
        "1500$ - 5000$": 15,
        "5000$ - 15000$": 25,
        "15000$ +": 30,
        "sur devis": 20,
    }
    
    # Bonus selon l'urgence
    bonus_urgence = {
        "exploratoire": 5,
        "standard": 12,
        "prioritaire": 18,
        "critique": 8,
    }
    
    # Bonus selon le secteur
    bonus_secteur = {
        "transport": 10,
        "santé": 15,
        "éducation": 15,
        "finance": 20,
        "commerce": 12,
        "agriculture": 10,
        "logistique": 12,
        "non spécifié": 0,
    }
    
    # Bonus selon la portée
    bonus_localisation = {
        "locale": 5,
        "nationale": 12,
        "régionale": 18,
        "continentale": 22,
        "mondiale": 25,
        "non spécifié": 0,
    }
    
    score = (
        clarte
        + bonus_budget.get(data.budget, 0)
        + bonus_urgence.get(data.urgence, 0)
        + bonus_secteur.get(data.secteur, 0)
        + bonus_localisation.get(data.localisation, 0)
    )
    
    # Analyse sectorielle
    if data.secteur == "finance":
        score += 5
        risques_base = ["Conformité réglementaire", "Sécurité des transactions", "Confiance utilisateur"]
    elif data.secteur == "santé":
        score += 3
        risques_base = ["Protection des données patients", "Intégration avec systèmes existants", "Adoption par le personnel médical"]
    elif data.secteur == "éducation":
        risques_base = ["Accessibilité hors ligne", "Adoption par les enseignants", "Coût des appareils"]
    else:
        risques_base = ["Adoption utilisateur", "Connectivité internet", "Maintenance technique"]
    
    # Ajustement selon la portée
    if data.localisation in ("continentale", "mondiale"):
        risques_base.append("Scalabilité infrastructure")
        risques_base.append("Multilinguisme et localisation")
    if data.localisation in ("locale", "nationale"):
        risques_base.append("Dépendance au marché local")
    
    # Budget insuffisant = risque supplémentaire
    if data.budget == "moins de 500$":
        risques_base.append("Budget critique : prototype uniquement")
        score -= 8
    
    # Conversion finale en int
    score = int(max(10, min(score, 98)))
    
    # Génération des résultats
    if score >= 80:
        faisabilite = "Très favorable"
        estimation = "4 à 8 semaines"
        estimation_budget = "1500$ - 5000$"
        recommandations = [
            "Projet mature, architecture scalable recommandée.",
            "Intégrer le paiement mobile (Airtel Money, Orange Money, M-Pesa) dès le MVP.",
            "Prévoir une version hors ligne ou low-data pour les zones à faible connectivité.",
            "Envisager une structure multi-tenant pour mutualiser les coûts.",
        ]
        technologies = ["FastAPI", "PostgreSQL", "Redis", "Docker", "Africa's Talking"]
        potentiel = "Élevé. Marché validé, exécution rapide recommandée."
    elif score >= 60:
        faisabilite = "Favorable"
        estimation = "8 à 14 semaines"
        estimation_budget = "800$ - 2500$"
        recommandations = [
            "Démarrer par un MVP ciblé sur une ville ou une région.",
            "Valider le besoin auprès de 10 utilisateurs réels avant de développer.",
            "Utiliser des canaux existants (WhatsApp, SMS) pour réduire la friction.",
            "Prévoir une phase de test de 2 semaines avec de vrais utilisateurs.",
        ]
        technologies = ["FastAPI", "SQLite", "Tailwind CSS", "Alpine.js"]
        potentiel = "Bon. Affiner la cible et tester rapidement."
    elif score >= 40:
        faisabilite = "Incertain"
        estimation = "12 à 20 semaines"
        estimation_budget = "500$ - 1500$"
        recommandations = [
            "Clarifier le problème principal avant de développer.",
            "Réaliser une étude de terrain (5 entretiens minimum).",
            "Commencer par un prototype no-code pour tester l'appétence.",
            "Revoir le périmètre : viser un seul cas d'usage critique.",
        ]
        technologies = ["Flask", "MySQL", "Bootstrap", "HTML/CSS/JS"]
        potentiel = "Incertain. Nécessite une validation terrain approfondie."
    else:
        faisabilite = "Défavorable en l'état"
        estimation = "20 semaines ou plus"
        estimation_budget = "Difficile à estimer"
        recommandations = [
            "Reformuler le problème. Est-il réel ? Douloureux ? Fréquent ?",
            "Étudier les solutions existantes (même informelles) avant de construire.",
            "Consulter un expert métier ou un mentor avant d'investir.",
            "Envisager un partenariat plutôt qu'un développement from scratch.",
        ]
        technologies = ["WordPress", "PHP", "MySQL", "HTML/CSS"]
        potentiel = "Faible en l'état. Revoir la proposition de valeur."
    
    random.shuffle(recommandations)
    random.shuffle(risques_base)
    
    return BridgeScanResponse(
        score=score,
        faisabilite=faisabilite,
        estimation_temps=estimation,
        estimation_budget=estimation_budget,
        recommandations=recommandations[:4],
        technologies_suggeres=technologies,
        risques=risques_base[:4],
        potentiel_marche=potentiel,
    )