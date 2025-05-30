import requests, bs4
from django.conf import settings
from tinymce import models as tinymce_models  
from django.db import models
from autoslug import AutoSlugField
from file_validator.models import DjangoFileValidator
from django_extensions.db.fields import RandomCharField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from core.models import Community


class Topic(models.Model):

  topic_id = RandomCharField(length=64)
  slug = AutoSlugField(populate_from="topic_id", always_update=True, editable=False, null=True)
  title = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
  user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  community = models.ForeignKey(to=Community, on_delete=models.CASCADE, null=True)
  content = tinymce_models.HTMLField(default="", blank=True)
  search_vector = SearchVectorField(null=True)
  image = models.ImageField(upload_to='images', null=True, blank=True,
    validators=[DjangoFileValidator(
    libraries=["filetype", "mimetypes",],
    acceptable_mimes=['image/jpeg', 'image/png', 'image/webp'], 
    acceptable_types=['image'],
    max_upload_file_size=5242880,
  )],)
  is_image = models.BooleanField(default=False)
  # is_question = models.BooleanField(default=False)
  
  class Meta:
    db_table = "topics"
    verbose_name = "topic"
    verbose_name_plural = "topics"
    ordering = ('-created',)
    indexes = (GinIndex(fields=["search_vector"]),)

  def __str__(self):
    return f'{self.title}'