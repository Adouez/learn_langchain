"""
🔍 Outil RAG - Recherche dans les règlements Cegedim
====================================================
"""

import os
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Variable globale pour le retriever (lazy loading)
_retriever_cegedim = None


def init_retriever_cegedim(path: str = "scripts/DocARag3"):
    """
    Initialise le retriever RAG pour les documents Cegedim.
    
    Args:
        path: Chemin vers le dossier contenant les documents
    """
    global _retriever_cegedim
    
    if _retriever_cegedim is None:
        print("📚 Initialisation du RAG Cegedim...")
        
        # Charger tous les fichiers markdown et txt
        loader = DirectoryLoader(
            path=path,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True
        )
        documents = loader.load()
        
        # Ajouter les fichiers .txt si présents
        try:
            loader_txt = DirectoryLoader(
                path=path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"}
            )
            documents.extend(loader_txt.load())
        except:
            pass
        
        print(f"   ✅ {len(documents)} documents chargés")
        
        # Découper en chunks (petits pour ce petit document)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"   ✅ {len(chunks)} morceaux créés")
        
        # Créer le vectorstore
        print("   🔄 Création de la base vectorielle...")
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        _retriever_cegedim = vectorstore.as_retriever(search_kwargs={"k": 3})
        print("   ✅ RAG Cegedim prêt !")
    
    return _retriever_cegedim


@tool
def recherche_reglements_cegedim(question: str) -> str:
    """Utile pour chercher des informations dans les règlements et procédures Cegedim.
    Permet de trouver : règles de contrats, procédures Pegase, règles Spayr, CDI/CDD, acomptes.
    Entrée : une question sur les règlements ou procédures internes Cegedim."""
    
    retriever = init_retriever_cegedim()
    docs = retriever.invoke(question)
    
    if docs:
        resultats = []
        for doc in docs:
            source = doc.metadata.get("source", "inconnu")
            nom_fichier = os.path.basename(source)
            resultats.append(f"[Source: {nom_fichier}]\n{doc.page_content}")
        
        contexte = "\n\n---\n\n".join(resultats)
        return f"Informations trouvées dans les règlements Cegedim :\n\n{contexte}"
    
    return "Aucune information pertinente trouvée dans les règlements Cegedim."
