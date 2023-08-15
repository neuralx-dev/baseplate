from django.db import models

# Create your models here.
from django.db import models

from authentication.models import User
from django.db import models


# Prompt model with a title, a description, a command which is long text, language which can be english or any other language, verified which can be true or false make it false by default, creator which refers to a user who created this prompt
class Prompt(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    command = models.TextField()
    language = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    ai_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('image', 'Image')])
    tags = models.CharField(max_length=250, default='')

    @property
    def like_count(self):
        return len(self.promptlike_set.all())


# Prompt like and has only two properties one is prompt which refers to Prompt and a user property which refers to user
class PromptLike(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Comment with a user and prompt property
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    content = models.TextField()
