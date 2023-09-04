from rest_framework import serializers

from authentication.serializers import UserSerializerProfile
from roboplus.models import *


class CategorySerializerList(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class FieldSerializerInsert(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['key', 'default', 'label', 'description']


class AppSerializerDetail(serializers.ModelSerializer):
    fieldss = serializers.SerializerMethodField()

    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'category', 'icon', 'fieldss', 'prompt']

    def get_fieldss(self, obj):
        fields = Field.objects.filter(app=obj)
        return FieldSerializer(fields, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    apps = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'apps']

    def get_apps(self, obj):
        apps = App.objects.filter(category=obj).order_by('-id')
        return AppSerializer(apps, many=True).data


class AppSerializerDisplay(serializers.ModelSerializer):
    fieldss = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'category', 'icon', 'fieldss', 'prompt']

    def get_fieldss(self, obj):
        fields = Field.objects.filter(app=obj)
        return FieldSerializer(fields, many=True).data

    def get_category(self, obj):
        return CategorySerializerList(Category.objects.get(id=obj.category.id)).data
