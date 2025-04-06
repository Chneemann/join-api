from django.test import TestCase
from django.contrib.auth import get_user_model
from task_app.caching import get_cached_task_by_id
from task_app.models import Task, AssignedTask
from task_app.choices import TaskCategory, TaskPriority, TaskStatus
from django.core.cache import cache

User = get_user_model()

class TaskCacheTests(TestCase):
    
    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="User", email="test@example.com")
        self.user = user

        self.task1 = Task.objects.create(
            title="Test Task 1",
            description="Description 1",
            category=TaskCategory.TECHNICAL_TASK,
            priority=TaskPriority.LOW,
            status=TaskStatus.TODO,
            date="2025-01-01",
            creator=self.user
        )
        
        self.task2 = Task.objects.create(
            title="Test Task 2",
            description="Description 2",
            category=TaskCategory.USER_STORY,
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.IN_PROGRESS,
            date="2025-01-02",
            creator=self.user
        )

        cache.clear()

    def test_get_cached_task_by_id(self):
        task = get_cached_task_by_id(self.task1.id)
        self.assertIsNotNone(task)
        self.assertEqual(task, self.task1)

    def test_cache_invalidation_on_task_save(self):
        cache.clear()

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)

        self.task1.status = TaskStatus.DONE
        self.task1.save()

        self.assertIsNone(cache.get(f"task_{self.task1.id}"))

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)

    def test_cache_invalidation_on_task_delete(self):
        cache.clear()

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)

        task_id = self.task1.id
        self.task1.delete()

        self.assertIsNone(cache.get(f"task_{task_id}"))

        task = get_cached_task_by_id(task_id)
        self.assertIsNone(task)

    def test_cache_invalidation_on_assigned_task_save(self):
        cache.clear()

        AssignedTask.objects.create(user=self.user, task=self.task1)

        self.assertIsNone(cache.get(f"task_{self.task1.id}"))

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)

    def test_cache_invalidation_on_assigned_task_delete(self):
        cache.clear()

        assigned_task = AssignedTask.objects.create(user=self.user, task=self.task1)
        assigned_task.delete()

        self.assertIsNone(cache.get(f"task_{self.task1.id}"))

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)
        
    def test_cache_serialization_error_handling(self):
        cache.set("task_corrupted", b"corrupted_data")
        cache.delete("task_corrupted")
        
        self.assertIsNone(cache.get("task_corrupted"))

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)

    def test_cache_behavior_on_multiple_tasks(self):
        cache.clear()

        task1 = get_cached_task_by_id(self.task1.id)
        task2 = get_cached_task_by_id(self.task2.id)

        self.assertEqual(task1, self.task1)
        self.assertEqual(task2, self.task2)

    def test_cache_removal_on_multiple_task_deletion(self):
        cache.clear()

        task1_id = self.task1.id
        task2_id = self.task2.id

        self.task1.delete()
        self.task2.delete()

        self.assertIsNone(cache.get(f"task_{task1_id}"))
        self.assertIsNone(cache.get(f"task_{task2_id}"))

    def test_cache_after_task_update(self):
        cache.clear()

        self.task1.title = "Updated Task 1"
        self.task1.save()

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task.title, "Updated Task 1")

    def test_cache_check_on_no_changes(self):
        cache.clear()

        task = get_cached_task_by_id(self.task1.id)
        self.assertEqual(task, self.task1)

        cached_task = cache.get(f"task_{self.task1.id}")
        self.assertIsNotNone(cached_task)

        cache.delete(f"task_{self.task1.id}")
        self.assertIsNone(cache.get(f"task_{self.task1.id}"))