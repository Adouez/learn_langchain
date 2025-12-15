# 🦜 Cours LangChain : De Zéro à Héros

Ce document regroupe les leçons progressives pour maîtriser LangChain.

## 🎓 Leçon 1 : Les Fondations

LangChain est un framework qui permet de connecter des modèles de langage (LLMs) à d'autres sources de données et d'outils.

Si GPT-4 est le **moteur**, LangChain est le **châssis** qui permet de construire une voiture autour.

### Concepts Clés :
- **LLM (Large Language Model)** : Le "cerveau" (ex: GPT-3.5, GPT-4).
- **API Key** : Le pass d'accès pour utiliser le cerveau.

### Exemple de code (`1_hello_langchain.py`) :
Une connexion simple pour poser une question brute.
```python
llm = ChatOpenAI(api_key="...", model="gpt-3.5-turbo")
response = llm.invoke("Bonjour !")
```

---

## 🧩 Leçon 2 : Structure et Prompt Templates

Les LLMs sont sensibles à la façon dont on leur parle. Pour obtenir de bons résultats de manière constante, on ne pose pas des questions brutes, on utilise des **Prompts Templates**.

### Pourquoi utiliser des Templates ?
1. **Réutilisabilité** : On crée un "moule" et on change juste les variables.
2. **Contextualisation** : On peut donner un "Rôle" au modèle (System Message) pour qu'il agisse comme un expert.

### Concepts Clés :
- **System Message** : Instruction cachée qui définit le comportement du bot ("Tu es un expert...").
- **Human Message** : La question de l'utilisateur.
- **Variable (`{question}`)** : La partie dynamique du template.

---

## 🔗 Leçon 3 : Les Chaînes (Chains) et LCEL

C'est le cœur de LangChain. Une "Chain" est une séquence d'actions.

### La syntaxe LCEL (LangChain Expression Language)
LangChain utilise une syntaxe élégante avec le symbole pipe `|` (comme en Unix/PowerShell) pour enchaîner les composants.

```python
chain = prompt | llm | output_parser
```
**Lecture :** "Prends l'entrée, passe-la au **Prompt**, envoie le résultat au **LLM**, puis nettoie la sortie avec le **Parser**."

### Les Composants de la Chaîne :
1. **Prompt** : Formate la question.
2. **LLM** : Génère la réponse brute (objet Message).
3. **Output Parser** : Transforme l'objet Message en texte simple (string).

### Exemple (`2_chains.py`) :
```python
prompt = ChatPromptTemplate.from_messages(...)
chain = prompt | llm | StrOutputParser()
chain.invoke({"question": "Explique..."})
```

---

## 🧠 Leçon 4 : La Mémoire (Memory)

Par défaut, un LLM est "stateless" (sans état) : il oublie tout après chaque réponse. Pour créer un Chatbot, il faut injecter l'historique de la conversation dans le Prompt à chaque tour.

### Comment ça marche ?
Au lieu d'envoyer juste la question actuelle, on envoie :
`[Historique des messages] + [Nouvelle Question]`

### Composants Clés :
1. **`MessagesPlaceholder`** : Une case vide dans le Prompt Template réservée pour insérer l'historique.
2. **`RunnableWithMessageHistory`** : Un outil qui gère automatiquement la sauvegarde des messages (ce que tu dis et ce que le bot répond) et leur réinjection au tour suivant.
3. **`session_id`** : Permet de distinguer les conversations de différents utilisateurs (ex: Alice vs Bob).

### Exemple (`3_memory.py`) :
```python
# Dans le prompt
MessagesPlaceholder(variable_name="history")

# L'exécution avec session_id
chain_with_history.invoke(
    {"question": "..."},
    config={"configurable": {"session_id": "user_123"}}
)
```

---

## 🔜 À venir : Leçon 5 - Le RAG (Retrieval Augmented Generation)

Maintenant que notre bot a de la mémoire, comment lui donner accès à VOS propres données (fichiers PDF, texte...) qu'il ne connait pas ? C'est le RAG.

