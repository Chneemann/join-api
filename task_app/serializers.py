from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, SubTask, AssignedTask

User = get_user_model()

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'

class AssignedTaskSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Gibt den Usernamen zurück, anstatt der ID

    class Meta:
        model = AssignedTask
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    assigned_users = AssignedTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'