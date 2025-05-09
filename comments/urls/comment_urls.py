from django.urls import path
from ..views import NewCommentView


urlpatterns = [
  path(route='topic/<slug:slug>/', view=NewCommentView.as_view(), name="new_comment"),
]