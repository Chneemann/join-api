from rest_framework import serializers
from .models import Task, SubTask, AssignedTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'done']

class AssignedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedTask
        fields = ['id', 'task', 'user']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    assigned_users = AssignedTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'date', 'creator', 'created_at', 'subtasks', 'assigned_users']