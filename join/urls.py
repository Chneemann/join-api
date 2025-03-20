from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_app.views import TaskViewSet, SubTaskViewSet, AssignedTaskViewSet
from user_app.views import UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'assigned_tasks', AssignedTaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]