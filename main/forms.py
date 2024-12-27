from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']