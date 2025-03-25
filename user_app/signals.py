from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def clear_user_cache(sender, instance, **kwargs):
    """Invalidate cache for the affected user"""
    cache_key = f"user_{instance.id}"
    cache.delete(cache_key)