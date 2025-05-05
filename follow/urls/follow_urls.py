from django.urls import path
from ..views import FollowCommunityView, FollowPeopleView, FollowUserView


urlpatterns = [
  path('community/<slug:slug>/', FollowCommunityView.as_view(), name='follow_community'),
  path('people/', FollowPeopleView.as_view(), name='follow_people'),
  path('user/<slug:slug>/', FollowUserView.as_view(), name='follow_user'),
]