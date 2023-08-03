from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.db.models import Q

from authentication.managers import UserAccountManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserAccountManager()
    role = models.IntegerField(default=0, choices=(
        (0, 'user'),
        (1, 'moderator'),
    ))


