from django.urls import path
from ..views import NewTopicView, TopicDetailView, TopicDeleteView, UpdateTopicView


urlpatterns = [
  path(route='community/<slug:slug>/new/', view=NewTopicView.as_view(), name='new_topic'),
  path(route='topic/<slug:slug>/update/', view=UpdateTopicView.as_view(), name='update_topic'),
  path(route='<slug:slug>/topic/<int:topic_pk>/', view=TopicDetailView.as_view(), name='topic'),
  path(route='<str:username>/topic/<slug:slug>/delete/', view=TopicDeleteView.as_view(), name="delete_topic"),
]