"""
🤖 Leçon 6bis : Agent avec RAG sur documents PDF
=================================================

Cet agent combine plusieurs outils :
1. 🔍 RAG - Interroge les rapports de maturité Clinitex
2. 🧮 Calculatrice - Fait des calculs mathématiques
3. 📅 Date - Donne la date actuelle
4. 🌐 Recherche Web - Cherche sur Internet (DuckDuckGo)
5. 📧 Email - Envoie des emails (mode simulation)
6. 📊 Graphiques - Génère des visualisations

L'agent décide SEUL quel outil utiliser selon ta question !

Les outils sont définis dans le dossier tools/ pour plus de lisibilité.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver  # 🧠 Pour la mémoire !

# ═══════════════════════════════════════════════════════════════════════════
# 📦 IMPORT DES OUTILS DEPUIS LE PACKAGE tools/
# ═══════════════════════════════════════════════════════════════════════════

from tools import (
    recherche_rapports_clinitex,
    calculatrice,
    date_actuelle,
    recherche_web,
    envoyer_email,
    generer_graphique,
    tous_les_outils  # Liste pratique de tous les outils
)

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════
# 🧠 MÉMOIRE - Sauvegarde l'historique des conversations
# ═══════════════════════════════════════════════════════════════════════════

memory = MemorySaver()

# ═══════════════════════════════════════════════════════════════════════════
# 🧠 CRÉATION DE L'AGENT
# ═══════════════════════════════════════════════════════════════════════════

print("🤖 Création de l'agent avec 6 outils...")

# Le cerveau de l'agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Instructions système
system_message = """Tu es un assistant expert en analyse de maturité digitale.

📚 **Rapports disponibles** (Clinitex) :
- Antoine Douez
- Nicolas Isnardy
- Sacha Dbusschere  
- Stéphane Beuve

🛠️ **Tes outils** :
1. **recherche_rapports_clinitex** : Chercher des infos dans les rapports de maturité
2. **calculatrice** : Faire des calculs (moyennes, différences, pourcentages)
3. **date_actuelle** : Connaître la date et l'heure actuelles
4. **recherche_web** : Chercher des informations sur Internet
5. **envoyer_email** : Envoyer un email (mode simulation par défaut)
6. **generer_graphique** : Créer des graphiques (barres, camembert, ligne)

📋 **Règles** :
- Utilise TOUJOURS l'outil de recherche pour répondre aux questions sur les rapports
- Cite tes sources quand tu donnes des informations
- Si tu fais des calculs, montre le détail
- Pour les graphiques, utilise le format JSON : {"labels": [...], "valeurs": [...]}
- Réponds en français de manière claire et structurée"""

# Créer l'agent ReAct avec TOUS les outils + MÉMOIRE
agent = create_react_agent(
    llm,
    tous_les_outils,  # Tous les outils du package tools/
    prompt=system_message,
    checkpointer=memory  # 🧠 Active la mémoire !
)


# ═══════════════════════════════════════════════════════════════════════════
# 🚀 FONCTION D'EXÉCUTION
# ═══════════════════════════════════════════════════════════════════════════

def poser_question(question: str, thread_id: str = "default") -> str:
    """Pose une question à l'agent et retourne la réponse.
    
    Args:
        question: La question à poser
        thread_id: Identifiant de la conversation (pour la mémoire)
    """
    print(f"\n❓ Question : {question}")
    print("🔄 L'agent réfléchit...")
    
    messages = [{"role": "user", "content": question}]
    
    # 🧠 On passe le thread_id pour que l'agent se souvienne de la conversation
    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke({"messages": messages}, config=config)
    
    reponse = result["messages"][-1].content
    print(f"\n✅ Réponse :\n{reponse}")
    print("-" * 60)
    return reponse


# ═══════════════════════════════════════════════════════════════════════════
# 🧪 TESTS
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTS DE L'AGENT MULTI-OUTILS (avec mémoire)")
    print("=" * 60)
    
    # On utilise un thread_id unique pour les tests
    TEST_THREAD = "test_session"
    
    # Test 1 : RAG - Question sur les rapports
    poser_question("Quels sont les principaux points forts identifiés dans le rapport d'Antoine ?", TEST_THREAD)
    
    # Test 2 : Calculatrice
    poser_question("Calcule la moyenne de 85, 78, 92 et 70.", TEST_THREAD)
    
    # Test 3 : Test de la MÉMOIRE ! 🧠
    poser_question("Quel était le résultat du calcul précédent ?", TEST_THREAD)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 💬 MODE INTERACTIF (avec mémoire)
    # ═══════════════════════════════════════════════════════════════════════
    
    print("\n" + "=" * 60)
    print("💬 MODE INTERACTIF (avec mémoire 🧠)")
    print("Pose tes questions ! L'agent se souvient de la conversation.")
    print("Tape 'quit' pour quitter, 'reset' pour nouvelle conversation.")
    print("=" * 60)
    
    # Thread ID pour le mode interactif (différent des tests)
    session_id = "user_session"
    
    while True:
        question = input("\n🎤 Ta question : ").strip()
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 À bientôt !")
            break
        if question.lower() == 'reset':
            # Nouvelle session = nouvelle mémoire
            import uuid
            session_id = str(uuid.uuid4())[:8]
            print(f"🔄 Nouvelle conversation démarrée (session: {session_id})")
            continue
        if question:
            poser_question(question, session_id)
