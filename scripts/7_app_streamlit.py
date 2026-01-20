"""
🎨 Leçon 8 : Application Chatbot avec Streamlit
===============================================

Une interface graphique complète pour ton chatbot LangChain !

Pour lancer : streamlit run scripts/7_app_streamlit.py
"""

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURATION DE LA PAGE
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Chatbot LangChain",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 SIDEBAR - PARAMÈTRES
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Sélection du modèle
    model_name = st.selectbox(
        "🧠 Modèle",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0
    )
    
    # Slider pour la température (créativité)
    temperature = st.slider(
        "🎨 Créativité",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="0 = Réponses précises, 1 = Réponses créatives"
    )
    
    # Personnalité du bot
    personality = st.text_area(
        "🎭 Personnalité du bot",
        value="Tu es un assistant amical et pédagogue. Tu expliques les concepts de manière simple avec des exemples concrets.",
        height=100
    )
    
    st.divider()
    
    # Bouton pour effacer la conversation
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Infos
    st.caption("🎓 Projet Learn LangChain")
    st.caption(f"📊 Messages : {len(st.session_state.get('messages', []))}")


# ═══════════════════════════════════════════════════════════════════════════
# 🧠 INITIALISATION DU MODÈLE
# ═══════════════════════════════════════════════════════════════════════════

# @st.cache_resource permet de ne créer le LLM qu'une seule fois
# (optimisation importante !)
@st.cache_resource
def get_llm(model: str, temp: float):
    """Crée et cache l'instance du LLM."""
    return ChatOpenAI(model=model, temperature=temp)


# On recrée le LLM si les paramètres changent
llm = get_llm(model_name, temperature)


# ═══════════════════════════════════════════════════════════════════════════
# 💾 MÉMOIRE DE SESSION
# ═══════════════════════════════════════════════════════════════════════════

# Initialiser l'historique des messages (une seule fois)
if "messages" not in st.session_state:
    st.session_state.messages = []


# ═══════════════════════════════════════════════════════════════════════════
# 🎨 INTERFACE PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════

# Titre
st.title("🤖 Chatbot LangChain")
st.caption("Ton assistant IA propulsé par LangChain et OpenAI")

# Afficher l'historique des messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    with st.chat_message(role):
        st.markdown(content)

# Message d'accueil si conversation vide
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("👋 Bonjour ! Je suis ton assistant. Pose-moi une question !")


# ═══════════════════════════════════════════════════════════════════════════
# 💬 GESTION DU CHAT
# ═══════════════════════════════════════════════════════════════════════════

# Zone de saisie
if prompt := st.chat_input("Tape ton message ici..."):
    
    # 1. Afficher le message de l'utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Sauvegarder dans l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 3. Préparer les messages pour le LLM (avec la personnalité)
    messages_for_llm = [SystemMessage(content=personality)]
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            messages_for_llm.append(HumanMessage(content=msg["content"]))
        else:
            messages_for_llm.append(AIMessage(content=msg["content"]))
    
    # 4. Générer la réponse
    with st.chat_message("assistant"):
        with st.spinner("🤔 Réflexion en cours..."):
            response = llm.invoke(messages_for_llm)
            response_content = response.content
        
        # Afficher la réponse
        st.markdown(response_content)
    
    # 5. Sauvegarder la réponse dans l'historique
    st.session_state.messages.append({"role": "assistant", "content": response_content})


# ═══════════════════════════════════════════════════════════════════════════
# 📊 FOOTER
# ═══════════════════════════════════════════════════════════════════════════

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"🧠 Modèle : {model_name}")
with col2:
    st.caption(f"🎨 Température : {temperature}")
with col3:
    st.caption(f"💬 Messages : {len(st.session_state.messages)}")
