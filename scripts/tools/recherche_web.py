"""
🌐 Outil Recherche Web - DuckDuckGo
===================================

Utilise DuckDuckGo pour faire des recherches web gratuites (pas de clé API requise).
"""

from langchain_core.tools import tool

# On essaie d'importer ddgs (anciennement duckduckgo-search), sinon on fait un fallback
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


@tool
def recherche_web(query: str) -> str:
    """Utile pour rechercher des informations récentes sur Internet.
    Permet de trouver des actualités, des définitions, des informations sur des entreprises, 
    des technologies, ou tout sujet nécessitant des données à jour.
    Entrée : une requête de recherche en français ou anglais."""
    
    if not DDGS_AVAILABLE:
        return """⚠️ L'outil de recherche web n'est pas disponible.
Pour l'activer, installez le package : pip install ddgs

En attendant, je ne peux répondre qu'avec mes connaissances existantes ou les documents Clinitex."""
    
    try:
        # Créer une instance DuckDuckGo
        ddgs = DDGS()
        
        # Rechercher (max 5 résultats)
        results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return f"🔍 Aucun résultat trouvé pour : '{query}'"
        
        # Formater les résultats
        output = f"🌐 Résultats de recherche pour '{query}' :\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "Sans titre")
            body = result.get("body", "Pas de description")
            href = result.get("href", "")
            
            output += f"**{i}. {title}**\n"
            output += f"   {body[:200]}...\n"
            output += f"   🔗 {href}\n\n"
        
        return output
    
    except Exception as e:
        return f"❌ Erreur lors de la recherche web : {e}"
