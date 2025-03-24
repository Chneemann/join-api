from rest_framework import serializers
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from .models import Task, SubTask, AssignedTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'done']

class AssignedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedTask
        fields = ['user_id']

class TaskSerializer(serializers.ModelSerializer):
    assignees = serializers.SerializerMethodField() 
    subtasks = SubTaskSerializer(many=True, read_only=True) 

    def get_assignees(self, obj):
        return obj.assigned_tasks.all().values('user_id')  

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'priority', 'status', 'date', 
                  'creator', 'created_at', 'subtasks', 'assignees']

    renderer_classes = [CamelCaseJSONRenderer] 
    parser_classes = [CamelCaseJSONParser]