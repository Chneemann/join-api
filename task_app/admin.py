from django.contrib import admin
from .models import Task, SubTask, AssignedTask

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

class AssignedTaskInline(admin.TabularInline):
    model = AssignedTask
    extra = 1 

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'priority', 'creator', 'date')
    search_fields = ('title', 'category', 'creator__username')
    list_filter = ('status', 'priority', 'date')
    inlines = [SubTaskInline, AssignedTaskInline]