
from django.contrib import admin
from .models import Task, TaskImage

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed')
    list_filter = ('completed', 'user')
    search_fields = ('title', 'description')

@admin.register(TaskImage)
class TaskImageAdmin(admin.ModelAdmin):
    list_display = ('task', 'image')