# 🎨 Leçon 8 : Interface Utilisateur avec Streamlit

## 🎯 Objectif

Jusqu'ici, nos scripts tournent dans le terminal. C'est bien pour apprendre, mais pour un **vrai projet**, il faut une interface graphique !

**Streamlit** est la solution parfaite :
- 🐍 100% Python (pas de HTML/CSS/JS)
- ⚡ Rechargement automatique
- 🎨 UI moderne et réactive
- 🤝 Parfait pour les projets IA/ML

---

## 🏗️ Architecture d'une App Streamlit

```
┌─────────────────────────────────────────────────────┐
│                    NAVIGATEUR                        │
│  ┌─────────────────────────────────────────────┐    │
│  │  💬 Chatbot LangChain                       │    │
│  │  ────────────────────────────────           │    │
│  │  🤖 Bonjour ! Comment puis-je t'aider ?     │    │
│  │  👤 Explique-moi le RAG                     │    │
│  │  🤖 Le RAG est une technique qui...         │    │
│  │  ────────────────────────────────           │    │
│  │  [____Tape ton message____] [Envoyer]       │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
           ↑↓ (communication temps réel)
┌─────────────────────────────────────────────────────┐
│              BACKEND (Python + LangChain)            │
│  - Gestion de la mémoire (session_state)            │
│  - Appels au LLM                                     │
│  - RAG si nécessaire                                 │
└─────────────────────────────────────────────────────┘
```

---

## 🧩 Composants Clés de Streamlit

### 1. `st.chat_message()` - Afficher un Message
```python
with st.chat_message("user"):      # Bulle utilisateur
    st.write("Bonjour !")

with st.chat_message("assistant"): # Bulle assistant
    st.write("Comment puis-je t'aider ?")
```

### 2. `st.chat_input()` - Zone de Saisie
```python
prompt = st.chat_input("Tape ton message...")
if prompt:
    # L'utilisateur a envoyé un message
    process(prompt)
```

### 3. `st.session_state` - Mémoire de Session
```python
# Initialiser l'historique (une seule fois)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ajouter un message
st.session_state.messages.append({"role": "user", "content": "..."})
```

> 💡 `session_state` est comme un dictionnaire qui **persiste** entre les rechargements de page.

### 4. `st.spinner()` - Indicateur de Chargement
```python
with st.spinner("Réflexion en cours..."):
    response = llm.invoke(...)  # Pendant ce temps, un spinner s'affiche
```

---

## 💻 Structure du Code (`7_app_streamlit.py`)

```python
import streamlit as st
from langchain_openai import ChatOpenAI

# 1. Configuration de la page
st.set_page_config(page_title="Mon Chatbot", page_icon="🤖")
st.title("🤖 Mon Chatbot LangChain")

# 2. Initialisation de la mémoire
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Afficher l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Zone de saisie
if prompt := st.chat_input("Pose ta question..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Générer et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            response = llm.invoke(st.session_state.messages)
        st.write(response.content)
    st.session_state.messages.append({"role": "assistant", "content": response.content})
```

---

## 🔄 Le Flux de l'Application

```
1. Utilisateur ouvre la page
   ↓
2. Streamlit initialise session_state (si vide)
   ↓
3. Affiche l'historique des messages
   ↓
4. Utilisateur tape un message
   ↓
5. Message ajouté à session_state + affiché
   ↓
6. LLM génère une réponse (avec spinner)
   ↓
7. Réponse ajoutée à session_state + affichée
   ↓
8. Retour à l'étape 4 (boucle)
```

---

## 🎨 Personnalisation

### Thème et Style
```python
st.set_page_config(
    page_title="Assistant Poudlard",
    page_icon="🧙",
    layout="wide",  # ou "centered"
    initial_sidebar_state="expanded"
)
```

### Sidebar (Menu Latéral)
```python
with st.sidebar:
    st.header("⚙️ Paramètres")
    temperature = st.slider("Créativité", 0.0, 1.0, 0.7)
    model = st.selectbox("Modèle", ["gpt-3.5-turbo", "gpt-4"])
```

### Boutons et Actions
```python
if st.button("🗑️ Effacer la conversation"):
    st.session_state.messages = []
    st.rerun()  # Recharge la page
```

---

## 🚀 Lancer l'Application

```bash
# Installation (si pas déjà fait)
pip install streamlit

# Lancement
streamlit run scripts/7_app_streamlit.py
```

L'app s'ouvre automatiquement dans ton navigateur à `http://localhost:8501`

---

## ⚠️ Points d'Attention

1. **Rechargement** : Streamlit recharge le script à chaque interaction → utilise `session_state` pour persister
2. **Variables d'environnement** : Le `.env` fonctionne avec `load_dotenv()` comme d'habitude
3. **Performance** : Initialise le LLM une seule fois avec `@st.cache_resource`
4. **Streaming** : Pour un effet "machine à écrire", utilise `st.write_stream()`

---

## 🧪 Exercices Suggérés

1. **Basique** : Faire fonctionner le chatbot simple
2. **Intermédiaire** : Ajouter un sélecteur de modèle dans la sidebar
3. **Avancé** : Intégrer le RAG Poudlard pour répondre aux questions sur le règlement

---

## ✅ Points à Retenir

- `st.chat_message()` + `st.chat_input()` = Interface de chat complète
- `st.session_state` = Mémoire entre les interactions (CRUCIAL)
- `st.spinner()` = Feedback visuel pendant le chargement
- `streamlit run fichier.py` = Lancer l'application
- **Pas besoin de HTML/CSS** : Tout est en Python !

---

## 🔜 Et Après ?

Félicitations ! 🎉 Tu as maintenant toutes les briques pour créer des applications LLM complètes :
- ✅ Chaînes et Prompts
- ✅ Mémoire
- ✅ RAG
- ✅ Agents
- ✅ Interface graphique

**Prochaine étape** : Créer TON propre projet ! 🚀
