from celery import shared_task
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(email, username):
    subject = "Welcome Dev Forum!"
    message = f"""
    Hi {username},

    Thank you for enjoying Dev Forum! We're excited to have you with us.
    Explore our features and enjoy the experience.

    Best regards,
    Your Dev Forum
    """
    html_message = f"""
        <h1>Welcome Dev Forum!</h1>
        <p>Hello, {username}!</p>
        <p>Thank you for visiting our forum. I hope you enjoy it.!</p>
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message
        )
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise


