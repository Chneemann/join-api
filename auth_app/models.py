from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.db import models
from join.settings import TOKEN_EXPIRATION_TIME

class ExpiringToken(Token):
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + TOKEN_EXPIRATION_TIME
        super().save(*args, **kwargs)