from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask, AssignedTask
from .serializers import TaskSerializer, SubTaskSerializer, AssignedTaskSerializer
from rest_framework.decorators import action
from .caching import get_cached_tasks, get_cached_task_by_id, get_cached_tasks_by_status
from user_app.caching import get_cached_user
from django.core.cache import cache
from .choices import TaskStatus


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        status_param = request.query_params.get('status', None)
        if status_param:
            tasks = get_cached_tasks_by_status(status_param)
        else:
            tasks = get_cached_tasks()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        task = get_cached_task_by_id(pk)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response({'error': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = [choice[0] for choice in TaskStatus.choices]
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Valid statuses: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"task_{task.id}")
        cache.delete(f"tasks_by_status_{task.status}")

        task.status = new_status
        task.save()
        return Response({'status': 'Status updated.'})


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class AssignedTaskViewSet(viewsets.ModelViewSet):
    queryset = AssignedTask.objects.all()
    serializer_class = AssignedTaskSerializer