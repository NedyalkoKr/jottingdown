from django.urls import path
from ..views import UnfollowCommunityView, UnfollowUserView


urlpatterns = [
  path(route='community/<slug:slug>/', view=UnfollowCommunityView.as_view(), name="unfollow_community"),
  path(route='user/<slug:slug>/', view=UnfollowUserView.as_view(), name='unfollow_user'),
]