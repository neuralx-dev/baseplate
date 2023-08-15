from django.contrib import admin

# Register your models here.
from roboprompt.models import *

admin.site.register(Prompt)
admin.site.register(PromptLike)
admin.site.register(Comment)