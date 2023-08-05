from django.urls import path
from .views import *

urlpatterns = [
    path("tools/", ToolListCreateView.as_view(), name="tool_list"),
    path("tools/search/", search_tools, name="search_tools"),
    path("tools/home/", tools_for_home, name="tools_for_home"),
    path("tools/tags/", all_tags, name="all_tags"),
    path("tools/save/", upload_tool, name="upload_tool"),
    # This matches /tools/ and handles GET and POST requests
    path("tools/<int:pk>/", ToolRetrieveUpdateDestroyView.as_view(), name="tool_detail"),
    # This matches /tools/1/, /tools/2/, etc. and handles GET, PUT, PATCH and DELETE requests
]
