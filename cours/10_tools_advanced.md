# 🔧 Leçon 10 : Tool Use Avancé - Créer des Outils Professionnels

## 🎯 Objectif

Dans la leçon sur les Agents, on a créé des outils simples avec `@tool`. Maintenant, on va voir comment créer des outils **robustes** et **professionnels** :

- Validation des entrées avec Pydantic
- Gestion des erreurs
- Outils asynchrones
- Outils avec état/contexte
- Bonnes pratiques de production

---

## 🧩 Les 3 Façons de Créer des Outils

| Méthode | Complexité | Cas d'usage |
|---------|------------|-------------|
| `@tool` | ⭐ Simple | Prototypes, outils simples |
| `StructuredTool` | ⭐⭐ Moyenne | Validation d'inputs, plus de contrôle |
| `BaseTool` (classe) | ⭐⭐⭐ Avancée | État, async, logique complexe |

---

## 1️⃣ Méthode Simple : Décorateur `@tool`

```python
from langchain_core.tools import tool

@tool
def calculer(expression: str) -> str:
    """Calcule une expression mathématique. Ex: '2 + 2' ou '10 * 5'"""
    return str(eval(expression))
```

### ✅ Avantages
- Ultra rapide à écrire
- La docstring devient la description

### ❌ Limites
- Pas de validation fine des inputs
- Difficile de gérer des erreurs proprement

---

## 2️⃣ Méthode Intermédiaire : `StructuredTool`

Permet de définir un **schéma Pydantic** pour les arguments :

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

# 1. Schéma des arguments
class RechercheArgs(BaseModel):
    query: str = Field(description="La recherche à effectuer")
    limit: int = Field(default=5, description="Nombre max de résultats")

# 2. La fonction
def rechercher(query: str, limit: int = 5) -> str:
    # ... logique de recherche ...
    return f"Résultats pour '{query}' (max {limit})"

# 3. Créer l'outil
outil_recherche = StructuredTool.from_function(
    func=rechercher,
    name="recherche_web",
    description="Recherche des informations sur le web",
    args_schema=RechercheArgs
)
```

### ✅ Avantages
- Validation automatique des arguments
- Valeurs par défaut
- Descriptions pour chaque argument

---

## 3️⃣ Méthode Avancée : Classe `BaseTool`

Pour un contrôle total : état, async, gestion d'erreurs personnalisée.

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class MonOutilArgs(BaseModel):
    param1: str = Field(description="Premier paramètre")
    param2: int = Field(default=10, description="Deuxième paramètre")

class MonOutilAvance(BaseTool):
    name: str = "mon_outil"
    description: str = "Description de ce que fait l'outil"
    args_schema: Type[BaseModel] = MonOutilArgs
    
    # État interne (optionnel)
    compteur: int = 0
    
    def _run(self, param1: str, param2: int = 10) -> str:
        """Exécution synchrone de l'outil."""
        self.compteur += 1  # On peut modifier l'état !
        return f"Résultat avec {param1} et {param2} (appel #{self.compteur})"
    
    async def _arun(self, param1: str, param2: int = 10) -> str:
        """Exécution asynchrone (optionnel)."""
        # Pour les opérations I/O (API, BDD, fichiers...)
        return await self._async_logic(param1, param2)
```

### ✅ Avantages
- État persistant entre les appels
- Support async natif
- Contrôle total sur l'exécution

---

## 🛡️ Gestion des Erreurs

### Méthode 1 : Return Error (Recommandé)

L'outil retourne un message d'erreur (l'agent peut réessayer) :

```python
@tool
def diviser(a: float, b: float) -> str:
    """Divise a par b."""
    if b == 0:
        return "Erreur : Division par zéro impossible. Réessaie avec b ≠ 0."
    return str(a / b)
```

### Méthode 2 : handle_tool_error

Configure le comportement global en cas d'exception :

```python
from langchain_core.tools import StructuredTool

def ma_fonction_risquee(x: int) -> str:
    if x < 0:
        raise ValueError("x doit être positif")
    return str(x * 2)

outil = StructuredTool.from_function(
    func=ma_fonction_risquee,
    name="doubler",
    description="Double un nombre positif",
    handle_tool_error=True  # Convertit les exceptions en messages
)
```

### Méthode 3 : Handler Personnalisé

```python
def mon_handler_erreur(error: Exception) -> str:
    return f"⚠️ L'outil a échoué : {str(error)}. Essaie autrement."

outil = StructuredTool.from_function(
    func=ma_fonction,
    handle_tool_error=mon_handler_erreur
)
```

---

## ⚡ Outils Asynchrones

Pour les opérations I/O (API, BDD, fichiers), l'async évite de bloquer :

```python
import httpx
from langchain_core.tools import tool

@tool
async def fetch_url(url: str) -> str:
    """Récupère le contenu d'une URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text[:500]  # Premiers 500 caractères
```

### Utilisation avec un Agent Async

```python
# L'agent doit être invoqué avec ainvoke()
result = await agent.ainvoke({"messages": [...]})
```

---

## 🎯 Bonnes Pratiques

### 1. Descriptions Claires et Complètes

```python
# ❌ Mauvais
@tool
def search(q: str) -> str:
    """Recherche."""
    ...

# ✅ Bon
@tool
def search_web(query: str) -> str:
    """Recherche des informations sur le web.
    
    Utilise cet outil quand tu as besoin d'informations actuelles
    ou de faits que tu ne connais pas.
    
    Args:
        query: La recherche à effectuer, sois précis et concis.
               Exemple: "météo Paris aujourd'hui" ou "prix iPhone 15"
    
    Returns:
        Les résultats de recherche formatés.
    """
    ...
```

### 2. Validation Stricte des Inputs

```python
from pydantic import BaseModel, Field, field_validator

class EnvoiEmailArgs(BaseModel):
    destinataire: str = Field(description="Adresse email du destinataire")
    sujet: str = Field(description="Sujet de l'email")
    corps: str = Field(description="Contenu de l'email")
    
    @field_validator('destinataire')
    @classmethod
    def valider_email(cls, v):
        if '@' not in v:
            raise ValueError("L'adresse email doit contenir @")
        return v
```

### 3. Limiter la Taille des Retours

```python
@tool
def lire_fichier(chemin: str) -> str:
    """Lit le contenu d'un fichier."""
    with open(chemin) as f:
        contenu = f.read()
    
    # Limiter pour ne pas exploser le contexte !
    if len(contenu) > 5000:
        return contenu[:5000] + "\n... [contenu tronqué]"
    return contenu
```

### 4. Logs et Traçabilité

```python
import logging

logger = logging.getLogger(__name__)

@tool
def action_importante(param: str) -> str:
    """Effectue une action importante."""
    logger.info(f"Action déclenchée avec param={param}")
    
    try:
        result = faire_action(param)
        logger.info(f"Action réussie: {result}")
        return result
    except Exception as e:
        logger.error(f"Action échouée: {e}")
        return f"Erreur: {e}"
```

---

## 🔄 Outils avec État

Parfois, un outil doit se souvenir de ses appels précédents :

```python
class OutilAvecHistorique(BaseTool):
    name: str = "recherche_avec_cache"
    description: str = "Recherche avec cache des résultats précédents"
    
    # État : cache des recherches
    cache: dict = {}
    
    def _run(self, query: str) -> str:
        # Vérifier le cache
        if query in self.cache:
            return f"[CACHE] {self.cache[query]}"
        
        # Sinon, faire la recherche
        result = self._faire_recherche(query)
        self.cache[query] = result
        return result
```

---

## 📊 Tableau Récapitulatif

| Aspect | `@tool` | `StructuredTool` | `BaseTool` |
|--------|---------|------------------|------------|
| Facilité | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Validation | Basique | Pydantic | Pydantic |
| État | ❌ | ❌ | ✅ |
| Async | Via `async def` | Config | `_arun()` |
| Erreurs | Try/except | `handle_tool_error` | Custom |

---

## ✅ Points à Retenir

1. **`@tool`** = Rapide pour prototyper
2. **`StructuredTool`** = Validation Pydantic des arguments
3. **`BaseTool`** = Contrôle total (état, async, custom)
4. **Descriptions** = Cruciales pour que l'agent choisisse le bon outil
5. **Erreurs** = Retourner un message plutôt que lever une exception
6. **Async** = Obligatoire pour les I/O en production

---

## 💻 Script Pratique

Voir `scripts/9_tools_advanced.py` pour des exemples complets !
