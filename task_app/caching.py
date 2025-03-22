from django.core.cache import cache
from .models import Task

def get_cached_tasks_by_status(status):
    cache_key = f"tasks_by_status_{status}"

    cached_tasks = cache.get(cache_key)

    if cached_tasks is not None:
        return cached_tasks
    
    tasks = Task.objects.filter(status=status)
    
    cache.set(cache_key, tasks, timeout=3600)
    
    return tasks