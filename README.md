# Apprendre LangChain avec Cursor 🦜🔗 + 🤖

Bienvenue dans ce dépôt d'apprentissage !

Ce projet est le fruit d'une méthode d'apprentissage moderne : **le VibeLearning**.
Il documente mon parcours pour maîtriser **LangChain**, le framework de référence pour développer des applications basées sur les LLM, guidé étape par étape par l'assistant IA de l'éditeur **Cursor**.

## 💡 Le Concept : Apprendre via Cursor

L'idée n'est pas simplement de copier-coller du code, mais de construire une compréhension solide par le dialogue avec l'IA :

1.  **Exploration interactive** : Je pose des questions conceptuelles ("Comment donner de la mémoire au bot ?").
2.  **Codage assisté** : L'IA propose une structure de code que nous affinons ensemble.
3.  **Documentation en temps réel** : Chaque concept appris est noté dans le dossier `cours/` pour ancrer les connaissances.
4.  **Progression itérative** : On part d'un script simple pour arriver à des architectures complexes (RAG, Agents).

C'est une façon d'apprendre plus rapide, plus pratique et totalement personnalisée.

---

## 🚀 Comment Utiliser ce Projet (Recommandation)

Ce dépôt est conçu comme un **template d'apprentissage**. Pour vivre l'expérience complète du VibeLearning, voici la démarche recommandée :

### 1. Cloner et nettoyer

```bash
git clone https://github.com/Adouez/learn_langchain.git
cd learn_langchain
```

**🧹 Supprimez les contenus générés** pour repartir de zéro :
- Supprimez le contenu des fichiers dans `cours/` (gardez les fichiers vides ou supprimez-les)
- Supprimez les scripts dans `scripts/` (sauf le dossier `DocARag/` si vous voulez garder les documents d'exemple)
- Supprimez le dossier `controles/`

### 2. Configurer l'environnement

```bash
pip install -r requirements.txt
```

Créez un fichier `.env` à la racine et ajoutez votre clé API :
```env
OPENAI_API_KEY=sk-...
```

### 3. Lancer votre apprentissage

Ouvrez le projet dans **Cursor** et commencez à dialoguer avec l'agent **PROFESSOR** :

> "Salut Professeur ! Je suis prêt à apprendre LangChain. On commence par quoi ?"

Le professeur va créer les cours et exercices adaptés à votre rythme, dans les dossiers `cours/` et `scripts/`.

---

## ⚠️ Note Importante : Compatibilité LangChain

LangChain évolue rapidement et son API change fréquemment entre les versions. Les scripts Python présents dans ce dépôt ont été générés à un instant T et **peuvent nécessiter des corrections** pour fonctionner avec les dernières versions de LangChain.

**Conseil** : Si vous rencontrez des erreurs, demandez à votre agent Cursor (avec un modèle récent et à jour) de corriger le code pour qu'il soit compatible avec votre version de LangChain installée.

---

## 📂 Structure du Projet

```
learn-langchain/
├── 📁 agents/                     # Rôles des agents IA (à conserver !)
│   ├── PROFESSOR.md              # Le professeur pédagogue
│   ├── ASSISTANT.md              # L'assistant personnel
│   └── CONTROLEUR.md             # Le contrôleur de connaissances
│
├── 📁 cours/                      # Leçons théoriques (générées par le Professeur)
│   ├── 00_introduction.md
│   ├── 01_fondations.md
│   ├── 02_prompt_templates.md
│   ├── 03_chains_lcel.md
│   ├── 04_memory.md
│   ├── 05_rag.md
│   └── 06_agents.md
│
├── 📁 scripts/                    # Exercices pratiques Python (générés)
│   ├── 1_hello_langchain.py
│   ├── 2_chains.py
│   ├── 3_memory.py
│   ├── 4_rag_basics.py
│   ├── 5_agents.py
│   └── DocARag/                  # Documents pour les exercices RAG
│       └── reglement_poudlard.txt
│
├── 📁 controles/                  # Quiz et évaluations (générés par le Contrôleur)
│   └── controle_cours_0_5.md
│
├── README.md
├── requirements.txt
└── .env                          # Votre clé API (à créer, non versionné)
```

---

## 🤖 Les Agents IA

Ce projet utilise trois "rôles" d'IA pour enrichir l'apprentissage. **Conservez le dossier `agents/`** car il définit le comportement de vos assistants :

| Agent | Rôle | Quand l'utiliser |
|-------|------|------------------|
| 🎓 **PROFESSOR** | Enseigne et crée les cours/exercices | Pour apprendre un nouveau concept |
| 🧙‍♂️ **ASSISTANT** | Répond aux questions et guide | Pour de l'aide ponctuelle |
| 📋 **CONTROLEUR** | Vérifie la compréhension avec des quiz | Pour tester vos connaissances |

---

## 📚 Parcours Suggéré

Une fois lancé avec le Professeur, voici la progression typique :

| Étape | Concept | Ce que vous apprendrez |
|-------|---------|------------------------|
| 1 | **Fondations** | Connexion au LLM, API Key, premier appel |
| 2 | **Prompt Templates** | System/Human Messages, variables |
| 3 | **Chains (LCEL)** | Chaînes et syntaxe pipe (`\|`) |
| 4 | **Memory** | Mémoire conversationnelle, sessions |
| 5 | **RAG** | Embeddings, Vector Store, interroger ses documents |
| 6 | **Agents** | Outils, décisions autonomes, LangGraph |

---

Bon apprentissage ! 🚀
