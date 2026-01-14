# 🤖 Leçon 6 : Les Agents - Quand le LLM Prend les Commandes

## 🧠 L'Idée Centrale

Jusqu'ici, nos programmes suivaient un chemin **prédéfini** :
- Chaîne simple : `Prompt → LLM → Réponse`
- RAG : `Question → Recherche → LLM → Réponse`

Avec un **Agent**, le LLM devient le **chef d'orchestre**. Il décide lui-même :
- Quel outil utiliser
- Dans quel ordre
- Quand il a assez d'informations pour répondre

---

## 🎭 Métaphore : Le Chef Cuisinier

| Concept | Chaîne Classique | Agent |
|---------|------------------|-------|
| Recette | Suivie à la lettre | Adaptée selon les ingrédients disponibles |
| Décision | Aucune (linéaire) | "Hmm, il me manque du sel, je vais chercher..." |
| Outils | Utilisés dans l'ordre prévu | Choisis selon le besoin |

> 💡 **Une Chain** = Un robot qui suit des instructions fixes.  
> 💡 **Un Agent** = Un assistant intelligent qui réfléchit à chaque étape.

---

## ⚙️ Les Composants d'un Agent

### 1. 🧠 Le Cerveau (LLM)
Le modèle qui réfléchit et prend les décisions. Il doit être capable de "raisonner" (GPT-4, GPT-3.5-turbo, Claude...).

### 2. 🛠️ Les Outils (Tools)
Des fonctions que l'Agent peut appeler. Exemples :
- `calculatrice` : pour faire des calculs
- `recherche_web` : pour chercher sur internet
- `lecteur_fichier` : pour lire des documents
- `base_de_données` : pour interroger une BDD

### 3. 🔄 La Boucle de Raisonnement (ReAct)
L'agent suit un cycle :
```
RÉFLEXION → ACTION → OBSERVATION → RÉFLEXION → ...
```

Jusqu'à ce qu'il ait assez d'infos pour donner la réponse finale.

---

## 🔄 Le Cycle ReAct (Reason + Act)

```
┌─────────────────────────────────────────────────┐
│  1. PENSÉE : "Pour répondre, j'ai besoin de..." │
│         ↓                                       │
│  2. ACTION : Appelle l'outil `calculatrice`     │
│         ↓                                       │
│  3. OBSERVATION : "Le résultat est 42"          │
│         ↓                                       │
│  4. PENSÉE : "Maintenant je peux répondre !"    │
│         ↓                                       │
│  5. RÉPONSE FINALE                              │
└─────────────────────────────────────────────────┘
```

---

## 💻 Structure du Code (`5_agents.py`)

Depuis **LangChain 1.x**, les agents sont gérés par **LangGraph** (plus simple et plus puissant).

```python
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# 1. Définir les outils avec le décorateur @tool
# La DOCSTRING devient automatiquement la description !
@tool
def calculatrice(expression: str) -> str:
    """Utile pour faire des calculs mathématiques."""
    return str(eval(expression))

tools = [calculatrice]

# 2. Créer l'agent (cerveau + outils + prompt système)
agent = create_react_agent(
    llm, 
    tools,
    prompt="Tu es un assistant intelligent. Utilise les outils disponibles."
)

# 3. Lancer l'agent (LangGraph gère la boucle automatiquement)
result = agent.invoke({"messages": [{"role": "user", "content": "Racine carrée de 144 ?"}]})
reponse = result["messages"][-1].content
```

---

## 🎯 Quand Utiliser un Agent ?

| Situation | Solution |
|-----------|----------|
| Question simple, pas besoin d'outil | Chaîne classique |
| Besoin de chercher dans vos docs | RAG |
| Tâche complexe nécessitant plusieurs outils | **Agent** |
| L'utilisateur peut poser des questions variées | **Agent** |

---

## ⚠️ Points d'Attention

1. **Coût** : Un agent fait plusieurs appels au LLM (réflexion à chaque étape) → plus cher.
2. **LangGraph** : Depuis LangChain 1.x, utilisez `langgraph.prebuilt.create_react_agent` (plus l'ancien `AgentExecutor`).
3. **Docstrings** : Avec le décorateur `@tool`, la **docstring** de la fonction devient automatiquement la description de l'outil. C'est ce que le LLM lit pour décider quel outil utiliser !
4. **Debugging** : Ajoutez des `print()` dans vos outils pour tracer les appels.

---

## ✅ Points à Retenir

- Un **Agent** = LLM + Outils + Boucle de raisonnement
- Le LLM **décide** quel outil utiliser (contrairement à une chaîne fixe)
- **ReAct** = Reason (réfléchir) + Act (agir) en boucle
- **LangGraph** gère les agents depuis LangChain 1.x (remplace `AgentExecutor`)
- Le décorateur `@tool` + la **docstring** = outil prêt à l'emploi
- Le résultat est dans `result["messages"][-1].content`

---

## 🔜 Prochaine Étape

Maintenant que tu comprends les Agents, on pourra créer une **interface Streamlit** pour interagir avec notre assistant de manière graphique ! 🚀


