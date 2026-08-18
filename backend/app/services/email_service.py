"""Entrega de e-mails transacionais com modo local seguro para desenvolvimento."""

import logging
import smtplib
from email.message import EmailMessage

from app.config import settings

logger = logging.getLogger(__name__)


def enviar_redefinicao_senha(destinatario: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL.rstrip('/')}/redefinir-senha?token={token}"
    if settings.EMAIL_MODE == "console":
        logger.info("Redefinição solicitada para %s; configure SMTP para entrega real.", destinatario)
        return

    if settings.EMAIL_MODE != "smtp":
        raise RuntimeError("EMAIL_MODE deve ser 'console' ou 'smtp'.")

    mensagem = EmailMessage()
    mensagem["Subject"] = "Redefinição de senha — Núcleo AI"
    mensagem["From"] = settings.EMAIL_FROM
    mensagem["To"] = destinatario
    mensagem.set_content(
        "Recebemos uma solicitação para redefinir sua senha. "
        f"Use este link em até {settings.PASSWORD_RESET_EXPIRE_MINUTES} minutos: {link}"
    )
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as servidor:
        if settings.SMTP_STARTTLS:
            servidor.starttls()
        if settings.SMTP_USERNAME:
            servidor.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        servidor.send_message(mensagem)


def enviar_convite(destinatario: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL.rstrip('/')}/aceitar-convite?token={token}"
    if settings.EMAIL_MODE == "console":
        logger.info("Convite de desenvolvimento para %s: %s", destinatario, link)
        return
    if settings.EMAIL_MODE != "smtp":
        raise RuntimeError("EMAIL_MODE deve ser 'console' ou 'smtp'.")
    mensagem = EmailMessage()
    mensagem["Subject"] = "Convite para a Núcleo AI"
    mensagem["From"] = settings.EMAIL_FROM
    mensagem["To"] = destinatario
    mensagem.set_content(
        f"Você foi convidado para a Núcleo AI. Aceite em até {settings.INVITE_EXPIRE_DAYS} dias: {link}"
    )
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as servidor:
        if settings.SMTP_STARTTLS:
            servidor.starttls()
        if settings.SMTP_USERNAME:
            servidor.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        servidor.send_message(mensagem)
