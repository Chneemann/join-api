from django.core.cache import cache
from django.core import serializers
from .models import Task

CACHE_TIMEOUT = 3600

def get_cached_task_by_id(task_id):
    return _get_or_set_cache(f"task_{task_id}", Task.objects.filter(pk=task_id), single=True)

def _get_or_set_cache(cache_key, queryset, single=False):
    cached_json = cache.get(cache_key)
    if cached_json:
        try:
            deserialized = list(serializers.deserialize("json", cached_json))
            return deserialized[0].object if single and deserialized else [obj.object for obj in deserialized]
        except Exception:
            cache.delete(cache_key)

    return _fetch_and_cache(cache_key, queryset, single)

def _fetch_and_cache(cache_key, queryset, single=False):
    objects = list(queryset)
    
    if not objects:
        return None if single else []
    
    serialized_json = serializers.serialize("json", objects)
    cache.set(cache_key, serialized_json, timeout=CACHE_TIMEOUT)
    
    return objects[0] if single else objects