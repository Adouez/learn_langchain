# 📝 CONTRÔLE DE CONNAISSANCES - LangChain (Leçons 6 à 10)

**📅 Date du contrôle** : 25 janvier 2026  
**👤 Candidat** : Antoine

---

## 📋 Informations

| | |
|---|---|
| **Cours couverts** | Agents, Chains vs Graphs, Streamlit, Structured Output, Tools Avancés |
| **Nombre de questions** | 18 (3 rappels + 15 nouvelles) |
| **Score final** | **15/21 (71%)** |
| **Notation** | ✅ Acquis / 🔄 À revoir / ❌ Non acquis |

---

# 🔄 RAPPELS - Cours 0 à 5

### Question R1 - LCEL (Leçon 3)
**Q : Que signifie LCEL et quelle est sa syntaxe de base ?**

> **Réponse d'Antoine** : "La signification de chaque lettre je sais plus mais c'est pour faire la chain de langchain, tu mets le LLM, le prompt system etc... à séparer avec des |"

🔄 **À revoir** — Concept et syntaxe OK, mais acronyme oublié.

**Rappel** : LCEL = **L**ang**C**hain **E**xpression **L**anguage

---

### Question R2 - RAG (Leçon 5)
**Q : Que signifie RAG ? Cite 3 composants utilisés dans un pipeline RAG.**

> **Réponse d'Antoine** : "Je tente : retrieved augmented generation ? Il faut charger les documents, les découper en chunk, stocker ces chunks"

🔄 **À revoir** — Presque ! C'est **Retrieval** (pas Retrieved).

**Rappel** : RAG = **Retrieval** Augmented Generation

---

### Question R3 - Mémoire (Leçon 4)
**Q : Quel est le rôle de MessagesPlaceholder dans un Prompt Template ?**

> **Réponse d'Antoine** : "C'est où tu vas placer l'historique de la conversation de l'utilisateur"

✅ **Acquis** — Parfait !

---

**Score Rappels** : ❌ **1/3**

---

# 🤖 PARTIE 1 : Les Agents (Leçon 6)

### Question 1 - Définition
**Q : Quelle est la différence fondamentale entre une Chain classique et un Agent ?**

> **Réponse d'Antoine** : "L'agent décide tout seul de la marche à suivre que la chain est défini"

✅ **Acquis** — Parfait ! L'Agent décide dynamiquement, la Chain suit un chemin fixe.

---

### Question 2 - Composants
**Q : Un Agent est composé de 3 éléments principaux. Lesquels ?**

> **Réponse d'Antoine** : "Le LLM, des outils (tools, RAG) et des paramètres (nb d'itération)"

🔄 **À revoir** (2/3 correct)

| Ta réponse | Correction |
|------------|------------|
| Le LLM ✅ | Le Cerveau (LLM) |
| Des outils ✅ | Les Outils (Tools) |
| Des paramètres ❌ | La **Boucle de Raisonnement (ReAct)** |

---

### Question 3 - ReAct
**Q : Que signifie ReAct et quel cycle suit un Agent ?**

> **Réponse d'Antoine** : "Re action, ça permet à l'agent de réfléchir à quel outil choisir, lire la réponse donnée par l'outil et adapter / refaire l'action en fonction de la réponse et ainsi de suite"

✅ **Acquis** — Cycle parfaitement décrit ! Juste une précision : ReAct = **Reason + Act** (pas "Re-action")

---

### Question 4 - Code
**Q : Dans ce code, à quoi sert la docstring de la fonction ?**
```python
@tool
def calculatrice(expression: str) -> str:
    """Utile pour faire des calculs mathématiques."""
    return str(eval(expression))
```

> **Réponse d'Antoine** : "C'est ce que va lire l'agent, le LLM pour savoir à quoi sert le tool et quand l'utiliser"

✅ **Acquis** — Parfait !

---

### Question 5 - Pratique
**Q : Quelle fonction de LangGraph utilise-t-on pour créer un Agent ReAct ?**

> **Réponse d'Antoine** : "create_react_agent() mais apparemment il y a une nouvelle version où create_agent suffit"

✅ **Acquis** — Correct ! `from langgraph.prebuilt import create_react_agent`

---

**Score Partie 1 (Agents)** : ✅ **4/5**

---

# ⚔️ PARTIE 2 : Chains vs Graphs (Leçon 7)

### Question 6 - Comparaison
**Q : Complète le tableau Chains vs Graphs**

> **Réponse d'Antoine** :
> - Chains : flux linéaire, boucles non, complexité facile
> - Graphs : flux arbre, boucles oui, complexité moyen

✅ **Acquis** (5/6 cases correctes) — "Arbre" → le terme exact est **"Flexible"**

---

### Question 7 - Règle d'Or
**Q : Complète : "Commence avec ______. Passe à ______ quand tu as besoin de ______ ou ______."**

> **Réponse d'Antoine** : "A, B x ou Y"

❌ **Non acquis**

**La règle d'or** : "Commence avec **LCEL**. Passe à **LangGraph** quand tu as besoin de **boucles** ou **conditions**."

---

### Question 8 - Cas d'Usage
**Q : Pour chaque situation, LCEL ou LangGraph ?**

> **Réponse d'Antoine** : "1 LCEL, 2 LG, 3 LG"

✅ **Acquis** — Parfait !

| Situation | Réponse | Verdict |
|-----------|---------|---------|
| Question → Réponse simple | LCEL | ✅ |
| Agent avec plusieurs outils | LangGraph | ✅ |
| Workflow avec boucle de validation | LangGraph | ✅ |

---

**Score Partie 2 (Chains vs Graphs)** : 🔄 **2/3**

---

# 🎨 PARTIE 3 : Streamlit (Leçon 8)

### Question 9 - Composants
**Q : Associe chaque composant Streamlit à sa fonction**

> **Réponse d'Antoine** : "st.chat_message() afficher le message du chat, st.chat_input là où l'utilisateur écrit, st.session_state mémoire de la conversation et st.spinner()..."

🔄 **À revoir** (3/4 correct)

| Composant | Réponse | Verdict |
|-----------|---------|---------|
| `st.chat_message()` | Afficher le message | ✅ |
| `st.chat_input()` | Là où l'utilisateur écrit | ✅ |
| `st.session_state` | Mémoire de la conversation | ✅ |
| `st.spinner()` | *(pas de réponse)* | ❌ |

**Réponse manquante** : `st.spinner()` = Indicateur de chargement

---

### Question 10 - Mémoire
**Q : Pourquoi st.session_state est-il CRUCIAL pour un chatbot Streamlit ?**

> **Réponse d'Antoine** : "Oui, sinon pas de mémoire, il oublie tout. Et ça sert à différencier les conversations"

✅ **Acquis** — Streamlit recharge le script à chaque interaction → sans session_state, tout est perdu !

---

### Question 11 - Lancement
**Q : Quelle commande utilise-t-on pour lancer une application Streamlit ?**

> **Réponse d'Antoine** : "streamlit run"

✅ **Acquis** — `streamlit run fichier.py`

---

**Score Partie 3 (Streamlit)** : 🔄 **2/3**

---

# 📊 PARTIE 4 : Structured Output (Leçon 9)

### Question 12 - Problème
**Q : Quel problème résout le Structured Output ?**

> **Réponse d'Antoine** : "Pouvoir transformer la réponse de l'agent en structure lisible pour une API ou une BDD"

✅ **Acquis** — Parfait ! Texte libre → Structure exploitable programmatiquement.

---

### Question 13 - Méthode
**Q : Quelle est la méthode recommandée pour forcer un format de sortie en LangChain ?**

> **Réponse d'Antoine** : "La fonction with_structured_output (mais natif OpenAI donc que pour les modèles OpenAI ?) Pydantic, les classes Python"

✅ **Acquis** — `llm.with_structured_output(MonSchema)` + bonne observation sur la compatibilité !

---

### Question 14 - Pydantic
**Q : À quoi sert Field(description=...) ?**

> **Réponse d'Antoine** : "Très important c'est pour dire au LLM à quoi correspond ce champ, ce qu'il doit mettre dedans"

✅ **Acquis** — Parfait ! Les descriptions guident le LLM.

---

### Question 15 - Types
**Q : Quel type Pydantic pour limiter une valeur à quelques choix possibles ?**

> **Réponse d'Antoine** : `literal[""]`

✅ **Acquis** — `Literal["spam", "important", "normal"]`

---

**Score Partie 4 (Structured Output)** : ✅ **4/4** 🎉

---

# 🔧 PARTIE 5 : Tools Avancés (Leçon 10)

### Question 16 - Méthodes
**Q : Il existe 3 façons de créer des outils dans LangChain. Lesquelles ?**

> **Réponse d'Antoine** : "@tool qu'on a dans scripts/tools, un autre oublié et baselmodel"

🔄 **À revoir** (1/3 correct)

| Ta réponse | Correction |
|------------|------------|
| `@tool` ✅ | Simple |
| "oublié" ❌ | `StructuredTool` (intermédiaire) |
| "baselmodel" 🔄 | `BaseTool` (pas BaseModel !) |

---

### Question 17 - Erreurs
**Q : Quelle est la bonne pratique pour gérer les erreurs dans un outil ?**

> **Réponse d'Antoine** : "Retourner un message d'erreur c'est mieux, plus simple avec StructuredTool et BaseTool"

✅ **Acquis** — Retourner un message permet à l'agent de comprendre et réessayer !

---

### Question 18 - BaseTool
**Q : Quel avantage unique offre la classe BaseTool par rapport à @tool ?**

> **Réponse d'Antoine** : "La gestion d'état, quand il retente un tool, il se souvient de pourquoi"

✅ **Acquis** — État interne persistant entre les appels !

---

**Score Partie 5 (Tools Avancés)** : 🔄 **2/3**

---

# 🎁 BONUS - Question de Synthèse (non posée)

### Question Bonus
Tu dois créer une application complète qui :
- A une interface graphique
- Utilise un Agent avec plusieurs outils
- Retourne des données structurées (JSON)
- Peut interroger une base de documents

**Quels concepts/outils de LangChain vas-tu combiner ?** (Cite au moins 6 éléments)

---

# 🏆 RÉSULTATS FINAUX

## 📊 Score par Partie

| Partie | Score | Appréciation |
|--------|-------|--------------|
| 🔄 Rappels (0-5) | 1/3 | ❌ À réviser |
| 1. Agents | 4/5 | ✅ Très bien |
| 2. Chains vs Graphs | 2/3 | 🔄 Correct |
| 3. Streamlit | 2/3 | 🔄 Correct |
| 4. Structured Output | 4/4 | ✅ Parfait ! 🎉 |
| 5. Tools Avancés | 2/3 | 🔄 Correct |
| **TOTAL** | **15/21** | **71%** |

---

## 📈 Comparaison avec le Contrôle Précédent

| Critère | Contrôle 0-5 | Contrôle 6-10 |
|---------|--------------|---------------|
| Score | 67% | **71%** ↗️ |
| Points faibles | LCEL, RAG | Toujours les acronymes |
| Points forts | Mémoire | Structured Output, Agents |

---

## 💪 Points Forts

- ✅ **Structured Output** : Maîtrise parfaite (4/4)
- ✅ **Agents** : Excellente compréhension (ReAct, @tool, docstring)
- ✅ **Cas d'usage** : Tu sais quand utiliser LCEL vs LangGraph
- ✅ **Bonnes pratiques** : Gestion des erreurs, descriptions claires

## 📚 Points à Réviser

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **LCEL** | = **L**ang**C**hain **E**xpression **L**anguage |
| **RAG** | = **Retrieval** Augmented Generation (pas "Retrieved") |
| **ReAct** | = **Reason + Act** (pas "Re-action") |
| **Règle d'or** | Commence avec LCEL → LangGraph si boucles/conditions |
| **3 méthodes outils** | `@tool` → `StructuredTool` → `BaseTool` |
| **st.spinner()** | Indicateur de chargement |

---

## 🎓 Verdict Final

> **Très bonne progression !** Tu maîtrises les concepts avancés (Agents, Structured Output) et tu sais quand utiliser chaque outil. Les acronymes (LCEL, RAG, ReAct) restent ton point faible — essaie des moyens mnémotechniques !

**Recommandation** : Crée une fiche avec les acronymes à mémoriser :
- **LCEL** = LangChain Expression Language
- **RAG** = Retrieval Augmented Generation
- **ReAct** = Reason + Act
