from django.urls import path
from ..views import FollowCommunityView


urlpatterns = [
  path('community/<slug:slug>/', FollowCommunityView.as_view(), name='follow_community'),
]