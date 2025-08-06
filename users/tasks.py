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


@shared_task
def send_password_reset_email(email, user_id):
    from .models import User
    from django.urls import reverse
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes, force_bytes

    logger.info(f"Starting password reset for {email} user_id {user_id}")
    try:
        user = User.objects.get(pk=user_id)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = (
            f"{settings.SITE_URL}{reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
        )
        subject = f"Password reset for {email}"
        message = f"""
            Hi {user.username}
            
            Please click the link below to reset your password:
            {reset_url}
            
        If you did not request this, please ignore this email.
        
        Best regards,
        Your Dev Forum
        """
        html_message = f"""
            <h1>Password Reset Request</h1>
            <p>Hi {user.username}</p>
            <p>Please click the link below to reset your password:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p>Best regards, Your Dev Forum</p>
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message
        )
        logger.info(f"Email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise
