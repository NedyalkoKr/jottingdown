from django.urls import path
from ..views import CategoriesView, CommunitiesYouFollowView


urlpatterns = [
  path(route='', view=CategoriesView.as_view(), name='communities'),
  path(route='you-follow/', view=CommunitiesYouFollowView.as_view(), name='communities_you_follow'),
]