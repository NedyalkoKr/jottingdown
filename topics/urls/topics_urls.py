from django.urls import path
from ..views import TopicsForYouBasedOnCommunitiesYouFollowView, RandomTopicListView


urlpatterns = [
  path(route='foryou/', view=TopicsForYouBasedOnCommunitiesYouFollowView.as_view(), name='topics_foryou_based_on_communities_you_follow'),
  path(route='random/', view=RandomTopicListView.as_view(), name='random_topics'),
]