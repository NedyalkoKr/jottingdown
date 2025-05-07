from django.urls import path
from ..views import CommunityView, LatestCommunityTopicsView, TopicDetailView, PostsFromCommunityYouFollowView, CommunityPostsView, LatestCommunityPostsView, CommunityTopicsWithMostViews


urlpatterns = [
  path(route='<slug:slug>/', view=CommunityView.as_view(), name='community'),
  path(route='<slug:slug>/posts/', view=CommunityPostsView.as_view(), name='community_posts'),
  path(route='<slug:slug>/latest-topics/', view=LatestCommunityTopicsView.as_view(), name='latest_community_topics'),
  path(route='<slug:slug>/latest-posts/', view=LatestCommunityPostsView.as_view(), name='latest_community_posts'),
  path(route='<slug:slug>/topic/<int:topic_pk>/', view=TopicDetailView.as_view(), name='topic'),
  path(route='<slug:slug>/posts/foryou/', view=PostsFromCommunityYouFollowView.as_view(), name='posts_from_community_you_follow'),
  path(route='<slug:slug>/most-views/', view=CommunityTopicsWithMostViews.as_view(), name='community_topics_with_most_views'),
]