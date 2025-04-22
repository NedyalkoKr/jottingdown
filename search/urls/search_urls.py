from django.urls import path, re_path
from ..views import SearchCommunityTopicsView


urlpatterns = [
  path(route='community/<slug:slug>/topics/', view=SearchCommunityTopicsView.as_view(), name='search_community_topics'),
]