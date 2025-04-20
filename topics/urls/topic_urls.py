from django.urls import path
from ..views import NewTopicView


urlpatterns = [
  path('community/<str:slug>/new/', NewTopicView.as_view(), name='new_topic'),
]