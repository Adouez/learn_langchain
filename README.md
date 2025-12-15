# Apprendre LangChain avec Cursor 🦜🔗 + 🤖

Bienvenue dans ce dépôt d'apprentissage !

Ce projet est le fruit d'une méthode d'apprentissage moderne : **le pair programming avec l'IA**.
Il documente mon parcours pour maîtriser **LangChain**, le framework de référence pour développer des applications basées sur les LLM, guidé étape par étape par l'assistant IA de l'éditeur **Cursor**.

## 💡 Le Concept : Apprendre via Cursor

L'idée n'est pas simplement de copier-coller du code, mais de construire une compréhension solide par le dialogue avec l'IA :
1.  **Exploration interactive** : Je pose des questions conceptuelles ("Comment donner de la mémoire au bot ?").
2.  **Codage assisté** : L'IA propose une structure de code que nous affinons ensemble.
3.  **Documentation en temps réel** : Chaque concept appris est noté dans le fichier `COURS.md` pour ancrer les connaissances.
4.  **Progression itérative** : On part d'un script simple pour arriver à des architectures complexes (RAG, Agents).

C'est une façon d'apprendre plus rapide, plus pratique et totalement personnalisée.

## 📂 Contenu du dépôt

Les scripts suivent une progression pédagogique logique :

*   **`1_hello_langchain.py`** : La base. Connexion simple à OpenAI pour générer du texte.
*   **`2_chains.py`** : Introduction aux **Prompt Templates** et aux **Chaînes (LCEL)** pour structurer les interactions.
*   **`3_memory.py`** : Implémentation de la **Mémoire** pour créer un chatbot capable de suivre une conversation.
*   **`4_rag_basics.py`** : Introduction au **RAG (Retrieval Augmented Generation)** pour interroger ses propres documents.
*   📄 **`COURS.md`** : Mes notes de cours détaillées, explications théoriques et snippets de code clés.

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
    python 1_hello_langchain.py
    ```