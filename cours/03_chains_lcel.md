# 🔗 Leçon 3 : Les Chaînes (Chains) et LCEL

## 📖 Introduction

C'est le cœur de LangChain ! Une "Chain" est une **séquence d'actions** qui s'enchaînent automatiquement.

---

## 🎨 La Syntaxe LCEL (LangChain Expression Language)

LangChain utilise une syntaxe élégante avec le symbole pipe `|` (comme en Unix/PowerShell) pour enchaîner les composants.

```python
chain = prompt | llm | output_parser
```

> 💡 **Lecture** : "Prends l'entrée, passe-la au **Prompt**, envoie le résultat au **LLM**, puis nettoie la sortie avec le **Parser**."

C'est comme une chaîne de montage industrielle : chaque étape traite le produit et le passe à la suivante.

---

## 🧩 Les Composants de la Chaîne

### 1. Prompt
Formate la question de l'utilisateur selon le template défini.

**Entrée** : `{"question": "C'est quoi Python ?"}` → **Sortie** : Message formaté

### 2. LLM
Génère la réponse brute. Le modèle renvoie un objet `AIMessage` avec la réponse.

**Entrée** : Message formaté → **Sortie** : Objet AIMessage

### 3. Output Parser
Transforme l'objet Message en texte simple (string). C'est le "nettoyeur".

**Entrée** : Objet AIMessage → **Sortie** : String propre

---

## 💻 Exemple de Code

**Fichier** : `scripts/2_chains.py`

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert Python."),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

# Exécution de la chaîne
reponse = chain.invoke({"question": "Explique les dictionnaires"})
```

### Flux de données :
```
{"question": "Explique les dictionnaires"}
            ↓
    [PROMPT] → Message formaté
            ↓
     [LLM] → AIMessage(content="Les dictionnaires sont...")
            ↓
   [PARSER] → "Les dictionnaires sont..."
```

---

## ✅ Points à Retenir

- Une **Chain** est une séquence d'actions enchaînées avec `|`
- **LCEL** = LangChain Expression Language (syntaxe avec le pipe)
- Les 3 composants de base : **Prompt** → **LLM** → **Parser**
- `invoke()` exécute toute la chaîne d'un coup

---

## 🔜 Prochaine Leçon

Nos chaînes fonctionnent, mais elles "oublient" tout entre chaque message. Apprenons à leur donner de la **Mémoire** !
