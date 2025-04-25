from django.urls import path
from ..views import UserTopicsView, UserCommunitiesView


urlpatterns = [
  path(route='<str:username>/', view=UserTopicsView.as_view(), name="user_topics"),
  path(route='<str:username>/communities/', view=UserCommunitiesView.as_view(), name="user_communities"),
]