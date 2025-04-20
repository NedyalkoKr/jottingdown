from django.db import models
from django.conf import settings
from django_extensions.db.fields import RandomCharField
from autoslug import AutoSlugField


class Category(models.Model):

  name = models.CharField(max_length=100)
  slug = AutoSlugField(populate_from="name", always_update=True, editable=False, null=True)
  created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
  description = models.TextField(blank=True, null=True)
  followers = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='followed_categories', blank=True)

  class Meta:
    db_table = "categories"
    verbose_name = "category"
    verbose_name_plural = "categories"
    ordering = ('name',)
  
  def save(self, *args, **kwargs):
    self.name = self.name.lower()
    super(Category, self).save(*args, **kwargs)
  
  def __str__(self):
    return f'{self.name}'


class Community(models.Model):
  
  name = models.CharField(max_length=100)
  slug = AutoSlugField(populate_from="name", always_update=True, editable=False, null=True)
  created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
  description = models.TextField(blank=True, null=True)
  # followers = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='followed_communities', blank=True)
  category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='communities')

  class Meta:
    db_table = "communities"
    verbose_name = "community"
    verbose_name_plural = "communities"
  
  def save(self, *args, **kwargs):
    self.name = self.name.lower()
    super(Community, self).save(*args, **kwargs)
  
  def __str__(self):
    return f'{self.name}'