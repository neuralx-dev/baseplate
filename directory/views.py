import base64
import os
import random
import time

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tool, ToolLike
from .serializers import ToolSerializer
# Create your views here.
from rest_framework import generics
from .models import Tool
from .serializers import *


@api_view(['GET'])
def tools_for_home(request):
    tags = Tool.objects.values_list('tags', flat=True)
    # join the list of tags with a '-' character
    tags_string = ','.join(tags)
    tags = list(set(tags_string.split(',')))[:15]
    random.shuffle(tags)

    return Response({
        'tools': ToolSerializerForList(Tool.objects.all().order_by('?')[:20], many=True).data,
        'tags': tags,
        'count': len(Tool.objects.all())
    }, status=status.HTTP_200_OK)


class ToolListCreateView(generics.ListCreateAPIView):
    # This view handles GET and POST requests for the Tool model
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


class ToolListView(generics.ListCreateAPIView):
    # This view handles GET and POST requests for the Tool model
    queryset = Tool.objects.all()
    serializer_class = ToolSerializerForList


class ToolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # This view handles GET, PUT, PATCH and DELETE requests for a single Tool instance
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


@api_view(['GET'])
def search_tools(request):
    # query = request.data['term']
    query = request.query_params.get('term', '')
    print()
    # filter out the tools that have the query in either name, about or tags
    tools = Tool.objects.filter(
        Q(name__contains=query) | Q(desc__contains=query) | Q(tags__contains=query) | Q(about__contains=query))
    print(len(tools))
    # serialize the tools
    tool_serializer = ToolSerializerForList(tools, many=True)
    # return a response with the serialized data and a status code of 200 (OK)
    return Response(tool_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_tags(request):
    tags = Tool.objects.values_list('tags', flat=True)
    # join the list of tags with a '-' character
    tags_string = ','.join(tags)
    tags = list(set(tags_string.split(',')))[:25]
    random.shuffle(tags)
    return Response(tags, status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_tool(request):
    # get the json data from the request body
    data = request.data
    print(data)
    print(request.FILES)
    # validate the data

    # # decode the base64 encoded files
    # #logo_data = request.data['logo']
    # banner_data = request.data['banner']
    #
    # #format_logo, imgstr_logo = logo_data.split(';base64,')
    # format_banner, imgstr_banner = banner_data.split(';base64,')
    # #ext_logo = format_logo.split('/')[-1]
    # ext_banner = format_banner.split('/')[-1]
    # #data_logo = ContentFile(base64.b64decode(imgstr_logo))
    # data_banner = ContentFile(base64.b64decode(imgstr_banner))
    #
    # #file_name_logo = f'{int(time.time())}.' + ext_logo
    # file_name_banner = f'{int(time.time())}.' + ext_banner
    # # request.user.avatar.save(file_name, data, save=True)
    #
    # # create a new tool object with the data and the file paths

    # save the tool object to the database

    # logo_file = request.FILES.get('logo')
    banner_file = request.FILES.get('banner')
    fs = FileSystemStorage(location='media/images/banner/')
    filename = fs.save(banner_file.name, banner_file)
    uploaded_file_url = fs.url(filename)
    tool = Tool(
        name=data['name'],
        about=data['about'],
        desc=data['desc'],
        banner='images/banners/' + banner_file.name,
        logo='',
        link=data['link'],
        tags=data['tags']
    )
    tool.save()

    # tool.logo.save(file_name_logo, data_logo, save=True)
    # tool.banner.save(file_name_banner, data_banner, save=True)
    # return a success response with the tool id
    return Response(ToolSerializer(tool, many=False).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_tool(request,tool_id):
    # get the tool id and the user id from the request data
    print(request.data)

    user_id = request.user.id



    # validate the tool id
    if not tool_id:
        return Response({'error': 'Missing tool id'}, status=status.HTTP_400_BAD_REQUEST)

    # check if the tool exists
    try:
        tool = Tool.objects.get(id=tool_id)
    except Tool.DoesNotExist:
        return Response({'error': 'Tool not found'}, status=status.HTTP_404_NOT_FOUND)

    # check if the user has already liked the tool
    if ToolLike.objects.filter(tool=tool, user=user_id).exists():
        ToolLike.objects.filter(tool=tool, user=user_id).first().delete()
        return Response({'error': 'like deleted'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # create a new tool like object with the tool and the user ids
    tool_like = ToolLike(tool=tool, user_id=user_id)

    # save the tool like object to the database
    tool_like.save()

    # return a success response with the tool like id
    return Response({'id': tool_like.id}, status=status.HTTP_201_CREATED)