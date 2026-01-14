# 📝 CONTRÔLE DE CONNAISSANCES - LangChain (Leçons 0 à 5)

**📅 Date du contrôle** : 12 janvier 2026  
**👤 Candidat** : Antoine

---

## 📋 Informations

| | |
|---|---|
| **Cours couverts** | Introduction, Fondations, Prompt Templates, Chains/LCEL, Memory, RAG |
| **Nombre de questions** | 15 |
| **Score final** | **10/15 (67%)** |
| **Notation** | ✅ Acquis / 🔄 À revoir / ❌ Non acquis |

---

# 🚀 PARTIE 1 : La Métaphore (Leçon 0)

### Question 1 - Compréhension
Dans la métaphore de la voiture, à quoi correspond chaque élément ?

| Élément | Réponse d'Antoine | Correction | Verdict |
|---------|-------------------|------------|---------|
| **Le moteur** | LLM (GPT-4) | LLM | ✅ |
| **Le châssis** | L'appel API | **LangChain** (le framework) | ❌ |
| **Le système de transmission** | Le prompting | **Les Chains** (enchaînement avec `\|`) | 🔄 |
| **Le GPS avec historique** | La mémoire | Memory | ✅ |
| **Le coffre à bagages** | Les documents | RAG | ✅ |

**Score Q1** : 🔄 À revoir (3/5)

---

# 🔌 PARTIE 2 : Les Fondations (Leçon 1)

### Question 2 - Définition
**Q : Qu'est-ce qu'un LLM ? Donne un exemple.**

> **Réponse d'Antoine** : "C'est un modèle IA spécialisé dans la conversation avec un humain. Les modèles les plus connus sont ChatGPT, Gemini, Claude Opus, DeepSeek"

✅ **Acquis** — Bonne réponse ! Précision : LLM = Large Language Model, capable de comprendre ET générer du langage naturel (pas uniquement conversation).

---

### Question 3 - Sécurité
**Q : Pourquoi ne faut-il jamais mettre sa clé API directement dans le code ? Quelle est la bonne pratique ?**

> **Réponse d'Antoine** : "Il faut mettre la clé API dans un .env ou tout autre fichier énuméré dans .gitignore"

✅ **Acquis** — Bonne pratique identifiée ! Le "pourquoi" implicite : éviter l'exposition publique de la clé (factures, abus).

---

### Question 4 - Code
**Q : Quelle méthode utilise-t-on pour envoyer un message au modèle et recevoir une réponse ?**

> **Réponse d'Antoine** : "invoke"

✅ **Acquis** — Parfait ! `llm.invoke("message")`

---

**Score Partie 2** : ✅ **3/3**

---

# 🧩 PARTIE 3 : Prompt Templates (Leçon 2)

### Question 5 - Compréhension
**Q : Explique la différence entre un System Message et un Human Message. À quoi sert chacun ?**

> **Réponse d'Antoine** : "Le prompt system donne une direction au LLM, comment il doit se comporter. Le prompt humain c'est ce que l'humain demande et à quoi doit répondre le LLM en se comportant comme le prompt system l'a défini"

✅ **Acquis** — Excellente compréhension de la relation entre les deux !

---

### Question 6 - Avantages
**Q : Cite 2 avantages d'utiliser des Prompt Templates plutôt que d'écrire les prompts "en dur".**

> **Réponse d'Antoine** : "C'est pour avoir une meilleure mémoire du LLM et ça stabilise le comportement global du LLM, réduisant les hallucinations ?"

❌ **Non acquis** — Confusion avec d'autres concepts.

**Les vraies réponses** :
1. **Réutilisabilité** : Un "moule" qu'on réutilise en changeant les variables
2. **Contextualisation** : Définir un rôle cohérent appliqué à chaque requête

---

### Question 7 - Syntaxe
**Q : Dans un Prompt Template, à quoi servent les `{accolades}` ?**

> **Réponse d'Antoine** : "C'est l'emplacement dans le prompt template de ce que va demander l'utilisateur humain"

✅ **Acquis** — Bonne idée ! Ce sont des **variables/placeholders** remplacées dynamiquement (pas seulement pour la question utilisateur : `{contexte}`, `{langue}`, etc.)

---

**Score Partie 3** : 🔄 **2/3**

---

# 🔗 PARTIE 4 : Chains et LCEL (Leçon 3)

### Question 8 - Définition
**Q : Que signifie LCEL ? À quoi ça sert ?**

> **Réponse d'Antoine** : "Je ne sais pas"

❌ **Non acquis**

**La réponse** : **LCEL = LangChain Expression Language**
- Syntaxe avec le pipe `|` pour enchaîner les composants
- `chain = prompt | llm | parser`

---

### Question 9 - Compréhension
**Q : Dans cette chaîne, explique le rôle de chaque composant :**
```python
chain = prompt | llm | StrOutputParser()
```

> **Réponse d'Antoine** : "Le prompt c'est l'ensemble des éléments (questions, variables, system) que l'on donne au LLM, le LLM c'est le modèle que l'on choisit pour répondre et le parser c'est la décomposition des éléments pour qu'ils soient divisés pour être ingérés correctement, par token, par le modèle LLM"

🔄 **À revoir** (2/3 correct)

| Composant | Réponse | Verdict |
|-----------|---------|---------|
| prompt | ✅ Correct | ✅ |
| llm | ✅ Correct | ✅ |
| StrOutputParser | ❌ Confusion avec tokenisation | ❌ |

**Correction** : Le Parser nettoie la **SORTIE** du LLM (transforme `AIMessage` en string), pas l'entrée !

---

### Question 10 - Flux de données
**Q : Décris ce qui se passe étape par étape quand on exécute :**
```python
chain.invoke({"question": "C'est quoi Python ?"})
```

> **Réponse d'Antoine** : "D'abord le prompt est envoyé au LLM, ensuite le LLM répond et à la fin de la chaîne, le parser nettoie la réponse"

✅ **Acquis** — Flux correct et correction sur le Parser retenue !

---

**Score Partie 4** : ❌ **1/3**

---

# 🧠 PARTIE 5 : La Mémoire (Leçon 4)

### Question 11 - Problème
**Q : Explique pourquoi un LLM est dit "stateless" par défaut. Quel problème cela pose pour un chatbot ?**

> **Réponse d'Antoine** : "Par défaut le LLM ne retient pas ce qui a été dit, il est 'reset' à chaque prompt. C'est un problème car si je lui dis que je m'appelle Antoine, qu'ensuite je lui demande comment je m'appelle et qu'il ne sait plus, la conversation n'aura aucun sens"

✅ **Acquis** — Excellente explication avec exemple concret !

---

### Question 12 - Composants
**Q : À quoi sert le `MessagesPlaceholder` dans un Prompt Template ?**

> **Réponse d'Antoine** : "Il vient ajouter à chaque question les questions et réponses précédentes entre le LLM et l'utilisateur"

✅ **Acquis** — Parfait ! C'est la "case vide" pour injecter l'historique.

---

### Question 13 - Utilité
**Q : Pourquoi utilise-t-on un `session_id` ? Donne un exemple concret.**

> **Réponse d'Antoine** : "C'est pour 'enregistrer' un historique, ça permet de revenir dessus. Si j'ai une discussion au sujet d'une recette de mayonnaise et qu'ensuite je veux une recette d'œuf mimosa, je peux reprendre le session_id de ma mayonnaise pour faire mon œuf mimosa"

✅ **Acquis** — Bon exemple ! Permet aussi de séparer les utilisateurs (Alice vs Bob).

---

**Score Partie 5** : ✅ **3/3** 🎉

---

# 📚 PARTIE 6 : RAG (Leçon 5)

### Question 14 - Définition
**Q : Que signifie RAG et à quoi ça sert ?**

> **Réponse d'Antoine** : "Je n'ai pas la signification de RAG mais ça permet d'ajouter du contenu 'perso' aux connaissances du LLM, des documents privés etc..."

🔄 **À revoir** — Utilité comprise, acronyme manquant.

**La réponse** : **RAG = Retrieval Augmented Generation** (Génération Augmentée par Récupération)

---

### Question 15 - Processus
**Q : Remets dans l'ordre les étapes du RAG :**

| Étape | Réponse d'Antoine | Correct | Verdict |
|-------|-------------------|---------|---------|
| Charger le document | 1 | 1 | ✅ |
| Découper en chunks | 2 | 2 | ✅ |
| Stocker dans une base vectorielle | 3 | **4** | ❌ |
| Transformer en vecteurs (embeddings) | 4 | **3** | ❌ |
| Chercher les morceaux pertinents | 5 | 5 | ✅ |
| Générer une réponse avec le contexte | 6 | 6 | ✅ |

🔄 **À revoir** (4/6) — Inversion : on vectorise AVANT de stocker !

**Ordre correct** :
1. Charger → 2. Découper → 3. Vectoriser → 4. Stocker → 5. Chercher → 6. Générer

---

**Score Partie 6** : 🔄 **1/2**

---

# 🎁 BONUS - Question de Synthèse

### Question Bonus (non posée)
Tu dois créer un chatbot qui :
- Se souvient de la conversation
- Peut répondre à des questions sur un fichier PDF de règlement interne

Quels composants de LangChain vas-tu utiliser ? (Cite au moins 5 éléments)

---

# 🏆 RÉSULTATS FINAUX

## 📊 Score par Partie

| Partie | Score | Appréciation |
|--------|-------|--------------|
| 1. Métaphore | 3/5 | 🔄 À revoir |
| 2. Fondations | 3/3 | ✅ Acquis |
| 3. Prompt Templates | 2/3 | 🔄 Partiel |
| 4. Chains/LCEL | 1/3 | ❌ À travailler |
| 5. Mémoire | 3/3 | ✅ Acquis |
| 6. RAG | 1/2 | 🔄 Partiel |
| **TOTAL** | **10/15** | **67%** |

---

## 💪 Points Forts

- ✅ **Fondations** : Maîtrise de LLM, API Key, `invoke()`
- ✅ **Mémoire** : Excellente compréhension du stateless, MessagesPlaceholder, session_id
- ✅ **Exemples concrets** : Capacité à illustrer les concepts (mayonnaise, Antoine)

## 📚 Points à Réviser

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **LCEL** | = LangChain Expression Language (syntaxe avec `\|`) |
| **StrOutputParser** | Nettoie la **sortie** du LLM (pas l'entrée !) |
| **Châssis** | = LangChain (le framework), pas l'API |
| **RAG** | = Retrieval Augmented Generation |
| **Ordre RAG** | Vectoriser **avant** de stocker |
| **Avantages Templates** | Réutilisabilité + Contextualisation |

---

## 🎓 Verdict Final

> **Bon niveau général !** Compréhension solide des concepts clés et de leurs usages pratiques. Quelques définitions techniques à mémoriser (LCEL, RAG) et la Leçon 3 (Chains) à retravailler.

**Recommandation** : Relire la Leçon 3 sur les Chains et LCEL.
