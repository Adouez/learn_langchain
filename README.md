# Apprendre LangChain avec Cursor 🦜🔗 + 🤖 ad

Bienvenue dans ce dépôt d'apprentissage !

Ce projet est le fruit d'une méthode d'apprentissage moderne : **le pair programming avec l'IA**.
Il documente mon parcours pour maîtriser **LangChain**, le framework de référence pour développer des applications basées sur les LLM, guidé étape par étape par l'assistant IA de l'éditeur **Cursor**.

## 💡 Le Concept : Apprendre via Cursor

L'idée n'est pas simplement de copier-coller du code, mais de construire une compréhension solide par le dialogue avec l'IA :
1.  **Exploration interactive** : Je pose des questions conceptuelles ("Comment donner de la mémoire au bot ?").
2.  **Codage assisté** : L'IA propose une structure de code que nous affinons ensemble.
3.  **Documentation en temps réel** : Chaque concept appris est noté dans le dossier `cours/` pour ancrer les connaissances.
4.  **Progression itérative** : On part d'un script simple pour arriver à des architectures complexes (RAG, Agents).

C'est une façon d'apprendre plus rapide, plus pratique et totalement personnalisée.

## 📂 Structure du Projet

```
learn-langchain/
├── 📁 scripts/                    # Exercices pratiques Python
│   ├── 1_hello_langchain.py      # Connexion simple à OpenAI
│   ├── 2_chains.py               # Prompt Templates et Chaînes LCEL
│   ├── 3_memory.py               # Mémoire conversationnelle
│   └── 4_rag_basics.py           # RAG (interroger ses documents)
│
├── 📁 cours/                      # Leçons théoriques détaillées
│   ├── 00_introduction.md        # Vue d'ensemble et sommaire
│   ├── 01_fondations.md          # LLM, API Key, bases
│   ├── 02_prompt_templates.md    # System/Human Messages, variables
│   ├── 03_chains_lcel.md         # Chaînes et syntaxe LCEL (|)
│   ├── 04_memory.md              # Mémoire et session_id
│   └── 05_rag.md                 # RAG, Embeddings, Vector Store
│
├── 📁 agents/                     # Rôles des agents IA
│   ├── PROFESSOR.md              # Le professeur pédagogue
│   ├── ASSISTANT.md              # L'assistant personnel
│   └── CONTROLEUR.md             # Le contrôleur de connaissances
│
├── 📁 DocARag/                    # Documents pour le RAG
│   └── reglement_poudlard.txt    # Document d'exemple
│
├── README.md                      # Ce fichier
└── requirements.txt               # Dépendances Python
```

## 🚀 Utilisation

Pour tester ces scripts chez vous :

1.  **Cloner le repo** :
    ```bash
    git clone https://github.com/Adouez/learn_langchain.git
    cd learn_langchain
    ```

2.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurer l'environnement** :
    Créez un fichier `.env` à la racine et ajoutez votre clé API :
    ```env
    OPENAI_API_KEY=sk-...
    ```

4.  **Lancer un script** :
    ```bash
    python scripts/1_hello_langchain.py
    ```

## 📚 Parcours Recommandé

| Étape | Script | Leçon | Concept |
|-------|--------|-------|---------|
| 1 | `scripts/1_hello_langchain.py` | `cours/01_fondations.md` | Connexion au LLM |
| 2 | `scripts/2_chains.py` | `cours/02_prompt_templates.md` | Templates de prompts |
| 3 | `scripts/2_chains.py` | `cours/03_chains_lcel.md` | Chaînes LCEL |
| 4 | `scripts/3_memory.py` | `cours/04_memory.md` | Mémoire conversationnelle |
| 5 | `scripts/4_rag_basics.py` | `cours/05_rag.md` | RAG et documents |

## 🤖 Les Agents IA

Ce projet utilise trois "rôles" d'IA pour enrichir l'apprentissage :

- **🎓 PROFESSOR** : Enseigne et crée les exercices
- **🧙‍♂️ ASSISTANT** : Répond aux questions et guide
- **📋 CONTROLEUR** : Vérifie la compréhension avec des quiz
