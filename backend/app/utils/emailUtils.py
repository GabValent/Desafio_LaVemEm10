import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def enviar_email(destinatario: str, assunto: str, corpo_html: str):

    REMETENTE = os.getenv("REMETENTE")
    SENHA_EMAIL = os.getenv("SENHA_EMAIL")


    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = assunto
    mensagem["From"] = REMETENTE
    mensagem["To"] = destinatario

    parte_html = MIMEText(corpo_html, "html")
    mensagem.attach(parte_html)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(REMETENTE, SENHA_EMAIL)
            servidor.sendmail(REMETENTE, destinatario, mensagem.as_string())
            print(f"[✓] Email enviado com sucesso para {destinatario}")
    except Exception as e:
        print(f"[x] Erro ao enviar e-mail para {destinatario}: {e}")
