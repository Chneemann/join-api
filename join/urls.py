from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_app.views import TaskViewSet, SubTaskViewSet, AssignedTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'assigned_tasks', AssignedTaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]