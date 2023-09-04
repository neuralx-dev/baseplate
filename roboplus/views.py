import json
import os

import openai
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .models import App, Field, Category
from .serializers import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_app(request):
    data = request.data
    app = App(
        name=data['name'],
        description=data['description'],
        category_id=data['category_id'],
        icon=data['icon'],
        user_id=request.user.id
    )
    app.save()
    for i in data['fields']:
        Field.objects.create(
            key=i['key'],
            description=i['description'],
            label=i['label'],
            default=i['default'],
            app=app
        )

    # Return the created app and fields data
    return Response(AppSerializerDetail(app).data, status=status.HTTP_201_CREATED)


class HomeViewClass(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_app(request, id):
    if not App.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    app = App.objects.get(id=id)
    return Response(AppSerializerDisplay(app).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_app(request, id):
    if not App.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    app = App.objects.get(id=id)
    app.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def add_field_to_app(request, id):
    # Get the app and field data from the request
    app = App.objects.get(id=id)
    field_data = request.data
    # fields = json.loads(field_data)

    # Validate the app and field data using model serializers
    field_serializer = FieldSerializerInsert(data=field_data, many=True)
    if field_serializer.is_valid():
        # Save the app and field objects to the database
        # app = app_serializer.save()
        field = field_serializer.save(app=app)

        # Return a success response with the app and field data
        return Response({
            'status': 'success',
            'message': 'Field added to app successfully',
            'app': AppSerializerDisplay(app).data,
        })
    else:
        # Return an error response with the validation errors
        return Response({
            'status': 'error',
            'message': 'Invalid app or field data',
            'field_errors': field_serializer.errors
        })


@api_view(['POST'])
def get_response(request):
    prompt = request.data['prompt']
    openai.api_key = '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'
    query = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system',
             'content': 'you are a machine that only responds what is necessary and '
                        'does not reply with anything further'},
            {"role": "user", "content": prompt}
        ]
    )
    response = query.get('choices')[0]['message']['content']
    return Response({'response': response})


@api_view(['GET'])
def get_categories(request):
    return Response(CategorySerializerList(Category.objects.all(), many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_apps(request):
    return Response(AppSerializer(App.objects.filter(user_id=request.user.id), many=True).data,
                    status=status.HTTP_200_OK)
