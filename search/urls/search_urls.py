from django.urls import path, re_path
from ..views import SearchCommunityTopicsView, SearchAllTopicsView, SearchesView, SearchUserTopicsView


urlpatterns = [
  path(route='community/<slug:slug>/topics/', view=SearchCommunityTopicsView.as_view(), name='search_community_topics'),
  path(route='topics/', view=SearchAllTopicsView.as_view(), name='search_all_topics'),
  path(route='history/', view=SearchesView.as_view(), name='searches'),
  path(route='<str:username>/topics/', view=SearchUserTopicsView.as_view(), name='search_user_topics'),
]