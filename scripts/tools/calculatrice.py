"""
🧮 Outils utilitaires - Calculatrice et Date
============================================
"""

from datetime import datetime
from langchain_core.tools import tool


@tool
def calculatrice(expression: str) -> str:
    """Utile pour faire des calculs mathématiques : additions, soustractions, 
    multiplications, divisions, pourcentages, moyennes, puissances.
    Exemples : '(80 + 75 + 90) / 3' pour une moyenne, '85 - 70' pour une différence, '2 ** 10' pour une puissance.
    Entrée : une expression mathématique valide en Python."""
    
    try:
        # Sécurité basique : n'autoriser que certains caractères
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "Erreur : expression contient des caractères non autorisés. Utilisez uniquement des chiffres et opérateurs (+, -, *, /, **, ())"
        
        resultat = eval(expression)
        
        # Formatage intelligent du résultat
        if isinstance(resultat, float):
            if resultat == int(resultat):
                resultat = int(resultat)
            else:
                resultat = round(resultat, 2)
        
        return f"✅ Résultat : {expression} = {resultat}"
    
    except ZeroDivisionError:
        return "❌ Erreur : Division par zéro impossible."
    except Exception as e:
        return f"❌ Erreur de calcul : {e}"


@tool
def date_actuelle() -> str:
    """Utile pour connaître la date et l'heure actuelles.
    Permet de contextualiser les analyses, calculer des durées, ou simplement répondre à 'quelle heure est-il ?'.
    Aucune entrée requise."""
    
    now = datetime.now()
    
    # Traduction française des jours et mois
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", 
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    
    jour_nom = jours[now.weekday()]
    mois_nom = mois[now.month - 1]
    
    return f"📅 Nous sommes le {jour_nom} {now.day} {mois_nom} {now.year} à {now.strftime('%H:%M')}."
