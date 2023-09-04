from django.db import models
from authentication.models import *


# Create your models here.
class Tool(models.Model):
    name = models.CharField(max_length=150, default='')
    about = models.CharField(max_length=500, default='')
    desc = models.TextField(max_length=10500, default='')
    banner = models.FileField(upload_to='images/banners/')
    logo = models.FileField(upload_to='images/logos/', default='')
    link = models.CharField(max_length=150, default='')
    tags = models.CharField(max_length=1000, default='')


class ToolLike(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
