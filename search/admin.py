from django.contrib import admin
from .models import SavedSearch, SearchHistory, SearchCommunityHistory


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
  list_display = ["name",]
  readonly_fields = ("created", "slug",)
  fieldsets = (
    ('New saved search'),
    {
      'fields': ('user', 'name',)
    },
  ),

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
  list_display = ["query", "search_count"]
  readonly_fields = ("timestamp", "slug",)
  fieldsets = (
    ('New search history'),
    {
      'fields': ('query', 'user',)
    },
  ),


@admin.register(SearchCommunityHistory)
class SearchCommunityHistoryAdmin(admin.ModelAdmin):
  list_display = ["query", "count"]
  readonly_fields = ("created", "slug",)
  fieldsets = (
    ('New search query'),
    {
      'fields': ('query', 'community',)
    },
  ),
