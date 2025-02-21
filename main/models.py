from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=50, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_tasks', args=[str(self.pk)])
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-important']

class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks', default=1)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=22, null=True, blank=True, verbose_name=u"Заголовок", default="")
    description = models.TextField(null=True, blank=True, verbose_name=u"Описание", default="")
    complete =  models.BooleanField(default=False, verbose_name=u"Состояние")
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-important', 'complete']

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True, default="")
    text = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return str(self.title)

class AuthUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.login
    
@receiver(pre_save, sender=Category)
def update_created_at(sender, instance, **kwargs):
    if instance.pk:
        instance.created_at = datetime.now()

@receiver(pre_save, sender=Task)
def update_created_at(sender, instance, **kwargs):
    if instance.pk:
        instance.created_at = datetime.now()