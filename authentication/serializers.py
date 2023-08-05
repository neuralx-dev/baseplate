from rest_framework.serializers import ModelSerializer, ReadOnlyField

from authentication.models import User


class UserSerializerData(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']


class UserSerializerProfile(ModelSerializer):
    symbol_name = ReadOnlyField()
    ranking = ReadOnlyField()
    stats = ReadOnlyField()
    points = ReadOnlyField()
    level = ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name', 'ranking', 'stats', 'points', 'level']
