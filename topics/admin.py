from django.contrib import admin
from .models import Topic, TopicView


@admin.register(TopicView)
class TopicViewAdmin(admin.ModelAdmin):
  list_display = ('topic',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
  list_display = ('title', 'community', 'views', 'slug',)
  search_fields = ('title', 'community__name')
  list_filter = ('community',)
  # list_per_page = 1
  # ordering = ('-created',)
  fieldsets = (
    ("", {"fields": ("title", "community", "user", "views", "content",)}),
  )