import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def enviar_email(destinatario: str, assunto: str, corpo_html: str):
    REMETENTE = os.getenv("REMETENTE")
    SENHA_EMAIL = os.getenv("SENHA_EMAIL")

    if not REMETENTE or not SENHA_EMAIL:
        logger.error("Variáveis de ambiente REMETENTE ou SENHA_EMAIL não configuradas.")
        raise ValueError("Configurações de e-mail ausentes.")

    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = assunto
    mensagem["From"] = REMETENTE
    mensagem["To"] = destinatario

    parte_html = MIMEText(corpo_html, "html")
    mensagem.attach(parte_html)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as servidor:
            servidor.login(REMETENTE, SENHA_EMAIL)
            servidor.sendmail(REMETENTE, destinatario, mensagem.as_string())
            logger.info(f"E-mail enviado com sucesso para {destinatario}")
    except smtplib.SMTPException as e:
        logger.exception(f"Erro SMTP ao enviar e-mail para {destinatario}: {e}")
    except Exception as e:
        logger.exception(f"Erro inesperado ao enviar e-mail para {destinatario}: {e}")
