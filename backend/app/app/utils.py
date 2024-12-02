import base64
import secrets
import smtplib
import string
from datetime import datetime, timezone
from email.headerregistry import Address
from email.message import EmailMessage
from typing import Any

# from emails.template import JinjaTemplate

from app.config import settings


def send_email(
    *,
    email_to: str,
    environment: dict[str, Any],
    subject_template: str = "",
    html_template: str = "",
) -> dict[str, dict[str, Any] | str]:
    msg = EmailMessage()
    msg["subject"] = subject_template
    msg['From'] = Address(
        settings.EMAILS_FROM_DISPLAY_NAME,
        settings.EMAILS_FROM_USERNAME,
        settings.EMAILS_FROM_DOMAIN
    )
    msg["to"] = email_to
    msg.set_content(environment["link"], charset='utf-8', cte='7bit')

    with smtplib.SMTP(host="localhost", port=1025) as server:
        server.send_message(msg)

    # return {
    #     "To": email_to,
    #     "Subject": subject_template,
    #     "Message": environment
    # }
# def send_email(
#     email_to: str,
#     subject_template: str = "",
#     html_template: str = "",
#     environment: Dict[str, Any] = {},
# ) -> None:
#     assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
#     message = emails.Message(
#         subject=JinjaTemplate(subject_template),
#         html=JinjaTemplate(html_template),
#         mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
#     )
#     smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     if settings.SMTP_USER:
#         smtp_options["user"] = settings.SMTP_USER
#     if settings.SMTP_PASSWORD:
#         smtp_options["password"] = settings.SMTP_PASSWORD
#     response = message.send(to=email_to, render=environment, smtp=smtp_options)
#     logging.info(f"send email result: {response}")


# def send_test_email(email_to: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - Test email"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
#         template_str = f.read()
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={"project_name": settings.PROJECT_NAME, "email": email_to},
#     )


def send_reset_password_email(email_to: str, email: str, nonce: str) -> str:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    # with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
    #     template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}auth/reset-password?nonce={nonce}"
    print(f"Sending email reset password: {link}", nonce)
    send_email(
        email_to=email_to,
        subject_template=subject,
        # html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return nonce


def send_account_activation_email(email_to: str, email: str, nonce: str) -> str:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Account activation for user {email}"
    # with open(Path(settings.EMAIL_TEMPLATES_DIR) / "account_activation.html") as f:
    #     template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}auth/activate?nonce={nonce}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        # html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_ACTIVATION_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return nonce


def generate_nonce() -> str:
    # 24 8-bits utf-8 characters gives 4 * (24/3) 6-bits base64 encoded characters
    # token length will be 192 bits once encoded
    nonce = ''.join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(24)
    )
    return base64.urlsafe_b64encode(nonce.encode()).decode()


def verify_password_reset_token(token: str) -> str | None:
    # To be deleted and replaced by verify_nonce
    return None


def verify_nonce(
        nonce: str,
        expected_nonce: str,
        issued_at: int,
        threshold_hours: int,
) -> bool:
    timestamp = int(datetime.timestamp(datetime.now(timezone.utc)))
    too_old = timestamp - issued_at > threshold_hours * 3600 + 60
    return not too_old and nonce == expected_nonce


def verify_password_reset_nonce(
        nonce: str,
        expected_nonce: str,
        issued_at: int
) -> bool:
    return verify_nonce(
        nonce, expected_nonce, issued_at, settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS
    )


def verify_account_activation_nonce(
        nonce: str,
        expected_nonce: str,
        issued_at: int
) -> bool:
    return verify_nonce(
        nonce, expected_nonce, issued_at, settings.EMAIL_ACTIVATION_TOKEN_EXPIRE_HOURS
    )
