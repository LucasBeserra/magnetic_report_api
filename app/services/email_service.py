import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.core.security import create_email_token


def send_email(to_email: str, subject: str, body: str):
    """
    Envia email usando SMTP do Gmail.
    Retorna True se enviou com sucesso, False se deu erro.
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
        msg['To'] = to_email

        html_part = MIMEText(body, 'html')
        msg.attach(html_part)

        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email enviado para {to_email}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False


def send_verification_email(email: str, full_name: str):
    """Envia email de verificação para o usuário"""
    token = create_email_token(email, "verify")
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    subject = "Verifique seu email - Magnetic Report"
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background-color: #4F46E5; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 20px 0;
            }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Olá {full_name or 'Usuário'}!</h2>
            <p>Obrigado por se registrar no Magnetic Report.</p>
            <p>Para completar seu cadastro, clique no botão abaixo:</p>
            <a href="{verification_url}" class="button">Verificar Email</a>
            <p>Ou copie e cole este link no seu navegador:</p>
            <p style="word-break: break-all; color: #666;">{verification_url}</p>
            <p>Este link expira em {settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS} horas.</p>
            <div class="footer">
                <p>Se você não criou esta conta, ignore este email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(email, subject, body)


def send_password_reset_email(email: str, full_name: str):
    """Envia email de recuperação de senha"""
    token = create_email_token(email, "reset")
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    subject = "Recuperação de Senha - Magnetic Report"
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background-color: #DC2626; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 20px 0;
            }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Olá {full_name or 'Usuário'}!</h2>
            <p>Recebemos uma solicitação para redefinir sua senha.</p>
            <p>Para criar uma nova senha, clique no botão abaixo:</p>
            <a href="{reset_url}" class="button">Redefinir Senha</a>
            <p>Ou copie e cole este link no seu navegador:</p>
            <p style="word-break: break-all; color: #666;">{reset_url}</p>
            <p>Este link expira em {settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hora(s).</p>
            <div class="footer">
                <p>Se você não solicitou isto, ignore este email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(email, subject, body)