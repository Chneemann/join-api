from rest_framework import serializers
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from .models import Task, SubTask, AssignedTask, TaskStatus

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'status']

class AssignedTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = AssignedTask
        fields = ['user_id']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    assignees = AssignedTaskSerializer(source='assigned', many=True, read_only=True)
    creator = serializers.CharField(source='creator.id', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'date', 'creator', 'created_at', 'subtasks', 'assignees']
        read_only_fields = ['id', 'creator', 'created_at']

    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser]