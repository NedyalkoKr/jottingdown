from django.db import models
from django_extensions.db.fields import RandomCharField
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.conf import settings
from tinymce import models as tinymce_models
from autoslug import AutoSlugField
from topics.models import Topic


class Comment(models.Model):

  comment_id = RandomCharField(length=64)
  slug = AutoSlugField(max_length=150, populate_from="comment_id", always_update=True, editable=False, null=True)
  topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  content = tinymce_models.HTMLField(blank=True, default="")
  created = models.DateTimeField(auto_now_add=True)
  search_vector = SearchVectorField(null=True)

  class Meta:
    db_table = "comments"
    verbose_name = "comment"
    verbose_name_plural = "comments"
    indexes = (GinIndex(fields=["search_vector"]),)

  def __str__(self):
    return f'{self.content}'