from django.urls import path
from ..views import CommunityView, CommunityLatestTopicsView, TopicDetailView


urlpatterns = [
  path(route='<slug:slug>/', view=CommunityView.as_view(), name='community'),
  path(route='<slug:slug>/latest-topics/', view=CommunityLatestTopicsView.as_view(), name='latest_community_topics'),
  path(route='<slug:slug>/topic/<int:topic_pk>/', view=TopicDetailView.as_view(), name='topic'),
]