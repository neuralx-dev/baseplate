from rest_framework import serializers
from .models import Tool, ToolLike


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'name', 'about', 'desc', 'banner', 'logo', 'link', 'tags']


class ToolSerializerForList(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = ['id', 'name', 'about', 'desc', 'banner', 'logo', 'link', 'tags', 'like_count']

    def get_like_count(self, obj):
        return ToolLike.objects.filter(tool=obj).count()
