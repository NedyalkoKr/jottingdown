from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Category, Community


class CategoriesView(LoginRequiredMixin, ListView):
  
  http_method_names = ["get", "post",]
  context_object_name = 'categories'
  template_name = 'categories/categories.html'

  def get_queryset(self):
    categories = Category.objects.prefetch_related('communities').prefetch_related('communities__followers')
    return categories


class CommunityView(LoginRequiredMixin, DetailView):
  model = Community
  template_name = 'communities/community.html'
  context_object_name = 'community'

  def get_object(self):
    community = Community.objects.get(slug=self.kwargs['slug'])
    return community
  
  # def get_context_data(self, **kwargs):
  #   context['posts'] = Post.objects.prefetch_related('comments').prefetch_related('context').prefetch_related('community').prefetch_related('user').filter(community=self.object)
  #   return context