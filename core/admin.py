from django.contrib import admin
from .models import Category, Community
from topics.models import Topic


class CommunityInline(admin.TabularInline):
  model = Community
  extra = 1
  fields = ('name', 'description')


class TopicInline(admin.TabularInline):
  model = Topic
  extra = 1
  fields = ('title', 'user',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  inlines = [CommunityInline]
  list_display = ('name',)
  search_fields = ('name',)
  list_filter = ('created',)
  filter_horizontal = ["followers",] 


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
  inlines = [TopicInline]
  list_display = ('name',)
  search_fields = ('name',)
  list_filter = ('created',)
  readonly_fields = ('created', 'slug',)
  fieldsets = (
    ("Community", {
      "fields": (
        "name", "category", "description",
      )}
    ),
  )

