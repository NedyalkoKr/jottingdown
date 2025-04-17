from django.urls import path
from ..views import CommunityView


urlpatterns = [
  path('<slug:slug>/', CommunityView.as_view(), name='community'),
]