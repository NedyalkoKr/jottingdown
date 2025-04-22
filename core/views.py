from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Category, Community
from topics.models import Topic


class CategoriesView(LoginRequiredMixin, ListView):
  
  http_method_names = ["get", "post",]
  context_object_name = 'categories'
  template_name = 'categories/categories.html'

  def get_queryset(self):
    categories = Category.objects.prefetch_related('communities').prefetch_related('communities__topic_set').prefetch_related('communities__followed_communities').prefetch_related('communities')
    return categories


class CommunityView(LoginRequiredMixin, DetailView):

  model = Community
  template_name = 'communities/community.html'
  context_object_name = 'community'

  def get_object(self):
    community = Community.objects.prefetch_related('topic_set__user').get(slug=self.kwargs['slug'])
    return community
  
  # def get_context_data(self, **kwargs):
  #   context['posts'] = Post.objects.prefetch_related('comments').prefetch_related('context').prefetch_related('community').prefetch_related('user').filter(community=self.object)
  #   return context


class CommunityLatestTopicsView(LoginRequiredMixin, DetailView):

  model = Topic
  template_name = 'communities/latest_community_topics.html'
  context_object_name = 'topics'

  def get_object(self):
    topics = Topic.objects.filter(community=Community.objects.get(slug=self.kwargs['slug'])).filter(created__day=timezone.now().day, created__month=timezone.now().month, created__year=timezone.now().year)
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context