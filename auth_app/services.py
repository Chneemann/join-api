from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model


User = get_user_model()

def create_password_reset_link(request, user, token):
    """Creates the password reset link."""
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    return f"{request.META.get('HTTP_ORIGIN', '')}/pw-reset/{uidb64}/{token}/"

def send_password_reset_email(user, token, reset_link):
    """Sends the password reset e-mail."""
    subject = 'Password Reset Request'
    message = render_to_string('emails/password_reset_email.html', {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'token': token,
        'reset_link': reset_link,
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email, html_message=message)
    
def verify_password_reset_token(uidb64, token):
    """Verifies the password reset token."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return user
    return None

def set_user_password(user, password):
    """Sets the new password for the user."""
    user.set_password(password)
    user.save()