"""
🔧 Leçon 10 : Tool Use Avancé - Outils Professionnels
=====================================================

Ce script montre les 3 façons de créer des outils LangChain :
1. @tool - Simple et rapide
2. StructuredTool - Validation Pydantic
3. BaseTool - Contrôle total (état, async, custom)

On crée ensuite un agent qui utilise ces outils.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, StructuredTool, BaseTool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field, field_validator
from typing import Type
import random

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ═══════════════════════════════════════════════════════════════════════════
# 1️⃣ MÉTHODE SIMPLE : @tool
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1️⃣ MÉTHODE @tool : Simple et rapide")
print("=" * 70)

@tool
def lancer_de(faces: int = 6) -> str:
    """Lance un dé et retourne le résultat.
    
    Args:
        faces: Nombre de faces du dé (par défaut 6)
    
    Returns:
        Le résultat du lancer
    """
    resultat = random.randint(1, faces)
    return f"🎲 Le dé à {faces} faces donne : {resultat}"


# Test direct
print(f"\n📝 Test de l'outil @tool :")
print(f"   {lancer_de.invoke({'faces': 20})}")
print(f"   Description : {lancer_de.description}")


# ═══════════════════════════════════════════════════════════════════════════
# 2️⃣ MÉTHODE INTERMÉDIAIRE : StructuredTool
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("2️⃣ MÉTHODE StructuredTool : Validation Pydantic")
print("=" * 70)


# Schéma des arguments avec validation
class CalculatriceArgs(BaseModel):
    """Arguments pour la calculatrice."""
    operation: str = Field(
        description="L'opération : 'addition', 'soustraction', 'multiplication', 'division'"
    )
    a: float = Field(description="Premier nombre")
    b: float = Field(description="Deuxième nombre")
    
    @field_validator('operation')
    @classmethod
    def valider_operation(cls, v):
        operations_valides = ['addition', 'soustraction', 'multiplication', 'division']
        if v.lower() not in operations_valides:
            raise ValueError(f"Opération invalide. Choisis parmi : {operations_valides}")
        return v.lower()


def calculer(operation: str, a: float, b: float) -> str:
    """Effectue le calcul demandé."""
    if operation == "addition":
        return f"{a} + {b} = {a + b}"
    elif operation == "soustraction":
        return f"{a} - {b} = {a - b}"
    elif operation == "multiplication":
        return f"{a} × {b} = {a * b}"
    elif operation == "division":
        if b == 0:
            return "❌ Erreur : Division par zéro impossible !"
        return f"{a} ÷ {b} = {a / b}"
    return "Opération inconnue"


# Créer l'outil avec gestion d'erreur
calculatrice = StructuredTool.from_function(
    func=calculer,
    name="calculatrice",
    description="Effectue des calculs mathématiques (addition, soustraction, multiplication, division)",
    args_schema=CalculatriceArgs,
    handle_tool_error=True  # Convertit les exceptions en messages
)

# Tests
print(f"\n📝 Test de l'outil StructuredTool :")
print(f"   {calculatrice.invoke({'operation': 'multiplication', 'a': 7, 'b': 6})}")
print(f"   {calculatrice.invoke({'operation': 'division', 'a': 10, 'b': 0})}")

# Test avec erreur de validation
try:
    print(f"   {calculatrice.invoke({'operation': 'racine', 'a': 9, 'b': 0})}")
except Exception as e:
    print(f"   ⚠️ Erreur capturée : {e}")


# ═══════════════════════════════════════════════════════════════════════════
# 3️⃣ MÉTHODE AVANCÉE : BaseTool (avec état)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("3️⃣ MÉTHODE BaseTool : Avec état persistant")
print("=" * 70)


class CompteurArgs(BaseModel):
    """Arguments pour le compteur."""
    action: str = Field(description="'incrementer', 'decrementer', 'reset' ou 'valeur'")
    valeur: int = Field(default=1, description="Valeur à ajouter/soustraire (défaut: 1)")


class CompteurTool(BaseTool):
    """Un compteur qui garde son état entre les appels."""
    
    name: str = "compteur"
    description: str = """Un compteur persistant. Actions possibles :
    - 'incrementer' : ajoute une valeur au compteur
    - 'decrementer' : soustrait une valeur du compteur  
    - 'reset' : remet le compteur à zéro
    - 'valeur' : affiche la valeur actuelle"""
    args_schema: Type[BaseModel] = CompteurArgs
    
    # État interne (persiste entre les appels !)
    compteur: int = 0
    historique: list = []
    
    def _run(self, action: str, valeur: int = 1) -> str:
        """Exécute l'action sur le compteur."""
        action = action.lower()
        
        if action == "incrementer":
            self.compteur += valeur
            self.historique.append(f"+{valeur}")
            return f"➕ Compteur incrémenté de {valeur}. Nouvelle valeur : {self.compteur}"
        
        elif action == "decrementer":
            self.compteur -= valeur
            self.historique.append(f"-{valeur}")
            return f"➖ Compteur décrémenté de {valeur}. Nouvelle valeur : {self.compteur}"
        
        elif action == "reset":
            self.compteur = 0
            self.historique.append("RESET")
            return f"🔄 Compteur remis à zéro."
        
        elif action == "valeur":
            return f"📊 Valeur actuelle : {self.compteur} | Historique : {' → '.join(self.historique[-5:])}"
        
        return f"❌ Action inconnue : {action}"


# Créer l'instance
compteur_tool = CompteurTool()

# Tests montrant la persistance de l'état
print(f"\n📝 Test de l'outil BaseTool (avec état) :")
print(f"   {compteur_tool.invoke({'action': 'incrementer', 'valeur': 5})}")
print(f"   {compteur_tool.invoke({'action': 'incrementer', 'valeur': 3})}")
print(f"   {compteur_tool.invoke({'action': 'decrementer', 'valeur': 2})}")
print(f"   {compteur_tool.invoke({'action': 'valeur'})}")


# ═══════════════════════════════════════════════════════════════════════════
# 4️⃣ OUTIL AVEC GESTION D'ERREUR PERSONNALISÉE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("4️⃣ Gestion d'erreur personnalisée")
print("=" * 70)


class ConversionArgs(BaseModel):
    """Arguments pour la conversion."""
    valeur: float = Field(description="La valeur à convertir")
    de_unite: str = Field(description="L'unité source (km, m, cm, mm)")
    vers_unite: str = Field(description="L'unité cible (km, m, cm, mm)")


def convertir_longueur(valeur: float, de_unite: str, vers_unite: str) -> str:
    """Convertit une longueur d'une unité à une autre."""
    # Tout convertir en mètres d'abord
    vers_metres = {"km": 1000, "m": 1, "cm": 0.01, "mm": 0.001}
    
    if de_unite not in vers_metres:
        raise ValueError(f"Unité source '{de_unite}' inconnue. Utilise : km, m, cm, mm")
    if vers_unite not in vers_metres:
        raise ValueError(f"Unité cible '{vers_unite}' inconnue. Utilise : km, m, cm, mm")
    
    en_metres = valeur * vers_metres[de_unite]
    resultat = en_metres / vers_metres[vers_unite]
    
    return f"📏 {valeur} {de_unite} = {resultat} {vers_unite}"


def handler_erreur_conversion(error: Exception) -> str:
    """Handler personnalisé pour les erreurs de conversion."""
    return f"⚠️ Conversion impossible : {str(error)}. Vérifie les unités (km, m, cm, mm)."


convertisseur = StructuredTool.from_function(
    func=convertir_longueur,
    name="convertisseur_longueur",
    description="Convertit des longueurs entre km, m, cm et mm",
    args_schema=ConversionArgs,
    handle_tool_error=handler_erreur_conversion
)

print(f"\n📝 Test avec handler d'erreur personnalisé :")
print(f"   {convertisseur.invoke({'valeur': 5, 'de_unite': 'km', 'vers_unite': 'm'})}")
print(f"   {convertisseur.invoke({'valeur': 100, 'de_unite': 'cm', 'vers_unite': 'mm'})}")
# Test avec erreur
print(f"   {convertisseur.invoke({'valeur': 10, 'de_unite': 'miles', 'vers_unite': 'm'})}")


# ═══════════════════════════════════════════════════════════════════════════
# 🤖 AGENT AVEC TOUS LES OUTILS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("🤖 AGENT avec tous les outils")
print("=" * 70)

# Liste de tous nos outils
tools = [lancer_de, calculatrice, compteur_tool, convertisseur]

# Créer l'agent
system_message = """Tu es un assistant polyvalent avec accès à plusieurs outils :
- Un dé pour les jeux
- Une calculatrice pour les maths
- Un compteur avec mémoire
- Un convertisseur de longueurs

Utilise le bon outil selon la demande."""

agent = create_react_agent(llm, tools, prompt=system_message)


def demander(question: str):
    """Envoie une question à l'agent."""
    print(f"\n❓ Question : {question}")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(f"🤖 Réponse : {result['messages'][-1].content}")


# Tests de l'agent
demander("Lance un dé à 20 faces pour moi")
demander("Combien font 15 multiplié par 7 ?")
demander("Incrémente le compteur de 10, puis de 5, puis dis-moi la valeur")
demander("Convertis 2.5 km en mètres")


# ═══════════════════════════════════════════════════════════════════════════
# 📚 RÉCAPITULATIF
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📚 RÉCAPITULATIF")
print("=" * 70)
print("""
🎯 Ce que tu as appris :

1. @tool
   - Le plus simple, parfait pour prototypes
   - Docstring = description de l'outil
   
2. StructuredTool
   - Validation Pydantic des arguments
   - @field_validator pour règles custom
   - handle_tool_error pour gérer les exceptions

3. BaseTool (classe)
   - État persistant entre les appels
   - Méthodes _run() et _arun() (async)
   - Contrôle total

💡 Conseils pro :
   - Descriptions DÉTAILLÉES = meilleur choix d'outil par l'agent
   - Retourner des messages d'erreur plutôt que lever des exceptions
   - Limiter la taille des retours pour ne pas exploser le contexte
   - Logger les appels pour le debugging
""")
