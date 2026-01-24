"""
🛠️ Package Tools - Tous les outils pour les agents LangChain
============================================================

Ce package regroupe tous les outils (tools) utilisables par les agents.
Import simplifié : from tools import tous_les_outils
"""

from .rag_clinitex import recherche_rapports_clinitex, init_retriever_clinitex
from .rag_cegedim import recherche_reglements_cegedim, init_retriever_cegedim
from .calculatrice import calculatrice, date_actuelle
from .recherche_web import recherche_web
from .email_tool import envoyer_email
from .graphiques import generer_graphique

# Liste de tous les outils disponibles (pratique pour les agents)
tous_les_outils = [
    recherche_rapports_clinitex,
    recherche_reglements_cegedim,
    calculatrice,
    date_actuelle,
    recherche_web,
    envoyer_email,
    generer_graphique
]

__all__ = [
    "recherche_rapports_clinitex",
    "init_retriever_clinitex",
    "recherche_reglements_cegedim",
    "init_retriever_cegedim",
    "calculatrice",
    "date_actuelle",
    "recherche_web",
    "envoyer_email",
    "generer_graphique",
    "tous_les_outils"
]
