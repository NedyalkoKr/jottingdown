from django.urls import path
from ..views import UserTopicsView, UserCommunitiesView, FollowingUsersView


urlpatterns = [
  path(route='<str:username>/', view=UserTopicsView.as_view(), name="user_topics"),
  path(route='<str:username>/communities/', view=UserCommunitiesView.as_view(), name="user_communities"),
  path(route='<str:username>/following/', view=FollowingUsersView.as_view(), name="following_users"),
]