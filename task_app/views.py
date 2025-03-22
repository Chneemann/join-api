from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Task, SubTask, AssignedTask
from .serializers import TaskSerializer, SubTaskSerializer, AssignedTaskSerializer
from rest_framework.decorators import action
from .caching import get_cached_tasks_by_status
from user_app.caching import get_cached_user

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get('status', None)

        if status_param:
            tasks = get_cached_tasks_by_status(status_param)
            return tasks
        return Task.objects.all()

    def get(self, request, status=None):
        tasks = get_cached_tasks_by_status(status)
        task_data = []

        for task in tasks:
            creator = get_cached_user(task['creator_id'])
            assignees = [get_cached_user(assignee['user_id']) for assignee in task['assigned_users']] 

            task_data.append({
                'title': task['title'],
                'description': task['description'],
                'status': task['status'],
                'creator': creator.first_name if creator else None,
                'assignees': [assignee.first_name for assignee in assignees if assignee]
            })
        
        return Response(task_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        status = request.data.get('status')

        if not status:
            return Response({'status': 'failed', 'message': 'No status provided'}, status=400)

        valid_statuses = ['todo', 'inprogress', 'awaitfeedback', 'done']
        if status not in valid_statuses:
            return Response({'status': 'failed', 'message': f'Invalid status: {status}'}, status=400)

        task.status = status
        task.save()
        return Response({'status': 'updated', 'task_id': task.id})


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class AssignedTaskViewSet(viewsets.ModelViewSet):
    queryset = AssignedTask.objects.all()
    serializer_class = AssignedTaskSerializer