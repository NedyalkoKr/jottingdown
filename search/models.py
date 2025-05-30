from django.db import models
from django.conf import settings
from django_extensions.db.fields import RandomCharField
from autoslug import AutoSlugField
from core.models import Community


class SavedSearch(models.Model):
  
  search_id = RandomCharField(length=64)
  slug = AutoSlugField(populate_from="search_id", always_update=True, editable=False, null=True)
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  created = models.DateTimeField(auto_now_add=True, null=True)
  name = models.CharField(max_length=300, blank=True, default='')

  class Meta:
    db_table = 'saved_searches'
    verbose_name = "saved search"
    verbose_name_plural = "saved searches"

  def save(self, *args, **kwargs):
    self.name = self.name.lower()
    super(SavedSearch, self).save(*args, **kwargs)


class SearchHistory(models.Model):

  search_history_id = RandomCharField(length=64)
  slug = AutoSlugField(populate_from="search_history_id", always_update=True, editable=False, null=True)  
  query = models.CharField(max_length=255)
  timestamp = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history', null=True)
  search_count = models.PositiveIntegerField(default=0)

  class Meta:
    ordering = ['-timestamp']
    db_table = 'search_history'
    verbose_name = "search history"
    verbose_name_plural = "search history"
    unique_together = ('user', 'query')

  def save(self, *args, **kwargs):
    self.query = self.query.lower()
    super(SearchHistory, self).save(*args, **kwargs)

  def __str__(self):
    return f"{self.query}"


class SearchCommunityHistory(models.Model):

  search_community_history_id = RandomCharField(length=64)
  slug = AutoSlugField(populate_from="search_community_history_id", always_update=True, editable=False, null=True)  
  community = models.ForeignKey(to=Community, on_delete=models.CASCADE, related_name='search_history')
  query = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True, db_index=True)
  count = models.PositiveIntegerField(default=1)

  class Meta:
    verbose_name = 'Search Community History'
    verbose_name_plural = 'Search Community Histories'
    unique_together = ['community', 'query']
    ordering = ['-created']

  def __str__(self):
    return f"Search: {self.query} in {self.community.name}"
  
  @classmethod
  def save_search(cls, community, query, has_results):
    if has_results:
      search, created = cls.objects.get_or_create(
        community=community,
        query=query,
        defaults={'count': 1}
      )
      if not created:
        search.count += 1
        search.save()
      return search
    return None