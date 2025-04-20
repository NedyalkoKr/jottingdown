from django.urls import path
from ..views import UnfollowCommunityView


urlpatterns = [
  path(route='community/<slug:slug>/', view=UnfollowCommunityView.as_view(), name="unfollow_community"),
]