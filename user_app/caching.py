import json
from django.core.cache import cache
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer

def get_cached_user(user_id):
    cache_key = f"user_{user_id}"
    cached_user = cache.get(cache_key)
    
    if cached_user is not None:
        return cached_user
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None

    serializer = UserSerializer(user)
    user_data = serializer.data
 
    cache.set(cache_key, user_data, timeout=3600)

    return user_data


def cache_user(user_id, user_data, timeout=3600):
    """
    Saves user data in the cache.
    """
    cache_key = f"user_{user_id}" 
    cache.set(cache_key, user_data, timeout)