from django.urls import path
from ..views import NewTopicView, TopicDetailView


urlpatterns = [
  path('community/<slug:slug>/new/', NewTopicView.as_view(), name='new_topic'),
  path('<slug:slug>/topic/<int:topic_pk>/', TopicDetailView.as_view(), name='topic'),
]