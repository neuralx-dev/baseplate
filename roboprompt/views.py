from django.db.models import Q, Count
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Prompt
from .serializers import *


# Authenticated class based API view for CRUD on Prompt model
class PromptAPIViewCreate(generics.ListCreateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]


class PromptAPIView(generics.ListCreateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializerForList
    permission_classes = [IsAuthenticated]


class PromptDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_prompt(request, prompt_id):
    # Get the prompt object by its id
    try:
        prompt = Prompt.objects.get(id=prompt_id)
    except Prompt.DoesNotExist:
        return Response({'error': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get the user object from the request
    user = request.user

    # Check if the user has already liked the prompt
    if PromptLike.objects.filter(prompt=prompt, user=user).exists():
        PromptLike.objects.filter(prompt=prompt, user=user).first().delete()
        return Response({'error': 'unliked', 'like_count': prompt.like_count}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Create a new prompt like object and save it
    prompt_like = PromptLike(prompt=prompt, user=user)
    prompt_like.save()

    # Return a success message and the new like count
    return Response({'message': 'You liked this prompt', 'like_count': prompt.like_count},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_prompt(request, prompt_id):
    # Get the prompt object by its id
    try:
        prompt = Prompt.objects.get(id=prompt_id)
    except Prompt.DoesNotExist:
        return Response({'error': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get the user object from the request
    user = request.user

    # Get the comment content from the request data
    content = request.data['content']
    if not content:
        return Response({'error': 'Comment content is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new comment object and save it
    comment = Comment(user=user, prompt=prompt, content=content)
    comment.save()

    # Serialize the comment object and return it
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_prompt(request, prompt_id):
    # Get the prompt object by its id
    try:
        prompt = Prompt.objects.get(id=prompt_id)
    except Prompt.DoesNotExist:
        return Response({'error': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the prompt object and return it
    serializer = PromptSerializerDetail(prompt)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Function based view that returns top 21 most liked prompts for Django REST Framework
@api_view(['GET'])
def get_top_prompts(request):
    # Get the prompts ordered by like count in descending order
    prompts = Prompt.objects.all()[:21]

    # Serialize the prompts and return a JSON response with the data
    serializer = PromptSerializerForList(prompts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_prompt(request):
    # Get the query parameter from the request
    query = request.query_params.get('q')
    if not query:
        return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Search the prompts by the query in the following fields: tags, ai_type, language, command, title, description
    # Order them by like_count in descending order
    prompts = Prompt.objects.filter(
        Q(tags__icontains=query) |
        Q(ai_type__icontains=query) |
        Q(language__icontains=query) |
        Q(command__icontains=query) |
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )[:21]

    # Serialize the prompts and return a JSON response with the data
    serializer = PromptSerializerForList(prompts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


