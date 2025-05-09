from django.urls import path
from ..views import NewTopicView, TopicDeleteView, UpdateTopicView, NewMediaTopicView


urlpatterns = [
  path(route='community/<slug:slug>/new/', view=NewTopicView.as_view(), name='new_topic'),
  path(route='community/<slug:slug>/media/', view=NewMediaTopicView.as_view(), name='new_media_topic'),
  path(route='topic/<slug:slug>/update/', view=UpdateTopicView.as_view(), name='update_topic'),
  path(route='<str:username>/topic/<slug:slug>/delete/', view=TopicDeleteView.as_view(), name="delete_topic"),
]