from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name=u"Заголовок")
    description = models.TextField(null=True, blank=True, verbose_name=u"Описание")
    complete =  models.BooleanField(default=False, verbose_name=u"Состояние")
    created = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-important', 'complete']

class AuthUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.login