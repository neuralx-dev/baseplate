from django.db import models

from authentication.models import User


# Create your models here.

class Map(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500,default='')
    map_file = models.FileField(upload_to='images/maps',default='')
    map_content = models.TextField(max_length=10000)


class Section(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    code = models.SlugField()


class Scenario(models.Model):
    patient = models.TextField()
    chief_complaint = models.TextField()
    illness = models.TextField()
    past_history = models.TextField()
    drug_history = models.TextField()
    social_history = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    prompt = models.TextField(max_length=5000)


class Chat(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    role = models.CharField(max_length=50, choices=(('system', 'system'), ('user', 'user'), ('assistant', 'assistant')))
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

