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
    assignees = serializers.SerializerMethodField() 
    subtasks = SubTaskSerializer(many=True, read_only=True) 

    def get_assignees(self, obj):
        return obj.assigned_users.all().values('id', 'user', 'task')  

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'date', 
                  'creator', 'created_at', 'subtasks', 'assignees']