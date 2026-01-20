"""
📚 Leçon 6 : RAG avec des fichiers Markdown
Ce script montre comment faire du RAG sur plusieurs documents Markdown.
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# =============================================================================
# 1. CHARGER LES DOCUMENTS MARKDOWN
# =============================================================================
# On utilise DirectoryLoader pour charger TOUS les fichiers Markdown d'un dossier d'un coup !
# - glob="**/*.md" : cherche tous les fichiers .md (même dans les sous-dossiers)
# - loader_cls=TextLoader : utilise TextLoader pour lire chaque fichier Markdown

print("📚 Chargement des règlements Cegedim...")

loader = DirectoryLoader(
    path="scripts/DocARag3",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},  # Important pour les accents français
    show_progress=True
)

documents = loader.load()
print(f"✅ {len(documents)} documents chargés depuis les fichiers Markdown.")

# =============================================================================
# 2. DÉCOUPER LES DOCUMENTS (CHUNKING)
# =============================================================================
# Pour les PDFs complexes, on utilise RecursiveCharacterTextSplitter
# C'est plus intelligent que CharacterTextSplitter car il découpe aux bons endroits
# (paragraphes, phrases, mots) pour garder le sens.

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Taille de chaque morceau (en caractères)
    chunk_overlap=200,    # Chevauchement entre morceaux (pour ne pas perdre de contexte)
    separators=["\n\n", "\n", ". ", " ", ""]  # Ordre de priorité pour couper
)

chunks = text_splitter.split_documents(documents)
print(f"✅ Documents découpés en {len(chunks)} morceaux.")

# =============================================================================
# 3. CRÉER LA BASE VECTORIELLE (INDEXATION)
# =============================================================================
# On transforme tous les chunks en vecteurs et on les stocke dans FAISS

print("🔄 Création de la base vectorielle (cela peut prendre quelques secondes)...")

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# On crée le retriever avec k=4 (retourne les 4 morceaux les plus pertinents)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

print("✅ Base vectorielle créée !")

# =============================================================================
# 4. CRÉER LA CHAÎNE RAG
# =============================================================================

llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Plus intelligent que gpt-3.5-turbo

template = """Tu es un assistant expert en règlements internes d'entreprise.
Tu as accès aux règlements Cegedim.

Utilise UNIQUEMENT le contexte fourni pour répondre à la question.
Si tu ne trouves pas l'information dans le contexte, dis-le clairement.

Contexte :
{context}

Question : {question}

Réponse :"""

prompt = ChatPromptTemplate.from_template(template)

# La chaîne RAG complète
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# =============================================================================
# 5. TESTER LE RAG
# =============================================================================

def poser_question(question: str):
    """Fonction helper pour poser une question et afficher la réponse."""
    print(f"\n❓ Question : {question}")
    print("🔍 Recherche dans les rapports...")
    reponse = rag_chain.invoke(question)
    print(f"\n📊 Réponse :\n{reponse}")
    print("-" * 60)

# Tests
print("\n" + "=" * 60)
print("🧪 TESTS DU RAG SUR LES RÈGLEMENTS CEGEDIM")
print("=" * 60)

poser_question("Quelles sont les règles concernant les contrats dans Pegase ?")
poser_question("Que se passe-t-il si la date de fin d'un CDI est entrée en retard dans Pegase ?")
poser_question("Comment un contrat est-il considéré comme valide ?")

# =============================================================================
# 6. MODE INTERACTIF (OPTIONNEL)
# =============================================================================

print("\n" + "=" * 60)
print("💬 MODE INTERACTIF")
print("Pose tes questions sur les règlements Cegedim.")
print("Tape 'quit' pour quitter.")
print("=" * 60)

while True:
    question = input("\n🎤 Ta question : ").strip()
    if question.lower() in ['quit', 'exit', 'q']:
        print("👋 À bientôt !")
        break
    if question:
        poser_question(question)
