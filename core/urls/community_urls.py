from django.urls import path
from ..views import CommunityView, CommunityLatestTopicsView


urlpatterns = [
  path('<slug:slug>/', CommunityView.as_view(), name='community'),
  path('<slug:slug>/latest-topics/', CommunityLatestTopicsView.as_view(), name='latest_community_topics'),
]