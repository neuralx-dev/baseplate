from rest_framework import serializers
from .models import Tool


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'about', 'desc', 'banner', 'logo', 'link', 'tags']
