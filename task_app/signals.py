from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, AssignedTask

@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def clear_task_cache(sender, instance, **kwargs):
    """Invalidate cache for the affected task status and individual task"""
    cache.delete(f"task_{instance.id}") 

@receiver(post_save, sender=AssignedTask)
@receiver(post_delete, sender=AssignedTask)
def clear_assigned_task_cache(sender, instance, **kwargs):
    """Invalidate cache when a task assignment changes"""
    cache.delete(f"task_{instance.task.id}")