# tasks/forms.py
from apps.users.models import CustomUser
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
        }

class TaskImageForm(forms.Form):
    image1 = forms.ImageField(required=False, label='Imagen 1')
    image2 = forms.ImageField(required=False, label='Imagen 2')
    image3 = forms.ImageField(required=False, label='Imagen 3')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar']

    