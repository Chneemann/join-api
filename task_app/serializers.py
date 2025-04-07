from rest_framework import serializers
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from .models import Task, SubTask, AssignedTask

class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source='task.id')

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'status', 'task']

class AssignedTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = AssignedTask
        fields = ['user_id']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    assignees = AssignedTaskSerializer(source='assigned_tasks', many=True, read_only=True)

    def get_assignees(self, obj):
        return list(obj.assigned_tasks.all().values('user_id'))

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'date', 'creator', 'created_at', 'subtasks', 'assignees']
        read_only_fields = ['id', 'creator', 'created_at']

    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]