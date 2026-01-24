# 📊 Leçon 9 : Structured Output - Forcer le Format de Sortie

## 🎯 Le Problème

Par défaut, un LLM retourne du **texte libre**. C'est bien pour un chatbot, mais problématique quand tu veux :
- Stocker les données dans une base
- Appeler une API avec des paramètres précis
- Traiter la réponse programmatiquement

```python
# ❌ Réponse texte libre (difficile à parser)
"Le produit coûte environ 29,99€ et il est disponible en bleu, rouge et vert."

# ✅ Réponse structurée (facile à utiliser)
{"prix": 29.99, "devise": "EUR", "couleurs": ["bleu", "rouge", "vert"]}
```

---

## 🧩 Les Solutions dans LangChain

| Méthode | Fiabilité | Complexité | Cas d'usage |
|---------|-----------|------------|-------------|
| `with_structured_output()` | ⭐⭐⭐ | Facile | **Recommandé** - Natif OpenAI |
| JSON Mode | ⭐⭐ | Facile | JSON simple sans schéma strict |
| Output Parsers | ⭐⭐ | Moyenne | Compatibilité avec anciens modèles |

---

## 🏆 Méthode Recommandée : `with_structured_output()`

### Comment ça marche ?

1. Tu définis un **schéma** avec Pydantic (une classe Python)
2. Tu attaches ce schéma au LLM avec `.with_structured_output()`
3. Le LLM est **forcé** de retourner un objet conforme au schéma

### Exemple Simple

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# 1. Définir le schéma avec Pydantic
class Personne(BaseModel):
    nom: str = Field(description="Le nom de la personne")
    age: int = Field(description="L'âge en années")
    ville: str = Field(description="La ville de résidence")

# 2. Attacher le schéma au LLM
llm = ChatOpenAI(model="gpt-4o-mini")
llm_structure = llm.with_structured_output(Personne)

# 3. Invoquer - Le résultat est un objet Personne !
result = llm_structure.invoke("Marie a 28 ans et habite à Lyon.")
print(result.nom)   # "Marie"
print(result.age)   # 28
print(result.ville) # "Lyon"
```

---

## 📐 Pydantic : Définir des Schémas

### Syntaxe de Base

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class MonSchema(BaseModel):
    # Champ obligatoire avec description
    nom: str = Field(description="Description pour le LLM")
    
    # Champ avec valeur par défaut
    score: int = Field(default=0, description="Score de 0 à 100")
    
    # Champ optionnel
    commentaire: Optional[str] = Field(default=None, description="Commentaire facultatif")
    
    # Liste de valeurs
    tags: List[str] = Field(description="Liste de tags")
```

### Types Supportés

| Type Python | Exemple | Description |
|-------------|---------|-------------|
| `str` | `"texte"` | Chaîne de caractères |
| `int` | `42` | Nombre entier |
| `float` | `3.14` | Nombre décimal |
| `bool` | `True` | Booléen |
| `List[T]` | `["a", "b"]` | Liste d'éléments |
| `Optional[T]` | `None` ou valeur | Champ facultatif |
| `Literal["a", "b"]` | `"a"` | Valeur parmi un choix |

---

## 🎯 Cas d'Usage Pratiques

### 1. Extraction d'Entités

```python
class EntitesExtraites(BaseModel):
    personnes: List[str] = Field(description="Noms des personnes mentionnées")
    lieux: List[str] = Field(description="Lieux géographiques mentionnés")
    dates: List[str] = Field(description="Dates mentionnées")
    
# "Marie et Jean sont allés à Paris le 15 janvier"
# → {"personnes": ["Marie", "Jean"], "lieux": ["Paris"], "dates": ["15 janvier"]}
```

### 2. Classification

```python
from typing import Literal

class ClassificationEmail(BaseModel):
    categorie: Literal["spam", "important", "normal"] = Field(description="Catégorie de l'email")
    urgence: int = Field(description="Niveau d'urgence de 1 à 5")
    resume: str = Field(description="Résumé en une phrase")
```

### 3. Analyse de Sentiment

```python
class AnalyseSentiment(BaseModel):
    sentiment: Literal["positif", "négatif", "neutre"] = Field(description="Sentiment global")
    score_confiance: float = Field(description="Score de confiance entre 0 et 1")
    emotions: List[str] = Field(description="Émotions détectées")
    explication: str = Field(description="Justification de l'analyse")
```

### 4. Génération de Données

```python
class Produit(BaseModel):
    nom: str
    description: str
    prix: float
    categories: List[str]

# "Génère un produit pour une boutique de sport"
# → Objet Produit complet et cohérent
```

---

## 🔄 Intégration avec les Chains

Tu peux utiliser `with_structured_output()` dans une chaîne LCEL :

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant qui analyse les avis clients."),
    ("human", "Analyse cet avis : {avis}")
])

class AnalyseAvis(BaseModel):
    note: int = Field(description="Note de 1 à 5")
    points_positifs: List[str]
    points_negatifs: List[str]
    recommande: bool

# Chaîne complète
chain = prompt | llm.with_structured_output(AnalyseAvis)

result = chain.invoke({"avis": "Super produit, livraison rapide, mais emballage abîmé."})
# result.note = 4
# result.points_positifs = ["Super produit", "livraison rapide"]
# result.points_negatifs = ["emballage abîmé"]
# result.recommande = True
```

---

## ⚠️ Points d'Attention

### 1. Les Descriptions sont Cruciales
```python
# ❌ Mauvais : pas de description
nom: str

# ✅ Bon : description claire
nom: str = Field(description="Le nom complet de la personne (prénom + nom)")
```

### 2. Modèles Compatibles
- ✅ GPT-4, GPT-4-turbo, GPT-4o, GPT-4o-mini
- ✅ GPT-3.5-turbo (récent)
- ⚠️ Modèles anciens : utiliser les Output Parsers à la place

### 3. Validation Automatique
Pydantic valide automatiquement les types. Si le LLM retourne un mauvais type, une erreur est levée.

### 4. Coût
Le structured output utilise le "function calling" d'OpenAI → légèrement plus de tokens.

---

## 📊 Comparaison des Méthodes

```
┌─────────────────────────────────────────────────────────────────┐
│  with_structured_output()                                       │
│  ✅ Fiable (function calling natif)                             │
│  ✅ Validation Pydantic                                         │
│  ✅ Simple à utiliser                                           │
│  ❌ Nécessite modèles récents                                   │
├─────────────────────────────────────────────────────────────────┤
│  JSON Mode (response_format={"type": "json_object"})            │
│  ✅ JSON garanti                                                │
│  ⚠️ Pas de schéma strict (peut manquer des champs)             │
│  ⚠️ Doit parser manuellement                                   │
├─────────────────────────────────────────────────────────────────┤
│  Output Parsers (PydanticOutputParser)                          │
│  ✅ Compatible tous modèles                                     │
│  ⚠️ Moins fiable (basé sur le prompt)                          │
│  ⚠️ Plus verbeux                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Points à Retenir

1. **`with_structured_output()`** = La méthode recommandée pour forcer un format
2. **Pydantic** = Définit le schéma avec des classes Python
3. **`Field(description=...)`** = Aide le LLM à comprendre chaque champ
4. **Types stricts** = `Literal["a", "b"]` pour limiter les choix
5. **Chaînable** = S'intègre parfaitement avec LCEL

---

## 🔜 Exercices Suggérés

1. Extraire les entités d'un article de presse
2. Classifier des tickets de support (bug, question, feature request)
3. Générer des fiches produit structurées à partir de descriptions libres

---

## 💻 Script Pratique

Voir `scripts/8_structured_output.py` pour des exemples complets et exécutables !
