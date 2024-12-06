from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('User must have login')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save()
        return user