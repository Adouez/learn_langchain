# 🧠 Leçon 4 : La Mémoire (Memory)

## 📖 Introduction

Par défaut, un LLM est "**stateless**" (sans état) : il oublie tout après chaque réponse. 

Pour créer un vrai Chatbot qui se souvient de la conversation, il faut **injecter l'historique** dans le Prompt à chaque tour.

---

## 🔄 Comment ça marche ?

Au lieu d'envoyer juste la question actuelle, on envoie :

```
[Historique des messages] + [Nouvelle Question]
```

> 💡 **Métaphore** : C'est comme un GPS avec historique. Au lieu de demander "Où aller ?", tu demandes "En partant de là où j'étais, où aller maintenant ?".

---

## 🧩 Composants Clés

### 1. `MessagesPlaceholder`
Une case vide dans le Prompt Template réservée pour insérer l'historique de conversation.

```python
MessagesPlaceholder(variable_name="history")
```

C'est comme réserver une place dans un formulaire pour "coller" l'historique plus tard.

### 2. `RunnableWithMessageHistory`
Un outil qui gère automatiquement :
- La sauvegarde des messages (ce que tu dis ET ce que le bot répond)
- La réinjection de l'historique au tour suivant

### 3. `session_id`
Un identifiant unique pour distinguer les conversations de différents utilisateurs.

> 💡 Alice et Bob peuvent parler au même bot sans mélanger leurs historiques grâce au `session_id`.

---

## 💻 Exemple de Code

**Fichier** : `scripts/3_memory.py`

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 1. Prompt avec emplacement pour l'historique
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant amical."),
    MessagesPlaceholder(variable_name="history"),  # <-- La mémoire
    ("human", "{question}")
])

# 2. Stockage de l'historique (en RAM ici)
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 3. Chaîne avec mémoire
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

# 4. Utilisation avec session_id
response = chain_with_history.invoke(
    {"question": "Je m'appelle Alice"},
    config={"configurable": {"session_id": "user_123"}}
)
```

---

## 📊 Flux de la Mémoire

```
Tour 1: "Je m'appelle Alice"
        ↓
[history: vide] + "Je m'appelle Alice" → Bot: "Bonjour Alice !"
        ↓
Sauvegarde: [Human: "Je m'appelle Alice", AI: "Bonjour Alice !"]

Tour 2: "Quel est mon nom ?"
        ↓
[history: Human+AI précédents] + "Quel est mon nom ?" → Bot: "Tu es Alice !"
```

---

## ✅ Points à Retenir

- Les LLMs sont **stateless** par défaut (sans mémoire)
- `MessagesPlaceholder` = L'emplacement réservé pour l'historique
- `RunnableWithMessageHistory` = Le gestionnaire automatique de mémoire
- `session_id` = Identifiant unique par utilisateur/conversation

---

## 🆕 Note : Évolution vers LangGraph (LangChain 1.x)

Depuis **LangChain 1.x**, une nouvelle approche est disponible via **LangGraph** :

| Approche | Outil | Cas d'usage |
|----------|-------|-------------|
| **Classique** | `RunnableWithMessageHistory` | Chaînes simples, facile à comprendre |
| **Moderne** | LangGraph + `MemorySaver` | Agents, workflows complexes, plus de contrôle |

### Avec LangGraph, la mémoire est gérée via un **état** :

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Le checkpointer sauvegarde l'état (dont les messages)
memory = MemorySaver()

agent = create_react_agent(llm, tools, checkpointer=memory)

# Le thread_id remplace le session_id
config = {"configurable": {"thread_id": "user_123"}}
result = agent.invoke({"messages": [...]}, config=config)
```

> 💡 **Conseil** : Commence par `RunnableWithMessageHistory` pour comprendre le concept, puis passe à LangGraph quand tu travailles avec des Agents.

📁 Voir le script `3bis_memory_langgraph.py` pour un exemple complet.

---

## 🔜 Prochaine Leçon

Notre bot a de la mémoire, mais il ne connaît que ce qu'il a appris pendant son entraînement. Comment lui faire lire VOS documents ? C'est le **RAG** !
