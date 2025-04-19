from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
  list_display = ('title', 'community')
  search_fields = ('title', 'community__name')
  list_filter = ('community',)
  # list_per_page = 1
  # ordering = ('-created',)
  fieldsets = (
    ("", {"fields": ("title", "community", "user", "content")}),
  )