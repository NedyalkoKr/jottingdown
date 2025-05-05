from django.urls import path
from ..views import PostsForYouBasedOnCommunitiesYouFollowView


urlpatterns = [
  path(route='foryou/', view=PostsForYouBasedOnCommunitiesYouFollowView.as_view(), name='posts_foryou_based_on_communities_you_follow'),
]