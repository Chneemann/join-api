import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from task_app.models import Task, SubTask, AssignedTask
from task_app.choices import TaskCategory, TaskPriority, TaskStatus

User = get_user_model()

class TaskModelTests(TestCase):

    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="User", email="test@example.com")
        self.user = user

    def test_task_creation(self):
        task = Task.objects.create(
            title="Test Task 1",
            description="Description 1",
            category=TaskCategory.TECHNICAL_TASK,
            priority=TaskPriority.LOW,
            status=TaskStatus.TODO,
            date="2025-01-01",
            creator=self.user
        )
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(str(task), 'Test Task')
        self.assertIsNotNone(task.id)
        self.assertEqual(task.creator, self.user)
        self.assertIsNotNone(task.created_at)

    def test_subtask_creation(self):
        task = Task.objects.create(title='Parent Task', creator=self.user)
        subtask = SubTask.objects.create(task=task, title='Test SubTask')
        self.assertTrue(isinstance(subtask, SubTask))
        self.assertEqual(str(subtask), 'Parent Task - Test SubTask')
        self.assertIsNotNone(subtask.id)
        self.assertEqual(subtask.task, task)
        self.assertEqual(subtask.status, False)

    def test_assigned_task_creation(self):
        task = Task.objects.create(title='Assigned Task', creator=self.user)
        assigned_user = User.objects.create(username='assigneduser')
        assigned_task = AssignedTask.objects.create(user=assigned_user, task=task)
        self.assertTrue(isinstance(assigned_task, AssignedTask))
        self.assertEqual(str(assigned_task), 'assigneduser - Assigned Task')
        self.assertEqual(assigned_task.user, assigned_user)
        self.assertEqual(assigned_task.task, task)

    def test_task_default_uuid(self):
        task = Task.objects.create(title='UUID Task', creator=self.user)
        self.assertTrue(isinstance(task.id, uuid.UUID))
        task2 = Task.objects.create(title='Another UUID Task', creator=self.user)
        self.assertNotEqual(task.id, task2.id)

    def test_subtask_default_status(self):
        task = Task.objects.create(title='Task with Subtask', creator=self.user)
        subtask = SubTask.objects.create(task=task, title='Default Status Subtask')
        self.assertFalse(subtask.status)