from django.urls import path
from .views import *

urlpatterns = [
    path("prompts/", PromptAPIView.as_view(), name="prompt_list"),
    path("prompts/create/", PromptAPIViewCreate.as_view(), name="create_prompt"),
    path("prompts/top/", get_top_prompts, name="top_prompts"),
    path("prompts/search/", search_prompt, name="top_prompts"),
    path("prompts/view/<int:prompt_id>/", get_prompt, name="get_prompt"),
    path("prompts/like/<int:prompt_id>/", like_prompt, name="like_prompt"),
    path("prompts/comment/<int:prompt_id>/", comment_prompt, name="comment_prompt"),
    path("propmts/<int:pk>/", PromptDetailAPIView.as_view(), name="prompt_detail"),
    # This matches /tools/1/, /tools/2/, etc. and handles GET, PUT, PATCH and DELETE requests
]
