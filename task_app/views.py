from rest_framework import viewsets
from .models import Task, SubTask, AssignedTask
from .serializers import TaskSerializer, SubTaskSerializer, AssignedTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

class AssignedTaskViewSet(viewsets.ModelViewSet):
    queryset = AssignedTask.objects.all()
    serializer_class = AssignedTaskSerializer