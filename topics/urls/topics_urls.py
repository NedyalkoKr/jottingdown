from django.urls import path
from ..views import TopicsForYouBasedOnCommunitiesYouFollowView


urlpatterns = [
  path(route='foryou/', view=TopicsForYouBasedOnCommunitiesYouFollowView.as_view(), name='topics_foryou_based_on_communities_you_follow'),
]