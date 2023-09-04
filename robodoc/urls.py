from django.urls import path
from .views import *

urlpatterns = [
    path('maps/', MapList.as_view(), name='map-list'),
    path('maps/<int:pk>/', MapDetail.as_view(), name='map-detail'),
    path('sections/<slug:code>/', section_detail, name='section-detail'),
    path('scenario/<int:id>/', scenario_details, name='scenario-detail'),
    path('chat/create/', submit_chat, name='submit_chat'),

]
