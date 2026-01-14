from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. Configuration de base
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 2. Le Prompt avec une place pour l'historique
# "history" est une variable spéciale où LangChain va injecter la conversation
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant amical qui se souvient des détails."),
    MessagesPlaceholder(variable_name="history"), # <-- L'emplacement de la mémoire
    ("human", "{question}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# 3. La Gestion de la Mémoire
# Nous devons stocker l'historique quelque part. Ici, dans un dictionnaire simple en mémoire RAM.
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# On emballe notre chaîne simple avec le gestionnaire d'historique
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

# 4. Simulation d'une conversation
session_id = "user_123" # Identifiant unique de l'utilisateur

print("--- Échange 1 ---")
response1 = chain_with_history.invoke(
    {"question": "Bonjour ! Je m'appelle Antoine."},
    config={"configurable": {"session_id": session_id}}
)
print(f"Toi: Bonjour ! Je m'appelle Antoine.\nBot: {response1}\n")

print("--- Échange 2 ---")
response2 = chain_with_history.invoke(
    {"question": "Quel est mon nom ?"}, # Le bot doit se souvenir d'Antoine
    config={"configurable": {"session_id": session_id}}
)
print(f"Toi: Quel est mon nom ?\nBot: {response2}")
