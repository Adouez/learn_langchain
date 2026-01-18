"""
🧠 Leçon 4 BIS : La Mémoire avec LangGraph (Approche Moderne)
=============================================================

Ce script montre l'approche MODERNE de la gestion de la mémoire
avec LangGraph, introduite dans LangChain 1.x.

Différences avec l'approche classique (3_memory.py) :
- Pas besoin de RunnableWithMessageHistory
- La mémoire est gérée via un "checkpointer" (MemorySaver)
- On utilise thread_id au lieu de session_id
- Plus adapté pour les Agents et workflows complexes
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════
# 🧠 PARTIE 1 : CONFIGURATION DU MODÈLE
# ═══════════════════════════════════════════════════════════════════════════

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Message système pour personnaliser le comportement
SYSTEM_MESSAGE = """Tu es un assistant amical qui se souvient des détails de la conversation.
Tu fais attention aux noms, préférences et informations partagées par l'utilisateur."""


# ═══════════════════════════════════════════════════════════════════════════
# 📊 PARTIE 2 : CRÉATION DU GRAPHE AVEC ÉTAT
# ═══════════════════════════════════════════════════════════════════════════

# MessagesState est un état pré-défini qui contient une liste de messages
# C'est LangGraph qui gère automatiquement l'ajout des nouveaux messages

def call_model(state: MessagesState):
    """
    Fonction appelée à chaque tour de conversation.
    Elle reçoit l'état actuel (avec l'historique) et retourne la réponse.
    """
    # On ajoute le message système au début de la conversation
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}] + state["messages"]
    
    # Le LLM reçoit TOUT l'historique à chaque appel
    response = llm.invoke(messages)
    
    # On retourne la réponse (LangGraph l'ajoute automatiquement à l'état)
    return {"messages": [response]}


# Création du graphe (workflow)
# C'est comme un diagramme : START -> model -> END
workflow = StateGraph(state_schema=MessagesState)

# On ajoute le nœud "model" qui appelle notre fonction
workflow.add_node("model", call_model)

# On connecte : Début -> model (puis fin automatique)
workflow.add_edge(START, "model")


# ═══════════════════════════════════════════════════════════════════════════
# 💾 PARTIE 3 : LA MÉMOIRE (CHECKPOINTER)
# ═══════════════════════════════════════════════════════════════════════════

# MemorySaver sauvegarde l'état en mémoire RAM
# Pour une vraie app, on utiliserait SqliteSaver ou PostgresSaver
memory = MemorySaver()

# On compile le graphe avec le checkpointer
# C'est comme "activer" la sauvegarde automatique
app = workflow.compile(checkpointer=memory)


# ═══════════════════════════════════════════════════════════════════════════
# 🚀 PARTIE 4 : TESTS DE LA MÉMOIRE
# ═══════════════════════════════════════════════════════════════════════════

def chat(message: str, thread_id: str) -> str:
    """
    Envoie un message et retourne la réponse.
    Le thread_id identifie la conversation (comme session_id avant).
    """
    # Configuration avec l'identifiant de conversation
    config = {"configurable": {"thread_id": thread_id}}
    
    # On envoie le message (LangGraph gère l'historique automatiquement)
    result = app.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config
    )
    
    # La réponse est le dernier message
    return result["messages"][-1].content


# === Test avec l'utilisateur "alice" ===
print("=" * 60)
print("🧪 TEST : Conversation avec Alice")
print("=" * 60)

print("\n--- Échange 1 ---")
response1 = chat("Bonjour ! Je m'appelle Alice et j'adore le chocolat.", thread_id="alice")
print(f"👤 Alice: Bonjour ! Je m'appelle Alice et j'adore le chocolat.")
print(f"🤖 Bot: {response1}")

print("\n--- Échange 2 ---")
response2 = chat("Quel est mon nom et qu'est-ce que j'aime ?", thread_id="alice")
print(f"👤 Alice: Quel est mon nom et qu'est-ce que j'aime ?")
print(f"🤖 Bot: {response2}")


# === Test avec un autre utilisateur "bob" (thread différent) ===
print("\n" + "=" * 60)
print("🧪 TEST : Conversation avec Bob (thread séparé)")
print("=" * 60)

print("\n--- Échange 1 ---")
response3 = chat("Salut ! Moi c'est Bob.", thread_id="bob")
print(f"👤 Bob: Salut ! Moi c'est Bob.")
print(f"🤖 Bot: {response3}")

print("\n--- Échange 2 ---")
response4 = chat("Tu connais Alice ?", thread_id="bob")
print(f"👤 Bob: Tu connais Alice ?")
print(f"🤖 Bot: {response4}")


# === Retour sur Alice (la mémoire est préservée !) ===
print("\n" + "=" * 60)
print("🧪 TEST : Retour sur Alice (mémoire préservée)")
print("=" * 60)

print("\n--- Échange 3 ---")
response5 = chat("Tu te souviens de ce que j'aime ?", thread_id="alice")
print(f"👤 Alice: Tu te souviens de ce que j'aime ?")
print(f"🤖 Bot: {response5}")


print("\n" + "=" * 60)
print("🎉 FIN DES TESTS")
print("=" * 60)
print("""
📚 Ce que tu as appris avec LangGraph :
   - MemorySaver = Sauvegarde automatique de l'état
   - thread_id = Identifiant de conversation (remplace session_id)
   - StateGraph = Définit le workflow de l'application
   - MessagesState = État pré-défini contenant les messages
   
💡 Avantages de LangGraph :
   - Plus de contrôle sur le flux
   - Même système pour chaînes simples ET agents
   - Checkpointers pour différents backends (RAM, SQLite, PostgreSQL...)
""")
