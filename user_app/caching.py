from django.core.cache import cache
from .models import User
from django.core.exceptions import ObjectDoesNotExist

def get_cached_user(user_id):
    cache_key = f"user_{user_id}"

    cached_user = cache.get(cache_key)
    if cached_user is not None:
        return cached_user
    
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    
    cache.set(cache_key, user, timeout=3600)
    
    return user