from django.urls import path
from ..views import SearchCommunityTopicsView, SearchAllTopicsView, SearchesView, SearchUserTopicsView, NewSavedSearchFromKeywordView, SavedSearchesView, DeleteSavedSearchView, NewSavedSearchView


urlpatterns = [
  path(route='topics/g/', view=SearchAllTopicsView.as_view(), name='search_all_topics'),
  path(route='history/', view=SearchesView.as_view(), name='searches'),
  path(route='topics/', view=SearchUserTopicsView.as_view(), name='search_user_topics'),
  path(route='<slug:slug>/keyword/new/', view=NewSavedSearchFromKeywordView.as_view(), name='new_saved_search_from_keyword'),
  path(route='saved/', view=SavedSearchesView.as_view(), name='saved_searches'),
  path(route='q/<slug:slug>/delete/', view=DeleteSavedSearchView.as_view(), name='delete_saved_search'),
  path(route='<str:search_query>/new/', view=NewSavedSearchView.as_view(), name='new_saved_search'),
  path(route='community/<slug:slug>/topics/', view=SearchCommunityTopicsView.as_view(), name='search_community_topics'),
]