import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_uuid_without_dashes():
    return str(uuid.uuid4()).replace("-", "")

class Task(models.Model):
    id = models.CharField(primary_key=True, default=generate_uuid_without_dashes, max_length=32,editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[('Technical Task', 'Technical Task'), ('User Story', 'User Story')])
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('urgent', 'Urgent')])
    status = models.CharField(max_length=50, choices=[('todo', 'Todo'), ('in_progress', 'In Progress'), ('await_feedback', 'Await feedback'), ('done', 'Done')])
    date = models.DateField()
    
    creator = models.ForeignKey(User, related_name="created_tasks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.title}"


class AssignedTask(models.Model):
    task = models.ForeignKey(Task, related_name="assigned_users", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="assigned_tasks", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} assigned to {self.task.title}"