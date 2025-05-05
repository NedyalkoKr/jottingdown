from django.urls import path
from ..views import CategoriesView, CommunitiesYouFollowView


urlpatterns = [
  path('', CategoriesView.as_view(), name='communities'),
  path('foryou/', CommunitiesYouFollowView.as_view(), name='communities_you_follow'),
]