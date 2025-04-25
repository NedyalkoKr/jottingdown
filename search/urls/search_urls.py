from django.urls import path, re_path
from ..views import SearchCommunityTopicsView, SearchAllTopicsView


urlpatterns = [
  path(route='community/<slug:slug>/topics/', view=SearchCommunityTopicsView.as_view(), name='search_community_topics'),
  path(route='topics/', view=SearchAllTopicsView.as_view(), name='search_all_topics'),
]