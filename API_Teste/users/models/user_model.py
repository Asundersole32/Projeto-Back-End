from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from uuid import uuid4

from ..user_manager import CustomUserManager


class CustomUser(AbstractBaseUser):
    uid = models.UUIDField(default=uuid4, primary_key=True, editable=False, unique=True)
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
    username=models.CharField(max_length=30, unique=True)
    data_joined=models.DataTimeField(verbose_name="data joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    first_name=models.CharField(max_length=60)
    last_name=models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username + ", " + self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
