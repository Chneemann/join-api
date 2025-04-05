from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_app.views import TaskViewSet, SubTaskViewSet, AssignedTaskViewSet
from user_app.views import UserViewSet
from auth_app.views import LoginView, LogoutView, AuthView, RegisterView, PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'assigned_tasks', AssignedTaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    path('auth/', AuthView.as_view(), name='auth'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]