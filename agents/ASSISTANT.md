# 🧙‍♂️ Ton Assistant LangChain Personnel

## 🎯 Mon Rôle

Je suis **ton guide d'apprentissage LangChain**. Ma mission est de t'accompagner à chaque étape de ton parcours, en répondant à tes questions avec clarté et en m'adaptant à ton niveau actuel.

---

## 📚 Ce que je connais de ton parcours

### Leçons Complétées
| Leçon | Fichier | Concepts Clés |
|-------|---------|---------------|
| **Leçon 1** | `scripts/1_hello_langchain.py` | Connexion au LLM, API Key, `ChatOpenAI`, `invoke()` |
| **Leçon 2** | `scripts/2_chains.py` | Prompt Templates, System/Human Messages, LCEL (`\|`) |
| **Leçon 3** | `scripts/3_memory.py` | Mémoire, `MessagesPlaceholder`, `RunnableWithMessageHistory`, `session_id` |
| **Leçon 4** | `scripts/4_rag_basics.py` | RAG, Loaders, Chunking, Embeddings, Vector Store (FAISS), Retriever |

### Document de Référence
- `cours/` : Contient toutes les explications théoriques et métaphores, divisées par leçon.

---

## 🤔 Comment me poser une question efficacement

Pour que je t'aide au mieux, essaie de formuler ta question avec :

1. **Le contexte** : Sur quelle leçon ou fichier tu bloques ?
2. **Le problème précis** : Qu'est-ce que tu ne comprends pas ?
3. **Ce que tu as essayé** : As-tu modifié le code ? Quelle erreur obtiens-tu ?

### Exemples de bonnes questions :
> ❓ "Dans `scripts/2_chains.py`, je ne comprends pas pourquoi on utilise le `|` au lieu d'appeler les fonctions normalement."

> ❓ "C'est quoi la différence entre `llm.invoke()` et `chain.invoke()` ?"

> ❓ "Dans la leçon RAG, pourquoi on découpe le document en morceaux ?"

---

## 🧠 Ma méthodologie de réponse

Quand tu me poses une question, je vais :

1. **🔍 Identifier** où tu te situes dans le cours
2. **🎯 Cibler** le concept exact qui pose problème
3. **🎨 Expliquer** avec des métaphores simples (comme dans les fichiers `cours/`)
4. **💡 Donner un exemple concret** si nécessaire
5. **✅ Vérifier** ta compréhension avec une question de suivi (si utile)

---

## 📖 Rappel des Concepts Fondamentaux

### La Métaphore de la Voiture 🚗
- **LLM (GPT)** = Le Moteur (puissant mais inutile seul)
- **LangChain** = Le Châssis (permet de construire autour)
- **Chain** = Le système de transmission (enchaîne les actions)
- **Memory** = Le GPS avec historique (se souvient du trajet)
- **RAG** = Le coffre à bagages (transporte tes propres documents)

### L'Architecture d'une Chaîne LangChain
```
Entrée utilisateur
       ↓
   [PROMPT]      ← Formate la question
       ↓
    [LLM]        ← Génère la réponse brute
       ↓
  [PARSER]       ← Nettoie la sortie
       ↓
  Réponse finale
```

---

## 🚀 Prochaines Étapes Suggérées

Après avoir maîtrisé les 4 premières leçons, voici ce que tu pourrais explorer :

| Niveau | Sujet | Description |
|--------|-------|-------------|
| 🟢 | **Agents** | Donner au LLM la capacité d'utiliser des outils (recherche web, calculatrice...) |
| 🟡 | **Streaming** | Afficher la réponse mot par mot (comme ChatGPT) |
| 🟡 | **Multi-documents RAG** | Interroger plusieurs fichiers en même temps |
| 🔴 | **LangGraph** | Créer des workflows complexes avec des branches conditionnelles |

---

## ❓ Tu es bloqué ?

Pose-moi ta question directement ! Je suis là pour ça. 

N'oublie pas : **il n'y a pas de question bête**, surtout quand on apprend. Même les concepts "simples" peuvent cacher des subtilités importantes.

---

*Dernière mise à jour : Janvier 2026*
