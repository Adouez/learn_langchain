"""
📧 Outil Email - Envoi de messages
==================================

Cet outil permet d'envoyer des emails.
Par défaut, il fonctionne en mode SIMULATION (pas d'envoi réel).

Pour activer l'envoi réel, configurez les variables d'environnement :
- SMTP_SERVER
- SMTP_PORT
- SMTP_USER
- SMTP_PASSWORD
"""

import os
from langchain_core.tools import tool

# Configuration SMTP (optionnel)
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT", "587")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Mode simulation par défaut
SIMULATION_MODE = not all([SMTP_SERVER, SMTP_USER, SMTP_PASSWORD])


@tool
def envoyer_email(destinataire: str, sujet: str, message: str) -> str:
    """Utile pour envoyer un email à quelqu'un.
    Peut servir à envoyer des rapports, des notifications, ou des résumés d'analyse.
    Entrée : destinataire (email), sujet, et corps du message."""
    
    # Validation basique
    if "@" not in destinataire:
        return "❌ Erreur : L'adresse email du destinataire semble invalide (pas de @)."
    
    if not sujet.strip():
        return "❌ Erreur : Le sujet de l'email ne peut pas être vide."
    
    if not message.strip():
        return "❌ Erreur : Le message ne peut pas être vide."
    
    if SIMULATION_MODE:
        # Mode simulation - on affiche ce qui SERAIT envoyé
        return f"""📧 **EMAIL SIMULÉ** (mode test)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📬 À : {destinataire}
📝 Sujet : {sujet}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Cet email n'a PAS été envoyé (mode simulation).
Pour activer l'envoi réel, configurez SMTP_SERVER, SMTP_USER et SMTP_PASSWORD dans .env"""
    
    else:
        # Mode réel - envoi via SMTP
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg["From"] = SMTP_USER
            msg["To"] = destinataire
            msg["Subject"] = sujet
            msg.attach(MIMEText(message, "plain", "utf-8"))
            
            with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            
            return f"✅ Email envoyé avec succès à {destinataire} !"
        
        except Exception as e:
            return f"❌ Erreur lors de l'envoi de l'email : {e}"
