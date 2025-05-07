from django.db import models
from django.conf import settings
from django_extensions.db.fields import RandomCharField
from autoslug import AutoSlugField
from topics.models import Topic


class TopicView(models.Model):

  topic_view_id = RandomCharField(length=64)
  slug = AutoSlugField(populate_from="topic_view_id", always_update=True, editable=False, null=True)
  topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, related_name='topic_views')
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  viewed_at = models.DateTimeField(auto_now_add=True)
  view_count = models.PositiveIntegerField(default=0)
  indexes = [
    models.Index(fields=['topic', 'user']),
  ]
  class Meta:
    db_table = "topic_views"
    verbose_name = "topic view"
    verbose_name_plural = "topic views"
    constraints = [
      models.UniqueConstraint(fields=['topic', 'user'], name='unique_topic_user_view')
    ]