from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from robodoc.models import *


class MapSerializer(ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class ScenarioSerializerList(ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'chief_complaint', 'patient']


class SectionSerializer(ModelSerializer):
    scenarios = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['map', 'name', 'description', 'code', 'scenarios']

    def get_scenarios(self, obj):
        scenarios = Scenario.objects.filter(section=obj)
        return ScenarioSerializerList(scenarios, many=True).data


class ScenarioSerializer(ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'