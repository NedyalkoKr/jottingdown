from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
  list_display = ('title', 'community_link',)
  search_fields = ('title', 'community__name')
  list_filter = ('created',)
  # list_per_page = 1
  # ordering = ('-created',)
  fieldsets = (
    ("", {"fields": ("title", "community", "user", "content", "image", "is_image",)}),
  )

  def community_link(self, obj):
    if obj.community:
      url = (
        reverse('admin:topics_topic_changelist')
        + f'?community__id__exact={obj.community.id}'
      )
      return format_html('<a href="{}">{}</a>', url, obj.community.name)
    return '-'
  community_link.short_description = 'Community'