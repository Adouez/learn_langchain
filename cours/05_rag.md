# 🔎 Leçon 5 : Le RAG (Retrieval Augmented Generation)

Le RAG est la technique qui permet de donner accès à vos propres données privées (PDF, TXT, Bases de données) à un LLM, sans avoir à le ré-entraîner.

## ⚙️ Comment ça marche ? (Le Pipeline RAG)

C'est un processus en 3 étapes principales :

1.  **Ingestion & Indexation (Préparation)**
    *   **Load** : On charge le fichier (ex: `TextLoader`, `PyPDFLoader`).
    *   **Split** : On découpe le texte en petits morceaux ("chunks") pour ne pas dépasser la limite de taille du modèle.
    *   **Embed** : On transforme ces morceaux en listes de nombres (vecteurs) grâce à un modèle d'embedding (ex: `OpenAIEmbeddings`).
    *   **Store** : On sauvegarde ces vecteurs dans une base de données vectorielle (ex: `FAISS`, `ChromaDB`).

2.  **Retrieval (Recherche)**
    *   Quand l'utilisateur pose une question, on la transforme aussi en vecteurs.
    *   On cherche dans la base les morceaux qui "ressemblent" le plus à la question (recherche de similarité sémantique).

3.  **Generation (Réponse)**
    *   On envoie au LLM : La question + Les morceaux trouvés.
    *   Prompt : *"Utilise ces morceaux pour répondre à la question"*.

## 💻 Exemple de code (`4_rag_basics.py`)

```python
# 1. Charger et Découper
loader = TextLoader("mon_document.txt")
chunks = CharacterTextSplitter(chunk_size=500).split_documents(loader.load())

# 2. Indexer (Vector Store)
vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# 3. Chaîne RAG
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

## ⚠️ Points d'attention
- **La qualité des données** : "Garbage in, garbage out". Si votre document est mal écrit ou mal découpé, la réponse sera mauvaise.
- **La taille des chunks** : Trop petits, on perd le contexte. Trop grands, on noie l'info précise.
