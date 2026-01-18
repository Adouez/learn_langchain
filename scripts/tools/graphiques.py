"""
📊 Outil Graphiques - Génération de visualisations
==================================================

Génère des graphiques avec matplotlib.
Les graphiques sont sauvegardés dans le dossier 'outputs/'.
"""

import os
import json
from datetime import datetime
from langchain_core.tools import tool

# On essaie d'importer matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Mode non-interactif pour serveur
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def _ensure_output_dir():
    """Crée le dossier outputs/ s'il n'existe pas."""
    output_dir = "scripts/outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


@tool
def generer_graphique(type_graphique: str, donnees: str, titre: str) -> str:
    """Utile pour créer des graphiques et visualisations.
    
    Types supportés : 'barres', 'camembert', 'ligne'
    
    Format des données (JSON) :
    - Pour barres/ligne : {"labels": ["A", "B", "C"], "valeurs": [10, 20, 30]}
    - Pour camembert : {"labels": ["A", "B"], "valeurs": [60, 40]}
    
    Exemple : type='barres', donnees='{"labels": ["Antoine", "Nicolas"], "valeurs": [85, 78]}', titre='Scores de maturité'
    
    Entrée : type_graphique, donnees (format JSON), titre du graphique."""
    
    if not MATPLOTLIB_AVAILABLE:
        return """⚠️ L'outil de graphiques n'est pas disponible.
Pour l'activer, installez matplotlib : pip install matplotlib"""
    
    try:
        # Parser les données JSON
        data = json.loads(donnees)
        labels = data.get("labels", [])
        valeurs = data.get("valeurs", [])
        
        if not labels or not valeurs:
            return "❌ Erreur : Les données doivent contenir 'labels' et 'valeurs'."
        
        if len(labels) != len(valeurs):
            return "❌ Erreur : Le nombre de labels doit correspondre au nombre de valeurs."
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Couleurs modernes
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4']
        
        if type_graphique.lower() in ['barres', 'bar', 'barre']:
            bars = ax.bar(labels, valeurs, color=colors[:len(labels)], edgecolor='white', linewidth=1.2)
            # Ajouter les valeurs sur les barres
            for bar, val in zip(bars, valeurs):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                       str(val), ha='center', va='bottom', fontweight='bold')
        
        elif type_graphique.lower() in ['camembert', 'pie', 'cercle']:
            ax.pie(valeurs, labels=labels, colors=colors[:len(labels)], 
                   autopct='%1.1f%%', startangle=90, explode=[0.02]*len(labels))
            ax.axis('equal')
        
        elif type_graphique.lower() in ['ligne', 'line', 'courbe']:
            ax.plot(labels, valeurs, marker='o', linewidth=2, markersize=8, color=colors[0])
            ax.fill_between(labels, valeurs, alpha=0.3, color=colors[0])
            ax.grid(True, alpha=0.3)
        
        else:
            return f"❌ Type de graphique '{type_graphique}' non reconnu. Utilisez : 'barres', 'camembert', ou 'ligne'."
        
        ax.set_title(titre, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        # Sauvegarder le graphique
        output_dir = _ensure_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graphique_{type_graphique}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return f"""✅ Graphique généré avec succès !

📊 Type : {type_graphique}
📝 Titre : {titre}
📁 Fichier : {filepath}

Le graphique a été sauvegardé. Tu peux l'ouvrir pour le visualiser."""
    
    except json.JSONDecodeError:
        return """❌ Erreur : Format JSON invalide pour les données.
Exemple correct : {"labels": ["A", "B", "C"], "valeurs": [10, 20, 30]}"""
    
    except Exception as e:
        return f"❌ Erreur lors de la génération du graphique : {e}"
