import json
from django.core.cache import cache
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

def get_cached_user(user_id):
    cache_key = f"user_{user_id}"
    cached_user_json = cache.get(cache_key)

    if cached_user_json is not None:
        return json.loads(cached_user_json)

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None

    if user:
        user_data = serializers.serialize('json', [user])
        cache.set(cache_key, user_data, timeout=3600)
        return json.loads(user_data)[0]['fields']
    else:
        return None