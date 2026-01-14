# 🎓 Leçon 1 : Les Fondations

## 📖 Introduction

LangChain est un framework qui permet de connecter des modèles de langage (LLMs) à d'autres sources de données et d'outils.

> 💡 **Métaphore** : Si GPT-4 est le **moteur**, LangChain est le **châssis** qui permet de construire une voiture autour.

---

## 🧠 Concepts Clés

### LLM (Large Language Model)
Le "cerveau" de notre application. Exemples : GPT-3.5, GPT-4, Claude, etc.

C'est le modèle qui comprend le langage naturel et génère des réponses.

### API Key
Le pass d'accès pour utiliser le cerveau. Sans cette clé, impossible de communiquer avec le modèle.

> ⚠️ **Important** : Ne jamais partager sa clé API publiquement ! Toujours la stocker dans un fichier `.env`.

---

## 💻 Exemple de Code

**Fichier** : `scripts/1_hello_langchain.py`

Une connexion simple pour poser une question brute au modèle :

```python
from langchain_openai import ChatOpenAI

# Initialiser le modèle
llm = ChatOpenAI(api_key="...", model="gpt-3.5-turbo")

# Poser une question
response = llm.invoke("Bonjour !")
```

### Explications :
1. **`ChatOpenAI`** : La classe qui permet de se connecter à l'API OpenAI
2. **`model`** : Le modèle à utiliser (gpt-3.5-turbo est rapide et économique)
3. **`invoke()`** : La méthode pour envoyer un message et recevoir une réponse

---

## ✅ Points à Retenir

- LangChain est un **framework** pour construire des applications LLM
- Le LLM est le **moteur**, LangChain est le **châssis**
- Toujours protéger sa clé API avec un fichier `.env`
- `invoke()` est la méthode de base pour communiquer avec le modèle

---

## 🔜 Prochaine Leçon

Maintenant que tu sais te connecter au modèle, apprenons à lui parler de manière structurée avec les **Prompt Templates** !
