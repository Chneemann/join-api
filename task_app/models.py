import uuid
from django.db import models
from django.contrib.auth import get_user_model
from .choices import TaskCategory, TaskPriority, TaskStatus
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

User = get_user_model()

def generate_uuid_without_dashes():
    return uuid.uuid4().hex

class Task(models.Model):
    id = models.CharField(primary_key=True, default=generate_uuid_without_dashes, max_length=32, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=TaskCategory.choices)
    priority = models.CharField(max_length=50, choices=TaskPriority.choices)
    status = models.CharField(max_length=50, choices=TaskStatus.choices)
    date = models.DateField()
    creator = models.ForeignKey(User, related_name="created_tasks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    id = models.CharField(primary_key=True, default=generate_uuid_without_dashes, max_length=32, editable=False, unique=True)
    task = models.ForeignKey(Task, related_name="subtasks_task", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.title}"

class AssignedTask(models.Model):
    user_id = models.ForeignKey(User, related_name="assigned_task", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="assigned_task", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_id} - {self.task}"