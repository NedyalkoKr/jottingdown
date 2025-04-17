from django.conf import settings
from django.db import models
from django_extensions.db.fields import RandomCharField
from core.models import Community


class Topic(models.Model):

  topic_id = RandomCharField(length=64)
  title = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  community = models.ForeignKey(to=Community, on_delete=models.CASCADE, null=True)

  class Meta:
    db_table = "topics"
    verbose_name = "topic"
    verbose_name_plural = "topics"
    ordering = ('-created',)

  def __str__(self):
    return f'{self.title}'