"""
⚔️ Leçon 7 : Chains vs Graphs - Comparaison Pratique
=====================================================

Ce script montre le MÊME problème résolu de deux façons :
1. Avec LCEL (Chains) - Approche linéaire
2. Avec LangGraph - Approche avec état et conditions

Problème : Un assistant qui analyse le sentiment d'un texte
et donne une réponse adaptée (encouragement ou félicitations).

Tu verras que :
- LCEL est plus concis pour les flux simples
- LangGraph permet d'ajouter des conditions et boucles
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

load_dotenv()

# Le modèle utilisé par les deux approches
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


# ═══════════════════════════════════════════════════════════════════════════
# 🔗 APPROCHE 1 : LCEL (Chains) - Flux Linéaire
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("🔗 APPROCHE 1 : LCEL (Chains)")
print("=" * 70)

# Avec LCEL, on doit tout faire en une seule chaîne linéaire
# Le LLM doit analyser ET répondre en même temps

prompt_lcel = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant empathique.
Analyse le sentiment du message (positif, négatif, neutre).
Puis réponds de manière adaptée :
- Si négatif : encourage et réconforte
- Si positif : félicite
- Si neutre : réponds normalement

Format ta réponse ainsi :
SENTIMENT: [positif/négatif/neutre]
RÉPONSE: [ta réponse adaptée]"""),
    ("human", "{message}")
])

# La chaîne : Prompt → LLM → Parser (tout linéaire)
chain_lcel = prompt_lcel | llm | StrOutputParser()

# Test
message_test = "J'ai raté mon examen et je suis vraiment déçu..."

print(f"\n📝 Message : \"{message_test}\"\n")
print("⏳ Traitement avec LCEL...")
result_lcel = chain_lcel.invoke({"message": message_test})
print(f"📤 Résultat :\n{result_lcel}")

print("\n" + "-" * 70)
print("💡 LCEL : Simple mais tout est fait en UN appel, pas de logique conditionnelle")
print("-" * 70)


# ═══════════════════════════════════════════════════════════════════════════
# 📊 APPROCHE 2 : LangGraph - Flux avec État et Conditions
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📊 APPROCHE 2 : LangGraph (avec conditions)")
print("=" * 70)


# 1. Définir l'état partagé entre les nœuds
class SentimentState(TypedDict):
    message: str           # Le message d'entrée
    sentiment: str         # Le sentiment détecté
    response: str          # La réponse générée


# 2. Nœud 1 : Analyser le sentiment
def analyze_sentiment(state: SentimentState) -> SentimentState:
    """Analyse le sentiment du message."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyse le sentiment de ce message. Réponds UNIQUEMENT par: positif, négatif ou neutre"),
        ("human", "{message}")
    ])
    chain = prompt | llm | StrOutputParser()
    sentiment = chain.invoke({"message": state["message"]}).strip().lower()
    print(f"   🔍 Sentiment détecté : {sentiment}")
    return {"sentiment": sentiment}


# 3. Nœuds de réponse (un par type de sentiment)
def respond_negative(state: SentimentState) -> SentimentState:
    """Réponse pour sentiment négatif."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "L'utilisateur est triste ou déçu. Réconforte-le avec empathie et encouragement."),
        ("human", "{message}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"message": state["message"]})
    print(f"   💙 Route : réponse_négative")
    return {"response": response}


def respond_positive(state: SentimentState) -> SentimentState:
    """Réponse pour sentiment positif."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "L'utilisateur est content. Félicite-le et partage sa joie !"),
        ("human", "{message}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"message": state["message"]})
    print(f"   💚 Route : réponse_positive")
    return {"response": response}


def respond_neutral(state: SentimentState) -> SentimentState:
    """Réponse pour sentiment neutre."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Réponds de manière informative et neutre."),
        ("human", "{message}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"message": state["message"]})
    print(f"   ⚪ Route : réponse_neutre")
    return {"response": response}


# 4. Fonction de routage (décide quelle branche prendre)
def route_by_sentiment(state: SentimentState) -> Literal["respond_negative", "respond_positive", "respond_neutral"]:
    """Décide quel nœud appeler selon le sentiment."""
    sentiment = state.get("sentiment", "").lower()
    if "négatif" in sentiment or "negatif" in sentiment or "negative" in sentiment:
        return "respond_negative"
    elif "positif" in sentiment or "positive" in sentiment:
        return "respond_positive"
    else:
        return "respond_neutral"


# 5. Construire le graphe
graph = StateGraph(SentimentState)

# Ajouter les nœuds
graph.add_node("analyze", analyze_sentiment)
graph.add_node("respond_negative", respond_negative)
graph.add_node("respond_positive", respond_positive)
graph.add_node("respond_neutral", respond_neutral)

# Définir les connexions
graph.add_edge(START, "analyze")  # Début → Analyse

# CONDITION : Après l'analyse, on route vers le bon nœud de réponse
graph.add_conditional_edges(
    "analyze",
    route_by_sentiment,
    {
        "respond_negative": "respond_negative",
        "respond_positive": "respond_positive",
        "respond_neutral": "respond_neutral"
    }
)

# Toutes les réponses mènent à la fin
graph.add_edge("respond_negative", END)
graph.add_edge("respond_positive", END)
graph.add_edge("respond_neutral", END)

# Compiler le graphe
app = graph.compile()


# Test avec le même message
print(f"\n📝 Message : \"{message_test}\"\n")
print("⏳ Traitement avec LangGraph...")
print("   📊 Étapes du graphe :")

result_graph = app.invoke({"message": message_test})
print(f"\n📤 Résultat :\n{result_graph['response']}")

print("\n" + "-" * 70)
print("💡 LangGraph : Plus verbeux mais permet des VRAIES conditions")
print("   Le flux a pris un chemin différent selon le sentiment détecté !")
print("-" * 70)


# ═══════════════════════════════════════════════════════════════════════════
# 🧪 TEST COMPARATIF : Message Positif
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("🧪 TEST BONUS : Message Positif")
print("=" * 70)

message_positif = "J'ai eu mon diplôme ! Je suis tellement heureux !"
print(f"\n📝 Message : \"{message_positif}\"\n")

print("🔗 LCEL :")
result_lcel_2 = chain_lcel.invoke({"message": message_positif})
print(f"{result_lcel_2}\n")

print("📊 LangGraph :")
print("   📊 Étapes du graphe :")
result_graph_2 = app.invoke({"message": message_positif})
print(f"\n{result_graph_2['response']}")


# ═══════════════════════════════════════════════════════════════════════════
# 📚 RÉCAPITULATIF
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📚 RÉCAPITULATIF")
print("=" * 70)
print("""
┌─────────────────────────────────────────────────────────────────────┐
│  LCEL (Chains)                  │  LangGraph                        │
├─────────────────────────────────┼───────────────────────────────────┤
│  prompt | llm | parser          │  StateGraph + add_node + add_edge │
│  Flux linéaire uniquement       │  Conditions et boucles possibles  │
│  1 appel LLM (tout en un)       │  Plusieurs appels (étape par      │
│                                 │  étape)                           │
│  Plus concis                    │  Plus explicite                   │
│  Idéal pour pipelines simples   │  Idéal pour agents/workflows      │
└─────────────────────────────────┴───────────────────────────────────┘

🎯 Règle d'or : Commence avec LCEL, passe à LangGraph si tu as besoin
   de boucles, conditions, ou d'un contrôle fin sur le flux.
""")
