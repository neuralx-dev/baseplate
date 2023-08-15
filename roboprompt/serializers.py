from rest_framework import serializers

from authentication.serializers import UserSerializerProfile
from .models import *


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = '__all__'


class PromptLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptLike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerProfile()

    class Meta:
        model = Comment
        fields = '__all__'


# Serializer for the prompt model that returns like count and all comments too
class PromptSerializerDetail(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    creator = UserSerializerProfile()

    class Meta:
        model = Prompt
        fields = ['id', 'title', 'description', 'command', 'language', 'verified', 'creator', 'ai_type', 'like_count',
                  'comments', 'tags']

    def get_like_count(self, obj):
        return PromptLike.objects.filter(prompt=obj).count()

    def get_comments(self, obj):
        comments = Comment.objects.filter(prompt=obj)
        return CommentSerializer(comments, many=True).data


class PromptSerializerForList(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    creator = UserSerializerProfile()

    class Meta:
        model = Prompt
        fields = ['id', 'title', 'description', 'command', 'language', 'verified', 'creator', 'ai_type', 'like_count',
                  'tags']

    def get_like_count(self, obj):
        return PromptLike.objects.filter(prompt=obj).count()
