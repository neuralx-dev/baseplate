from django.urls import path

from authentication.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('user/set/apikey/', set_openai_api_key),
]
