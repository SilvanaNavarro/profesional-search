import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", SMTP_USER)


def is_email_configured() -> bool:
    return all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL])


def send_email(to_email: str, subject: str, body: str) -> bool:
    if not is_email_configured():
        logging.warning("Email service is not configured. Cannot send email.")
        return False
    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            logging.info(f"Email sent successfully to {to_email}")
            return True
    except smtplib.SMTPAuthenticationError as e:
        logging.exception(f"SMTP Authentication Error: {e}. Check credentials.")
    except smtplib.SMTPServerDisconnected as e:
        logging.exception(f"SMTP Server Disconnected: {e}. Check server/port.")
    except Exception as e:
        logging.exception(f"Failed to send email to {to_email}: {e}")
    return False


def send_verification_email(to_email: str, code: str) -> bool:
    subject = "Tu C\x0800f3digo de Verificaci\x0800f3n para ProfessionalBook"
    body = f'\n    <html>\n        <body style="font-family: Arial, sans-serif; text-align: center; color: #333;">\n            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">\n                <h1 style="color: #f97316;">ProfessionalBook</h1>\n                <h2>Confirma tu direcci\x0800f3n de correo electr\x0800f3nico</h2>\n                <p>Gracias por registrarte. Usa el siguiente c\x0800f3digo para verificar tu cuenta:</p>\n                <p style="font-size: 24px; font-weight: bold; letter-spacing: 5px; background-color: #f0f0f0; padding: 15px; border-radius: 5px;">{code}</p>\n                <p>Este c\x0800f3digo expirar\x0800e1 en 10 minutos. Si no solicitaste este c\x0800f3digo, puedes ignorar este mensaje.</p>\n            </div>\n        </body>\n    </html>\n    '
    return send_email(to_email, subject, body)


def send_booking_confirmation_email(
    to_email: str, user_name: str, professional_name: str, date: str, time: str
) -> bool:
    subject = "¡Tu cita en ProfessionalBook ha sido confirmada!"
    body = f'\n    <html>\n        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">\n            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 30px; border-radius: 12px; background-color: #f9f9f9;">\n                <h1 style="color: #f97316; text-align: center;">ProfessionalBook</h1>\n                <h2 style="color: #333; text-align: center;">Confirmación de Cita</h2>\n                <p>Hola {user_name},</p>\n                <p>¡Buenas noticias! Tu pago ha sido procesado exitosamente y tu cita ha sido confirmada.</p>\n                <div style="background-color: #fff; padding: 20px; border-radius: 8px; border: 1px solid #eee; margin-top: 20px;">\n                    <h3 style="color: #f97316; margin-top: 0;">Detalles de la Reserva:</h3>\n                    <p><strong>Profesional:</strong> {professional_name}</p>\n                    <p><strong>Fecha:</strong> {date}</p>\n                    <p><strong>Hora:</strong> {time}</p>\n                </div>\n                <p style="margin-top: 25px;">Recuerda ser puntual. Si necesitas reprogramar, por favor contacta al profesional directamente.</p>\n                <p>Gracias por usar ProfessionalBook.</p>\n                <p style="text-align: center; font-size: 12px; color: #999; margin-top: 30px;">\n                    Este es un correo automático, por favor no respondas a este mensaje.\n                </p>\n            </div>\n        </body>\n    </html>\n    '
    return send_email(to_email, subject, body)