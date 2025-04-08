from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.db import models
from join.settings import TOKEN_EXPIRATION_TIME
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExpiringToken(Token):
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        if self.expires_at is None:
            return True
        return self.expires_at < timezone.now()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + TOKEN_EXPIRATION_TIME
        super().save(*args, **kwargs)

class ExpiringTokenAuthentication(TokenAuthentication):
    model = ExpiringToken

    def authenticate_credentials(self, key):
        token = self.model.objects.filter(key=key).first()

        if not token:
            raise AuthenticationFailed({"error": "Invalid token."})

        if token.is_expired():
            token.delete()
            raise AuthenticationFailed({"error": "Token expired."})

        return (token.user, token)