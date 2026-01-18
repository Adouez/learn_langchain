"""
🔍 Outil RAG - Recherche dans les rapports Clinitex
===================================================
"""

import os
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Variable globale pour le retriever (lazy loading)
_retriever = None


def init_retriever_clinitex(path: str = "scripts/DocArag2"):
    """
    Initialise le retriever RAG une seule fois.
    Appelé automatiquement au premier usage de l'outil.
    
    Args:
        path: Chemin vers le dossier contenant les PDFs
    """
    global _retriever
    
    if _retriever is None:
        print("📚 Initialisation du RAG Clinitex...")
        
        # Charger tous les PDFs
        loader = DirectoryLoader(
            path=path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        documents = loader.load()
        print(f"   ✅ {len(documents)} pages chargées")
        
        # Découper en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"   ✅ {len(chunks)} morceaux créés")
        
        # Créer le vectorstore
        print("   🔄 Création de la base vectorielle...")
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        print("   ✅ RAG Clinitex prêt !")
    
    return _retriever


@tool
def recherche_rapports_clinitex(question: str) -> str:
    """Utile pour chercher des informations dans les rapports de maturité digitale Clinitex.
    Permet de trouver : scores de maturité, recommandations, axes d'amélioration, 
    points forts/faibles, comparaisons entre consultants (Antoine, Nicolas, Sacha, Stéphane).
    Entrée : une question sur les rapports de maturité."""
    
    retriever = init_retriever_clinitex()
    docs = retriever.invoke(question)
    
    if docs:
        resultats = []
        for doc in docs:
            source = doc.metadata.get("source", "inconnu")
            nom_fichier = os.path.basename(source)
            resultats.append(f"[Source: {nom_fichier}]\n{doc.page_content}")
        
        contexte = "\n\n---\n\n".join(resultats)
        return f"Informations trouvées dans les rapports :\n\n{contexte}"
    
    return "Aucune information pertinente trouvée dans les rapports."
