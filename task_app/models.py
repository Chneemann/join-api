import uuid
from django.db import models
from django.contrib.auth import get_user_model
from .choices import TaskCategory, TaskPriority, TaskStatus

User = get_user_model()

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.title}"

class AssignedTask(models.Model):
    user = models.ForeignKey(User, related_name="assigned_tasks", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="assigned_tasks", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} - {self.task}"