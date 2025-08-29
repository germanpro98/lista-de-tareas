# tasks/models.py
from django.db import models
from django.conf import settings  # para referenciar al usuario actual

class Task(models.Model):
    user = models.ForeignKey(  # 👈 Enlace con el usuario
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class TaskImage(models.Model):
    task = models.ForeignKey(Task, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='task_images/, blank=True, null=True')

    def __str__(self):
        return f"Imagen de {self.task.title}"
