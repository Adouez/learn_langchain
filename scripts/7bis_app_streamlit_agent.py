"""
🤖 Leçon 8bis : Streamlit + Agent LangGraph avec Tools Modulaires
=================================================================

Cette version utilise :
- Streamlit pour l'interface
- LangGraph pour l'agent
- MemorySaver pour la mémoire
- Les TOOLS du package tools/ (RAG Cegedim, calculatrice, etc.)

Pour lancer : streamlit run scripts/7bis_app_streamlit_agent.py
"""

import sys
import os

# Ajouter le dossier scripts au path pour importer le package tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import streamlit as st
import uuid
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# ═══════════════════════════════════════════════════════════════════════════
# 📦 IMPORT DES TOOLS DEPUIS LE PACKAGE tools/
# ═══════════════════════════════════════════════════════════════════════════

from tools import (
    recherche_reglements_cegedim,  # 🔍 RAG Cegedim
    calculatrice,                   # 🧮 Calculs
    date_actuelle,                  # 📅 Date/Heure
    # recherche_web,                # 🌐 Web (optionnel - nécessite duckduckgo-search)
    # envoyer_email,                # 📧 Email (optionnel)
    # generer_graphique,            # 📊 Graphiques (optionnel - nécessite matplotlib)
)

load_dotenv()

# Liste des outils actifs (tu peux en ajouter/retirer facilement !)
TOOLS_ACTIFS = [
    recherche_reglements_cegedim,
    calculatrice,
    date_actuelle,
]

# ═══════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION DE LA PAGE
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Agent Cegedim",
    page_icon="🏢",
    layout="centered"
)

# ═══════════════════════════════════════════════════════════════════════════
# 🧠 CRÉATION DE L'AGENT AVEC MÉMOIRE
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_resource
def create_agent():
    """Crée l'agent avec sa mémoire (cached = créé une seule fois)."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    memory = MemorySaver()
    
    system_prompt = """Tu es un assistant intelligent spécialisé dans les procédures Cegedim.

🛠️ Tes outils :
1. **recherche_reglements_cegedim** : Pour chercher dans les règlements et procédures internes
2. **calculatrice** : Pour faire des calculs
3. **date_actuelle** : Pour connaître la date/heure

📋 Règles :
- Utilise TOUJOURS l'outil de recherche pour les questions sur Cegedim, Pegase, Spayr, contrats
- Cite tes sources quand tu trouves des informations
- Réponds de manière claire et structurée en français
- Si tu ne trouves pas l'info, dis-le clairement"""
    
    agent = create_react_agent(
        llm,
        TOOLS_ACTIFS,
        prompt=system_prompt,
        checkpointer=memory
    )
    
    return agent

agent = create_agent()

# ═══════════════════════════════════════════════════════════════════════════
# 🔑 GESTION DU THREAD_ID
# ═══════════════════════════════════════════════════════════════════════════

# On stocke le thread_id dans session_state (persist entre les reloads)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]

# On stocke aussi l'historique pour l'AFFICHAGE (pas pour la mémoire LLM)
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.header("🏢 Agent Cegedim")
    
    st.info(f"🔑 Session : `{st.session_state.thread_id}`")
    
    st.divider()
    
    st.subheader("🛠️ Outils actifs")
    for tool in TOOLS_ACTIFS:
        st.write(f"- {tool.name}")
    
    st.divider()
    
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.session_state.display_messages = []
        st.rerun()
    
    st.divider()
    
    st.caption("📚 Sources : DocARag3/")
    st.caption("🧠 Mémoire : LangGraph MemorySaver")

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 INTERFACE PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════

st.title("🏢 Assistant Règlements Cegedim")
st.caption("Pose tes questions sur les procédures Pegase, Spayr, contrats...")

# Afficher l'historique
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Message d'accueil
if not st.session_state.display_messages:
    with st.chat_message("assistant"):
        st.markdown("""👋 Bonjour ! Je suis l'assistant Cegedim.

Je peux t'aider avec :
- 📋 Les règles de contrats (CDI, CDD)
- 💻 Les procédures Pegase
- 💰 Les règles Spayr et acomptes
- 🧮 Des calculs

Pose-moi ta question !""")

# ═══════════════════════════════════════════════════════════════════════════
# 💬 GESTION DU CHAT
# ═══════════════════════════════════════════════════════════════════════════

if prompt := st.chat_input("Tape ta question..."):
    
    # 1. Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.display_messages.append({"role": "user", "content": prompt})
    
    # 2. Appeler l'agent
    with st.chat_message("assistant"):
        with st.spinner("🤔 Recherche dans les règlements..."):
            
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            
            result = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                config=config
            )
            
            response_content = result["messages"][-1].content
        
        st.markdown(response_content)
    
    # 3. Sauvegarder pour l'affichage
    st.session_state.display_messages.append({"role": "assistant", "content": response_content})

# ═══════════════════════════════════════════════════════════════════════════
# 📊 FOOTER
# ═══════════════════════════════════════════════════════════════════════════

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"🔑 Session : {st.session_state.thread_id}")
with col2:
    st.caption(f"💬 Messages : {len(st.session_state.display_messages)}")
with col3:
    st.caption(f"🛠️ Tools : {len(TOOLS_ACTIFS)}")
