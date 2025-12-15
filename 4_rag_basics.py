import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. Charger le document
# On utilise un TextLoader simple ici. Pour des PDF, on utiliserait PyPDFLoader.
print("📚 Chargement du règlement de Poudlard...")
loader = TextLoader("reglement_poudlard.txt", encoding="utf-8")
documents = loader.load()

# 2. Découper le document (Chunking)
# Même si le texte est court, c'est une bonne pratique de le découper.
# chunk_size=500 : Des morceaux de 500 caractères environ.
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)
print(f"✅ Document découpé en {len(chunks)} morceaux.")

# 3. Créer la base de données vectorielle (Vector Store)
# Il nous faut des "Embeddings" : c'est ce qui transforme le texte en vecteurs (nombres)
# pour que l'ordinateur comprenne le sens des phrases.
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# On transforme le vectorstore en "Retriever" (Chercheur)
retriever = vectorstore.as_retriever()

# 4. Le Modèle et le Prompt RAG
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

template = """Tu es un assistant administratif de Poudlard.
Utilise le contexte suivant pour répondre à la question de l'élève.
Si tu ne trouves pas la réponse dans le contexte, dis simplement que tu ne sais pas.

Contexte : {context}

Question : {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 5. La Chaîne RAG
# C'est ici que tout s'assemble.
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt 
    | llm 
    | StrOutputParser()
)

# 6. Testons-le !
question = "Est-ce que je peux amener mon dragon norvégien dans ma chambre ?"
print(f"\n❓ Question : {question}")
print("🔍 Recherche dans le règlement...")

reponse = rag_chain.invoke(question)
print(f"\n📜 Réponse officielle :\n{reponse}")

print("\n--- Test 2 ---")
question2 = "A quelle heure est le couvre-feu pour les premières années ?"
print(f"❓ Question : {question2}")
reponse2 = rag_chain.invoke(question2)
print(f"📜 Réponse officielle :\n{reponse2}")

