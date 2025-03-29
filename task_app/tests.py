from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import Task, AssignedTask
from .caching import get_cached_tasks, get_cached_tasks_by_status, get_cached_task_by_id
from .choices import TaskStatus

User = get_user_model()

class TaskCacheTests(TestCase):
    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="User", email="test@example.com")
        self.user = user
        self.task1 = Task.objects.create(
            title="Test Task 1",
            description="Description 1",
            category="Work",
            priority="High",
            status=TaskStatus.TODO,
            date="2025-01-01",
            creator=self.user
        )
        self.task2 = Task.objects.create(
            title="Test Task 2",
            description="Description 2",
            category="Personal",
            priority="Medium",
            status=TaskStatus.IN_PROGRESS,
            date="2025-01-02",
            creator=self.user
        )
        cache.clear()

    def test_get_cached_tasks(self):
        tasks = get_cached_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)

    def test_get_cached_tasks_by_status(self):
        tasks_todo = get_cached_tasks_by_status(TaskStatus.TODO)
        self.assertEqual(len(tasks_todo), 1)
        self.assertEqual(tasks_todo[0], self.task1)
        
        tasks_in_progress = get_cached_tasks_by_status(TaskStatus.IN_PROGRESS)
        self.assertEqual(len(tasks_in_progress), 1)
        self.assertEqual(tasks_in_progress[0], self.task2)

    def test_get_cached_task_by_id(self):
        task = get_cached_task_by_id(self.task1.id)
        self.assertIsNotNone(task)
        self.assertEqual(task, self.task1)

    def test_cache_invalidation_on_task_save(self):
        cache.clear()

        get_cached_tasks()
        self.task1.status = TaskStatus.DONE
        self.task1.save()

        self.assertIsNone(cache.get("all_tasks"))
        self.assertIsNone(cache.get(f"tasks_by_status_{TaskStatus.TODO}"))
        self.assertIsNone(cache.get(f"task_{self.task1.id}"))

        tasks = get_cached_tasks()
        self.assertIn(self.task1, tasks)

    def test_cache_invalidation_on_task_delete(self):
        cache.clear()

        get_cached_tasks()
        task_id = self.task1.id
        self.task1.delete()

        self.assertIsNone(cache.get("all_tasks"))
        self.assertIsNone(cache.get(f"task_{task_id}"))

        tasks = get_cached_tasks()
        self.assertNotIn(self.task1, tasks)

    def test_cache_invalidation_on_assigned_task_save(self):
        cache.clear()

        AssignedTask.objects.create(user_id=self.user, task=self.task1)
        
        self.assertIsNone(cache.get("all_tasks"))
        self.assertIsNone(cache.get(f"tasks_by_status_{self.task1.status}"))
        self.assertIsNone(cache.get(f"task_{self.task1.id}"))

        tasks = get_cached_tasks_by_status(self.task1.status)
        self.assertIn(self.task1, tasks)

    def test_cache_invalidation_on_assigned_task_delete(self):
        cache.clear()

        assigned_task = AssignedTask.objects.create(user_id=self.user, task=self.task1)

        assigned_task.delete()
        
        self.assertIsNone(cache.get("all_tasks"))
        self.assertIsNone(cache.get(f"tasks_by_status_{self.task1.status}"))
        self.assertIsNone(cache.get(f"task_{self.task1.id}"))
        
        tasks = get_cached_tasks_by_status(self.task1.status)
        self.assertIn(self.task1, tasks)

    def test_cache_serialization_error_handling(self):
        cache.set("task_corrupted", b"corrupted_data")

        cache.delete("task_corrupted")

        self.assertIsNone(cache.get("task_corrupted"))

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)