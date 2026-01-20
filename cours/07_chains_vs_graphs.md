# ⚔️ Leçon 7 : Chains vs Graphs - L'Évolution de LangChain

## 🎯 Pourquoi ce Cours ?

Tu as appris deux syntaxes différentes dans ce parcours :
- **LCEL** (Chains) : `prompt | llm | parser`
- **LangGraph** : `StateGraph`, `add_node`, `add_edge`

Ce cours explique **quand utiliser quoi** et pourquoi LangChain a évolué.

---

## 🏗️ L'Analogie : Construction de Maisons

| Concept | Chains (LCEL) | Graphs (LangGraph) |
|---------|---------------|---------------------|
| **Type** | Chaîne de montage | Plan d'architecte |
| **Flux** | Toujours linéaire (A → B → C) | Flexible (boucles, conditions, branches) |
| **Contrôle** | Peu | Total |
| **Métaphore** | Train sur rails | GPS avec plusieurs routes |

> 💡 **LCEL** = "Fais A, puis B, puis C, toujours dans cet ordre"  
> 💡 **LangGraph** = "Si X alors fais A, sinon fais B, puis décide si on recommence"

---

## 🔗 Les Chains (LCEL) - Ce que tu Connais

### Syntaxe
```python
chain = prompt | llm | parser
result = chain.invoke({"question": "..."})
```

### Caractéristiques
- ✅ **Simple** et élégant
- ✅ Parfait pour les flux **linéaires**
- ✅ Facile à lire et comprendre
- ❌ Pas de boucles possibles
- ❌ Pas de conditions (if/else)
- ❌ Difficile de gérer un état complexe

### Cas d'Usage Idéaux
- Question → Réponse simple
- RAG basique (recherche → génération)
- Transformations de données en pipeline

### Schéma
```
Input → [Prompt] → [LLM] → [Parser] → Output
         ↓          ↓         ↓
       (linéaire, toujours le même chemin)
```

---

## 📊 Les Graphs (LangGraph) - La Nouvelle Approche

### Syntaxe
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(MyState)
graph.add_node("step_a", function_a)
graph.add_node("step_b", function_b)
graph.add_edge(START, "step_a")
graph.add_conditional_edges("step_a", decide_next)  # Conditions !
graph.add_edge("step_b", END)

app = graph.compile()
result = app.invoke({"input": "..."})
```

### Caractéristiques
- ✅ **Boucles** possibles (l'agent peut recommencer)
- ✅ **Conditions** (si X alors Y)
- ✅ **État** partagé entre les nœuds
- ✅ **Checkpointing** (sauvegarde/reprise)
- ❌ Plus verbeux
- ❌ Courbe d'apprentissage plus raide

### Cas d'Usage Idéaux
- **Agents** (décisions dynamiques)
- Workflows avec **boucles** (réessayer, valider)
- Applications avec **mémoire persistante**
- Multi-agents (plusieurs LLMs qui collaborent)

### Schéma
```
                    ┌──────────────┐
                    │              │
Input → [Node A] → [Condition] → [Node B] → Output
             ↑          │
             └──────────┘  (boucle possible !)
```

---

## 🔄 Le Cycle de Vie d'un Agent

C'est ICI que LangGraph brille. Un agent doit pouvoir :

```
1. Réfléchir     → "J'ai besoin d'infos"
2. Agir         → Appeler un outil
3. Observer     → Lire le résultat
4. Décider      → "Encore besoin d'infos ?" 
   ├── OUI → Retour à l'étape 1 (BOUCLE)
   └── NON → Répondre (FIN)
```

**Impossible avec LCEL** (pas de boucle).  
**Naturel avec LangGraph** (c'est fait pour ça).

---

## 📋 Tableau Comparatif Complet

| Critère | Chains (LCEL) | Graphs (LangGraph) |
|---------|---------------|---------------------|
| **Syntaxe** | `a \| b \| c` | `add_node`, `add_edge` |
| **Flux** | Linéaire uniquement | Linéaire + Boucles + Conditions |
| **État** | Passé d'un maillon à l'autre | État global partagé |
| **Mémoire** | `RunnableWithMessageHistory` | `MemorySaver` (checkpointer) |
| **Debugging** | Print dans les maillons | Visualisation du graphe possible |
| **Agents** | ❌ Limité | ✅ Conçu pour |
| **Complexité** | Faible | Moyenne à élevée |
| **Quand l'utiliser** | Pipelines simples | Workflows complexes |

---

## 🎓 Règle d'Or

```
┌─────────────────────────────────────────────────────────┐
│  "Commence avec LCEL. Passe à LangGraph quand tu as    │
│   besoin de boucles, conditions, ou d'un vrai agent."  │
└─────────────────────────────────────────────────────────┘
```

### Arbre de Décision

```
As-tu besoin de boucles ou conditions ?
├── NON → Utilise LCEL (Chains)
└── OUI → As-tu besoin d'un agent avec outils ?
          ├── OUI → LangGraph + create_react_agent
          └── NON → LangGraph + StateGraph custom
```

---

## 💻 Exemple Comparatif (`6_chains_vs_graphs.py`)

Le script montre le **même problème** résolu des deux façons :
1. Avec une Chain LCEL
2. Avec un Graph LangGraph

Tu verras que pour un flux simple, LCEL est plus concis.  
Mais dès qu'on ajoute une condition, LangGraph devient nécessaire.

---

## 🧩 Comment ils Cohabitent

Bonne nouvelle : **tu peux mixer les deux** !

```python
from langgraph.graph import StateGraph

# Une chaîne LCEL classique
chain = prompt | llm | parser

# Utilisée comme nœud dans un graphe
def node_with_chain(state):
    result = chain.invoke(state)
    return {"output": result}

graph.add_node("llm_step", node_with_chain)
```

> 💡 Les Chains sont des **briques** que tu peux utiliser **dans** un Graph !

---

## ✅ Points à Retenir

1. **LCEL (Chains)** = Simple, linéaire, élégant → pour les pipelines basiques
2. **LangGraph** = Flexible, boucles, état → pour les agents et workflows
3. **Pas de remplacement** : LangGraph **complète** LCEL, il ne le remplace pas
4. **Migration progressive** : Commence simple, complexifie si besoin
5. **Les agents modernes** utilisent LangGraph (comme `create_react_agent`)

---

## 📚 Récap du Parcours

| Leçon | Concept | Technologie |
|-------|---------|-------------|
| 1-3 | Bases, Prompts, Chains | LCEL |
| 4 | Mémoire | LCEL + LangGraph |
| 5 | RAG | LCEL |
| 6 | Agents | LangGraph |
| **7** | **Chains vs Graphs** | **Les deux !** |

---

## 🔜 Et Maintenant ?

Tu as maintenant une vision complète de l'écosystème LangChain moderne !  
Prochaine étape : créer une **interface utilisateur** avec Streamlit pour rendre tout ça interactif ! 🚀
