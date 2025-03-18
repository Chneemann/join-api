from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[('technical_task', 'Technical Task'), ('user_story', 'User Story')])
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
        return f"{self.user.username} assigned to {self.task.title}"