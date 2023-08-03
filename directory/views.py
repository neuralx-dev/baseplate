from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tool
from .serializers import ToolSerializer
# Create your views here.
from rest_framework import generics
from .models import Tool
from .serializers import ToolSerializer


@api_view(['GET'])
def tools_for_home(request):
    return Response(ToolSerializer(Tool.objects.all().order_by('?')[:20], many=True).data, status=status.HTTP_200_OK)


class ToolListCreateView(generics.ListCreateAPIView):
    # This view handles GET and POST requests for the Tool model
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


class ToolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # This view handles GET, PUT, PATCH and DELETE requests for a single Tool instance
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer


@api_view(['GET'])
def search_tools(request):
    #query = request.data['term']
    query = request.query_params.get('term', '')
    print()
    # filter out the tools that have the query in either name, about or tags
    tools = Tool.objects.filter(Q(name__contains=query) | Q(name__contains=query) | Q(name__contains=query))
    # serialize the tools
    tool_serializer = ToolSerializer(tools, many=True)
    # return a response with the serialized data and a status code of 200 (OK)
    return Response(tool_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_tags(request):
    tags = Tool.objects.values_list('tags', flat=True)
    # join the list of tags with a '-' character
    tags_string = ','.join(tags)

    return Response(list(set(tags_string.split(','))), status=status.HTTP_200_OK)
