import json
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from .serializers import UserSerializer

CACHE_TIMEOUT = 3600

def get_cached_user_by_id(user_id):
    return _get_or_set_cache(f"user_{user_id}", user_id)

def _get_or_set_cache(cache_key, user_id=None):
    cached_json = cache.get(cache_key)
    
    if cached_json:
        try:
            return json.loads(cached_json)
        except json.JSONDecodeError:
            cache.delete(cache_key)
    
    return _fetch_and_cache(cache_key, user_id)

def _fetch_and_cache(cache_key, user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    
    serializer = UserSerializer(user)
    user_data = serializer.data
    
    cache.set(cache_key, json.dumps(user_data), timeout=CACHE_TIMEOUT)
    
    return user_data