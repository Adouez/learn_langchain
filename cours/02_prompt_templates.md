# 🧩 Leçon 2 : Structure et Prompt Templates

## 📖 Introduction

Les LLMs sont sensibles à la façon dont on leur parle. Pour obtenir de bons résultats de manière constante, on ne pose pas des questions brutes, on utilise des **Prompt Templates**.

---

## 🎯 Pourquoi utiliser des Templates ?

### 1. Réutilisabilité
On crée un "moule" et on change juste les variables. Plus besoin de réécrire le prompt à chaque fois !

### 2. Contextualisation
On peut donner un "Rôle" au modèle (System Message) pour qu'il agisse comme un expert dans un domaine précis.

---

## 🧠 Concepts Clés

### System Message
Instruction cachée qui définit le **comportement** du bot.

```python
("system", "Tu es un expert en cuisine française...")
```

> 💡 Le System Message est comme le "costume" que tu fais porter au modèle. Un costume de chef = réponses culinaires !

### Human Message
La question de l'utilisateur. C'est ce que tu (ou ton utilisateur) envoie au bot.

```python
("human", "Comment faire une quiche lorraine ?")
```

### Variable (`{question}`)
La partie dynamique du template. Elle sera remplacée par la vraie valeur au moment de l'exécution.

```python
("human", "{question}")  # {question} sera remplacé dynamiquement
```

---

## 💻 Exemple de Code

**Fichier** : `scripts/2_chains.py`

```python
from langchain_core.prompts import ChatPromptTemplate

# Créer le template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert technique en Python."),
    ("human", "{question}")
])

# Utiliser le template
formatted_prompt = prompt.format(question="C'est quoi une liste ?")
```

---

## ✅ Points à Retenir

- Les **Prompt Templates** permettent de structurer les messages
- **System Message** = Le rôle/comportement du bot
- **Human Message** = La question de l'utilisateur
- Les **variables** (`{...}`) rendent le template dynamique et réutilisable

---

## 🔜 Prochaine Leçon

Maintenant que tu sais créer des prompts structurés, apprenons à les **enchaîner** avec d'autres composants grâce aux **Chains** !
