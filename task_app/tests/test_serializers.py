import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from task_app.models import Task, SubTask, AssignedTask
from task_app.serializers import TaskSerializer, SubTaskSerializer, AssignedTaskSerializer
from task_app.choices import TaskCategory, TaskPriority, TaskStatus
from datetime import date

User = get_user_model()

class SerializerTests(TestCase):

    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="User", email="test@example.com")
        self.user = user
        self.test_date = date(2025, 1, 1)

        self.task = Task.objects.create(
            title="Test Task 1",
            description="Description 1",
            category=TaskCategory.TECHNICAL_TASK,
            priority=TaskPriority.LOW,
            status=TaskStatus.TODO,
            date=self.test_date,
            creator=self.user
        )

        self.subtask1 = SubTask.objects.create(task=self.task, title='SubTask 1', status=True)
        self.subtask2 = SubTask.objects.create(task=self.task, title='SubTask 2', status=False)
        self.assigned_user = User.objects.create(email='assigned@example.com')
        self.assigned_task = AssignedTask.objects.create(user=self.assigned_user, task=self.task)

    def test_subtask_serializer(self):
        serializer = SubTaskSerializer(self.subtask1)
        expected_data = {'id': str(self.subtask1.id), 'title': 'SubTask 1', 'status': True, 'task': str(self.task.id)}
        self.assertEqual(serializer.data, expected_data)
        
    def test_assigned_task_serializer(self):
        serializer = AssignedTaskSerializer(self.assigned_task)
        expected_data = {'user_id': str(self.assigned_user.id)}
        self.assertEqual(serializer.data, expected_data)

    def test_task_serializer(self):
        serializer = TaskSerializer(self.task)
        expected_data = {
            'id': str(self.task.id),
            'title': 'Test Task 1',
            'description': 'Description 1',
            'category': 'Technical Task',
            'priority': 'low',
            'status': 'todo',
            'date': '2025-01-01',
            'creator': self.user.id,
            'created_at': self.task.created_at.isoformat().replace('+00:00', 'Z'),
            'subtasks': [
                {'id': str(self.subtask1.id), 'title': 'SubTask 1', 'status': True, 'task': str(self.task.id)},
                {'id': str(self.subtask2.id), 'title': 'SubTask 2', 'status': False, 'task': str(self.task.id)}
            ],
            'assignees': [{'user_id': str(self.assigned_user.id)}]
        }
        
        self.assertEqual(serializer.data, expected_data)
        
    def test_task_serializer_create_validation(self):
        data = {
            'title': 'New Task',
            'category': 'INVALID',
            'priority': TaskPriority.LOW,
            'status': TaskStatus.TODO,
            'date': '2025-04-20',
            'creator': self.user.id
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)

    def test_task_serializer_update_validation(self):
        data = {'priority': 'WRONG'}
        serializer = TaskSerializer(self.task, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('priority', serializer.errors)