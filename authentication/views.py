# Create your views here.
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import UserSerializerData


@api_view(['POST'])
def register(request):
    user = User.objects.create(email=request.data['email'])
    user.set_password(request.data['password'])
    user.save()
    refresh = RefreshToken.for_user(user)

    return Response({**{
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }, **dict(UserSerializerData(user).data)}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = authenticate(request, email=request.data['email'], password=request.data['password'])

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({**{
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }, **dict(UserSerializerData(user).data)}, status=status.HTTP_200_OK)
    else:

        user = User.objects.create(
            email=request.data['email'],
        )
        user.set_password(request.data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({**{
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }, **dict(UserSerializerData(user).data)}, status=status.HTTP_201_CREATED)
