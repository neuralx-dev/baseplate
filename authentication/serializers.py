from rest_framework.serializers import ModelSerializer, ReadOnlyField

from authentication.models import User


class UserSerializerData(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']


class UserSerializerProfile(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
