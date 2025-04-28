import pytest
from unittest.mock import patch
from app.Services.enviarEmail import enviar_email

@patch("app.Services.enviarEmail.smtplib.SMTP_SSL")
def test_enviar_email(mock_smtp):
    mock_smtp.return_value.__enter__.return_value.sendmail.return_value = None
    destinatario = "destinatario@dominio.com"
    assunto = "Assunto do E-mail"
    corpo_html = "<html><body><p>Corpo do e-mail</p></body></html>"
    
    enviar_email(destinatario, assunto, corpo_html)
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()
