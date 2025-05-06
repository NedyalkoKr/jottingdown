from django.urls import path
from ..views import FollowCommunityView, FollowPeopleView, FollowUserView, FollowingUsersView


urlpatterns = [
  path(route='people/', view=FollowPeopleView.as_view(), name='follow_people'),
  path(route='community/<slug:slug>/', view=FollowCommunityView.as_view(), name='follow_community'),
  path(route='user/<slug:slug>/', view=FollowUserView.as_view(), name='follow_user'),
  path(route='following/', view=FollowingUsersView.as_view(), name='following_users'),
]