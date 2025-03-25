from django.test import TestCase
from .models import User
from .caching import get_cached_user

class UserCacheTest(TestCase):
    def test_cache_invalidierung_nach_speichern(self):
        user = User.objects.create(first_name="Test", last_name="User", email="test@example.com")

        cached_user = get_cached_user(user.id)
        self.assertIsNotNone(cached_user)

        user.first_name = "Updated"
        user.save()

        cached_user_after_update = get_cached_user(user.id)
        self.assertIsNotNone(cached_user_after_update)