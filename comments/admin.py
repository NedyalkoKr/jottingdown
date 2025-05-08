from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('comment_id', 'topic', 'user', 'created')

