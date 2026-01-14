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

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# 1. Définir les outils
tools = [
    Tool(name="calculatrice", func=ma_fonction, description="...")
]

# 2. Créer l'agent (cerveau + outils)
agent = create_react_agent(llm, tools, prompt)

# 3. L'exécuteur gère la boucle ReAct
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. Lancer l'agent
resultat = executor.invoke({"input": "Quelle est la racine carrée de 144 ?"})
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
2. **Verbosité** : Activez `verbose=True` pour comprendre ce que fait l'agent.
3. **Outils bien décrits** : La description des outils est CRUCIALE. C'est ce que le LLM lit pour décider quel outil utiliser !
4. **Boucles infinies** : Limitez le nombre d'itérations (`max_iterations`).

---

## ✅ Points à Retenir

- Un **Agent** = LLM + Outils + Boucle de raisonnement
- Le LLM **décide** quel outil utiliser (contrairement à une chaîne fixe)
- **ReAct** = Reason (réfléchir) + Act (agir) en boucle
- La **description des outils** guide les décisions de l'agent
- Utilisez `verbose=True` pour voir le raisonnement interne

---

## 🔜 Prochaine Étape

Maintenant que tu comprends les Agents, on pourra créer une **interface Streamlit** pour interagir avec notre assistant de manière graphique ! 🚀


