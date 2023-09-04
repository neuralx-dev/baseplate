from django.urls import path
from .views import *

urlpatterns = [
    path("apps/create/", create_app, name="create_tool"),
    path("apps/home/", HomeViewClass.as_view(), name="apps_home"),
    path("apps/mine/", get_my_apps, name="get_my_apps"),
    path("apps/get/<int:id>/", get_app, name="get_app"),
    path("apps/delete/<int:id>/", delete_app, name="delete_app"),
    path("apps/process/", get_response, name="get_response"),
    path("apps/categories/all/", get_categories, name="get_categories"),
    path("apps/add/field/<int:id>/", add_field_to_app, name="add_field_to_app"),
    # This matches /tools/1/, /tools/2/, etc. and handles GET, PUT, PATCH and DELETE requests
]
