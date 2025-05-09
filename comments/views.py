from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView
from .models import Comment
from .forms import CommentModelForm



class NewCommentView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    
  model = Comment
  form_class = CommentModelForm
  template_name = 'comments/new_comment.html'
  context_object_name = 'comment'
  http_method_names = ["get", "post",]
  permission_required = ('accounts.full_access_to_entire_platform',)
