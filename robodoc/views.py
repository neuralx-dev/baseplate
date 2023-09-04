from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from robodoc.models import Map, Section, Scenario, Chat, Message
from robodoc.serializers import MapSerializer, SectionSerializer, ScenarioSerializer


# Create your views here.
class MapList(generics.ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


class MapDetail(generics.RetrieveAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


@api_view(['GET'])
def section_detail(request, code):
    try:
        section = Section.objects.get(code=code)
    except Section.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SectionSerializer(section)
    return Response(serializer.data)


@api_view(['GET'])
def scenario_details(request, id):
    try:
        scenario = Scenario.objects.get(id=id)
    except Section.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ScenarioSerializer(scenario)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_chat(request):
    chat = Chat.objects.create(
        doctor_id=request.user.id,
        scenario_id=request.data['scenario_id']
    )
    for i in request.data['messages']:
        Message.objects.create(
            role=i['role'],
            content=['content'],
            chat=chat
        )
    return Response(status=status.HTTP_201_CREATED)
