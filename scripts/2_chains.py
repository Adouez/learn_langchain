from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. Le Modèle
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 2. Le Prompt Template (Le moule à questions)
# On définit un "rôle" (System) et la question de l'utilisateur (Human)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert technique en Python et LangChain. Tu expliques des concepts complexes avec des métaphores simples."),
    ("human", "{question}")
])

# 3. L'Output Parser (Le nettoyeur)
# Par défaut, le LLM renvoie un objet complexe (AIMessage). 
# Ce parser va extraire juste le texte (string) pour que ce soit plus propre.
output_parser = StrOutputParser()

# 4. La Chaîne (The Chain)
# C'est la magie de LangChain : on utilise le pipe "|" pour enchaîner les étapes.
# Prompt -> Modèle -> Nettoyeur
chain = prompt | llm | output_parser

# 5. Exécution
print("🤖 Le Professeur LangChain réfléchis...")
reponse = chain.invoke({"question": "C'est quoi LangChain exactement ?"})

print("\n💬 Réponse améliorée :")
print(reponse)
