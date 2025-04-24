from django.urls import path
from ..views import UserTopicsView


urlpatterns = [
  path(route='<str:username>/', view=UserTopicsView.as_view(), name="user_topics"),
]