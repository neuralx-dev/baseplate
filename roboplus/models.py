from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    color = models.CharField(max_length=50, default='fff')

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    prompt = models.TextField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, default='bi-app')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    key = models.CharField(max_length=50)
    default = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    app = models.ForeignKey(App, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.key


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
