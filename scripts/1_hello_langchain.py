import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Charger les variables d'environnement (la clé API)
load_dotenv()

# Vérification simple
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️ ERREUR : La clé API n'est pas trouvée. Vérifie ton fichier .env !")
else:
    print("✅ Clé API chargée.")

# 2. Initialiser le modèle (Le "Moteur")
# temperature=0 rend le modèle très factuel et précis. 
# temperature=1 le rend plus créatif.
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 3. Lui poser une question directement
print("\n🤖 Je réfléchis...")
response = llm.invoke("Explique-moi ce qu'est LangChain en une phrase simple pour un enfant de 10 ans.")

# 4. Afficher la réponse
print(f"\n💬 Réponse :\n{response.content}")
