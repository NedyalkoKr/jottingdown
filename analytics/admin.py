from django.contrib import admin
from .models import TopicView


admin.site.register(TopicView)
class TopicViewAdmin(admin.ModelAdmin):
  list_display = ('topic', 'user', 'viewed_at', 'view_count')
  list_filter = ('topic', 'user',)
  search_fields = ('topic', 'user')
  ordering = ('-viewed_at',)


