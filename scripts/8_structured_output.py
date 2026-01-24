"""
📊 Leçon 9 : Structured Output - Forcer le Format de Sortie
============================================================

Ce script montre comment forcer le LLM à retourner des données
structurées (JSON/objets Python) au lieu de texte libre.

Très utile pour :
- APIs qui attendent des données formatées
- Stockage en base de données
- Traitement automatisé des réponses
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

load_dotenv()

# Le modèle (gpt-4o-mini est économique et supporte bien le structured output)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ═══════════════════════════════════════════════════════════════════════════
# 📌 EXEMPLE 1 : Extraction Simple
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("📌 EXEMPLE 1 : Extraction d'informations sur une personne")
print("=" * 70)


class Personne(BaseModel):
    """Informations sur une personne extraites d'un texte."""
    nom: str = Field(description="Le prénom et nom de la personne")
    age: int = Field(description="L'âge de la personne en années")
    ville: str = Field(description="La ville où habite la personne")
    profession: Optional[str] = Field(default=None, description="La profession si mentionnée")


# Attacher le schéma au LLM
llm_personne = llm.with_structured_output(Personne)

texte = "Marie Dupont a 32 ans. Elle travaille comme développeuse à Bordeaux."

print(f"\n📝 Texte : \"{texte}\"\n")
result = llm_personne.invoke(f"Extrais les informations de ce texte : {texte}")

print(f"✅ Résultat structuré :")
print(f"   - Nom : {result.nom}")
print(f"   - Âge : {result.age}")
print(f"   - Ville : {result.ville}")
print(f"   - Profession : {result.profession}")
print(f"\n   📦 Type de l'objet : {type(result).__name__}")


# ═══════════════════════════════════════════════════════════════════════════
# 📌 EXEMPLE 2 : Classification avec Choix Limités
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📌 EXEMPLE 2 : Classification de tickets support")
print("=" * 70)


class TicketClassification(BaseModel):
    """Classification d'un ticket de support client."""
    categorie: Literal["bug", "question", "feature_request", "autre"] = Field(
        description="La catégorie du ticket"
    )
    urgence: Literal["basse", "moyenne", "haute", "critique"] = Field(
        description="Le niveau d'urgence"
    )
    produit: str = Field(description="Le produit ou service concerné")
    resume: str = Field(description="Résumé du problème en une phrase")


llm_ticket = llm.with_structured_output(TicketClassification)

tickets = [
    "L'application crash quand je clique sur 'Sauvegarder'. Impossible de travailler !",
    "Ce serait cool d'avoir un mode sombre dans l'interface.",
    "Comment exporter mes données en CSV ?"
]

for i, ticket in enumerate(tickets, 1):
    print(f"\n📩 Ticket {i} : \"{ticket}\"")
    result = llm_ticket.invoke(f"Classifie ce ticket de support : {ticket}")
    print(f"   📁 Catégorie : {result.categorie}")
    print(f"   ⚡ Urgence : {result.urgence}")
    print(f"   🏷️ Produit : {result.produit}")
    print(f"   📝 Résumé : {result.resume}")


# ═══════════════════════════════════════════════════════════════════════════
# 📌 EXEMPLE 3 : Extraction de Listes
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📌 EXEMPLE 3 : Extraction d'entités nommées")
print("=" * 70)


class EntitesExtraites(BaseModel):
    """Entités extraites d'un texte."""
    personnes: List[str] = Field(description="Noms des personnes mentionnées")
    organisations: List[str] = Field(description="Noms des entreprises ou organisations")
    lieux: List[str] = Field(description="Lieux géographiques (villes, pays, etc.)")
    dates: List[str] = Field(description="Dates ou périodes mentionnées")


llm_entites = llm.with_structured_output(EntitesExtraites)

article = """
Le PDG d'Apple, Tim Cook, a annoncé lors de la conférence de San Francisco 
le 15 mars 2024 un partenariat stratégique avec Microsoft. Satya Nadella, 
CEO de Microsoft, était présent à Seattle pour la signature de l'accord.
"""

print(f"\n📰 Article :\n{article}")
result = llm_entites.invoke(f"Extrais les entités de ce texte : {article}")

print(f"\n✅ Entités extraites :")
print(f"   👤 Personnes : {result.personnes}")
print(f"   🏢 Organisations : {result.organisations}")
print(f"   📍 Lieux : {result.lieux}")
print(f"   📅 Dates : {result.dates}")


# ═══════════════════════════════════════════════════════════════════════════
# 📌 EXEMPLE 4 : Avec une Chaîne LCEL
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📌 EXEMPLE 4 : Analyse de sentiment avec chaîne LCEL")
print("=" * 70)


class AnalyseSentiment(BaseModel):
    """Analyse de sentiment d'un texte."""
    sentiment: Literal["très_positif", "positif", "neutre", "négatif", "très_négatif"] = Field(
        description="Le sentiment global du texte"
    )
    score_confiance: float = Field(
        description="Score de confiance entre 0.0 et 1.0"
    )
    emotions: List[str] = Field(
        description="Liste des émotions détectées (joie, colère, tristesse, etc.)"
    )
    mots_cles: List[str] = Field(
        description="Mots ou expressions clés qui justifient l'analyse"
    )


# Chaîne LCEL complète : Prompt → LLM avec structure
prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un expert en analyse de sentiment.
Analyse le texte fourni et extrais le sentiment, les émotions et les mots clés.
Sois précis dans ton évaluation."""),
    ("human", "{texte}")
])

chain_sentiment = prompt | llm.with_structured_output(AnalyseSentiment)

avis_clients = [
    "Produit incroyable ! Livraison ultra rapide, je suis vraiment satisfait !",
    "Bof, ça fait le job mais sans plus. Le prix est correct.",
    "Catastrophe totale. Produit cassé à l'arrivée et service client inexistant !"
]

for avis in avis_clients:
    print(f"\n💬 Avis : \"{avis}\"")
    result = chain_sentiment.invoke({"texte": avis})
    
    # Emoji selon le sentiment
    emoji_map = {
        "très_positif": "🌟",
        "positif": "😊",
        "neutre": "😐",
        "négatif": "😞",
        "très_négatif": "😡"
    }
    emoji = emoji_map.get(result.sentiment, "❓")
    
    print(f"   {emoji} Sentiment : {result.sentiment} (confiance: {result.score_confiance:.0%})")
    print(f"   💭 Émotions : {', '.join(result.emotions)}")
    print(f"   🔑 Mots clés : {', '.join(result.mots_cles)}")


# ═══════════════════════════════════════════════════════════════════════════
# 📌 EXEMPLE 5 : Génération de Données Structurées
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📌 EXEMPLE 5 : Génération de fiche produit")
print("=" * 70)


class FicheProduit(BaseModel):
    """Fiche produit complète pour un e-commerce."""
    nom: str = Field(description="Nom commercial du produit")
    description_courte: str = Field(description="Description en une phrase (max 100 caractères)")
    description_longue: str = Field(description="Description détaillée (2-3 phrases)")
    prix_suggere: float = Field(description="Prix suggéré en euros")
    categories: List[str] = Field(description="Catégories du produit (2-3 max)")
    points_forts: List[str] = Field(description="3 points forts principaux")
    public_cible: str = Field(description="Le public cible pour ce produit")


llm_produit = llm.with_structured_output(FicheProduit)

demande = "Génère une fiche produit pour des écouteurs bluetooth sportifs haut de gamme"

print(f"\n📝 Demande : \"{demande}\"\n")
result = llm_produit.invoke(demande)

print(f"🎧 {result.nom}")
print(f"   💰 Prix : {result.prix_suggere}€")
print(f"   📝 {result.description_courte}")
print(f"\n   📖 Description :")
print(f"   {result.description_longue}")
print(f"\n   📁 Catégories : {', '.join(result.categories)}")
print(f"   🎯 Public cible : {result.public_cible}")
print(f"\n   ✨ Points forts :")
for i, point in enumerate(result.points_forts, 1):
    print(f"      {i}. {point}")


# ═══════════════════════════════════════════════════════════════════════════
# 📚 RÉCAPITULATIF
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📚 RÉCAPITULATIF")
print("=" * 70)
print("""
🎯 Ce que tu as appris :

1. Pydantic BaseModel → Définir des schémas de données
2. Field(description=...) → Guider le LLM sur chaque champ
3. with_structured_output() → Forcer le format de sortie
4. Literal["a", "b"] → Limiter les choix possibles
5. List[str] → Extraire des listes d'éléments
6. Optional[T] → Champs facultatifs

💡 Cas d'usage courants :
   - Extraction d'entités (NER)
   - Classification automatique
   - Analyse de sentiment
   - Génération de données formatées
   - APIs qui retournent du JSON

⚠️ Rappel : Les descriptions Field() sont CRUCIALES pour la qualité !
""")
