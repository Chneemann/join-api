from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask, AssignedTask
from .serializers import TaskSerializer, SubTaskSerializer, AssignedTaskSerializer
from rest_framework.decorators import action
from .caching import get_cached_task_by_id
from django.core.cache import cache
from .choices import TaskStatus
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, pk=None):
        task = get_cached_task_by_id(pk)
        if not task:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            cache.delete(f"task_{task.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            cache.delete(f"task_{pk}")
            return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch']) 
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response({'error': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = [choice[0] for choice in TaskStatus.choices]
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Valid statuses: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"task_{task.id}")

        task.status = new_status
        task.save()
        return Response({'status': 'Status updated.'})

class SubTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class AssignedTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = AssignedTask.objects.all()
    serializer_class = AssignedTaskSerializer