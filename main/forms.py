from django import forms
from .models import Task

class MyModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']