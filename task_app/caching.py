from django.core.cache import cache
from django.core import serializers
from .models import Task

def get_cached_tasks():
    cache_key = "all_tasks"
    cached_tasks_json = cache.get(cache_key)

    if cached_tasks_json is not None:
        deserialized_objects = list(serializers.deserialize('json', cached_tasks_json))
        tasks = [obj.object for obj in deserialized_objects]
        return tasks

    tasks = Task.objects.all()
    tasks_json = serializers.serialize('json', tasks)
    cache.set(cache_key, tasks_json, timeout=3600)
    return tasks

def get_cached_tasks_by_status(status):
    cache_key = f"tasks_by_status_{status}"
    cached_tasks_json = cache.get(cache_key)

    if cached_tasks_json is not None:
        deserialized_objects = list(serializers.deserialize('json', cached_tasks_json))
        tasks = [obj.object for obj in deserialized_objects]
        return tasks

    tasks = Task.objects.filter(status=status)
    tasks_json = serializers.serialize('json', tasks)
    cache.set(cache_key, tasks_json, timeout=3600)
    return tasks

def get_cached_task_by_id(task_id):
    cache_key = f"task_{task_id}"
    cached_task_json = cache.get(cache_key)

    if cached_task_json is not None:
        try:
            return list(serializers.deserialize('json', cached_task_json))[0].object
        except IndexError:
            return None

    try:
        task = Task.objects.get(pk=task_id)
        task_json = serializers.serialize('json', [task])
        cache.set(cache_key, task_json, timeout=3600)
        return task
    except Task.DoesNotExist:
        return None