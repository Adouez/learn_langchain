"""
🤖 Leçon 6 : Les Agents LangChain
=================================

Dans ce script, nous allons créer un Agent qui peut :
1. Faire des calculs mathématiques
2. Répondre à des questions sur Poudlard (en utilisant notre RAG !)

L'agent DÉCIDE lui-même quel outil utiliser selon la question.
C'est la grande différence avec une chaîne classique !

Exécute ce script et observe le raisonnement de l'agent avec verbose=True.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════
# 🛠️ PARTIE 1 : CRÉATION DES OUTILS
# ═══════════════════════════════════════════════════════════════════════════

# --- OUTIL 1 : La Calculatrice ---
# Un outil simple qui évalue des expressions mathématiques.
# ATTENTION : eval() est dangereux en production ! C'est juste pour l'exemple.

@tool
def calculatrice(expression: str) -> str:
    """Utile pour faire des calculs mathématiques. Entrée : une expression mathématique comme '2 + 2' ou '(15 * 3) / 5' ou '144 ** 0.5'"""
    try:
        # On nettoie l'expression et on calcule
        resultat = eval(expression)
        return f"Le résultat de {expression} est : {resultat}"
    except Exception as e:
        return f"Erreur de calcul : {e}"


# --- OUTIL 2 : Le Règlement de Poudlard (Mini-RAG) ---
# On réutilise notre RAG de la leçon 5 comme un outil !

# Variables globales pour le retriever (initialisées plus tard)
_retriever = None

def _init_retriever():
    """Initialise le retriever une seule fois."""
    global _retriever
    if _retriever is None:
        loader = TextLoader("scripts/DocARag/reglement_poudlard.txt", encoding="utf-8")
        documents = loader.load()
        
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    return _retriever

@tool
def reglement_poudlard(question: str) -> str:
    """Utile pour trouver des informations sur les règles de Poudlard, les horaires, les animaux autorisés, le couvre-feu, etc. Entrée : une question sur le règlement."""
    retriever = _init_retriever()
    docs = retriever.invoke(question)
    if docs:
        contexte = "\n".join([doc.page_content for doc in docs])
        return f"Voici ce que dit le règlement :\n{contexte}"
    return "Aucune information trouvée dans le règlement."


# ═══════════════════════════════════════════════════════════════════════════
# 🧠 PARTIE 2 : CRÉATION DE L'AGENT
# ═══════════════════════════════════════════════════════════════════════════

print("🔧 Initialisation des outils...")

# Définir la liste des outils
# ⚠️ LA DESCRIPTION (docstring) EST CRUCIALE : c'est ce que le LLM lit pour choisir l'outil !
tools = [calculatrice, reglement_poudlard]

# Le modèle LLM qui va "réfléchir"
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Message système pour guider l'agent
system_message = """Tu es un assistant intelligent de Poudlard.
Tu peux utiliser les outils à ta disposition pour :
- Faire des calculs mathématiques avec la calculatrice
- Chercher des informations dans le règlement de Poudlard

Réfléchis étape par étape avant de répondre."""

# Créer l'agent ReAct avec LangGraph
# LangGraph gère automatiquement la boucle de raisonnement
agent = create_react_agent(
    llm, 
    tools,
    prompt=system_message
)

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 PARTIE 3 : TESTS DE L'AGENT
# ═══════════════════════════════════════════════════════════════════════════

def executer_agent(question: str) -> str:
    """Exécute l'agent et retourne la réponse finale."""
    messages = [{"role": "user", "content": question}]
    result = agent.invoke({"messages": messages})
    # La dernière réponse de l'agent
    return result["messages"][-1].content

print("\n" + "="*60)
print("🧪 TEST 1 : Question de calcul")
print("="*60)

question1 = "Combien font 15 élèves fois 3 chocogrenouilles chacun, divisé par 5 maisons ?"
print(f"❓ Question : {question1}\n")
reponse1 = executer_agent(question1)
print(f"\n✅ Réponse finale : {reponse1}")

print("\n" + "="*60)
print("🧪 TEST 2 : Question sur le règlement")
print("="*60)

question2 = "Est-ce que je peux avoir un hibou dans ma chambre à Poudlard ?"
print(f"❓ Question : {question2}\n")
reponse2 = executer_agent(question2)
print(f"\n✅ Réponse finale : {reponse2}")

print("\n" + "="*60)
print("🧪 TEST 3 : Question mixte (calcul + règlement)")
print("="*60)

question3 = "Si le couvre-feu est à 21h et qu'il me faut 15 minutes pour rentrer, à quelle heure dois-je partir au plus tard ?"
print(f"❓ Question : {question3}\n")
reponse3 = executer_agent(question3)
print(f"\n✅ Réponse finale : {reponse3}")

print("\n" + "="*60)
print("🎉 FIN DES TESTS")
print("="*60)
print("""
📚 Ce que tu as appris :
   - L'agent DÉCIDE quel outil utiliser selon la question
   - Le cycle ReAct : Pensée → Action → Observation → ...
   - LangGraph gère maintenant les agents (depuis LangChain 1.x)
   - La description des outils (docstring) guide les décisions
""")
