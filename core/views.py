from datetime import timedelta
from django.utils import timezone
from django.db.models import F, Count
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django_extensions.db.fields import RandomCharField
from django.views.generic import ListView, DetailView
from .models import Category, Community
from topics.models import Topic
from analytics.models import TopicView
from topics.forms import TopicModelForm


class CategoriesView(LoginRequiredMixin, ListView):
  
  http_method_names = ["get", "post",]
  context_object_name = 'categories'
  template_name = 'categories/categories.html'

  def get_queryset(self):
    return Category.objects.prefetch_related(
      'communities__topic_set',
      'communities__followed_communities'
    ).distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['followed_communities'] = self.request.user.following_communities.all()
    return context
  

class CommunityView(LoginRequiredMixin, ListView):

  http_method_names = ["get",]
  context_object_name = 'topics'
  template_name = 'communities/community.html'

  def get_queryset(self):
    community = Community.objects.prefetch_related('topic_set__user').get(slug=self.kwargs['slug'])
    topics = Topic.objects.filter(community=community).exclude(user=self.request.user)
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context


class CommunityPostsView(LoginRequiredMixin, ListView):

  http_method_names = ["get",]
  context_object_name = 'posts'
  template_name = 'communities/community_posts.html'

  def get_queryset(self):
    community = Community.objects.prefetch_related('topic_set__user').get(slug=self.kwargs['slug'])
    posts = Topic.objects.filter(community=community).exclude(user=self.request.user)
    return posts

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context


class LatestCommunityTopicsView(LoginRequiredMixin, ListView):

  http_method_names = ["get",]
  context_object_name = 'topics'
  template_name = 'communities/latest_community_topics.html'

  def get_queryset(self):
    community = Community.objects.get(slug=self.kwargs['slug'])
    topics = Topic.objects.filter(community=community).filter(created__day=timezone.now().day, created__month=timezone.now().month, created__year=timezone.now().year).exclude(user=self.request.user)
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context


class LatestCommunityPostsView(LoginRequiredMixin, ListView):

  http_method_names = ["get",]
  context_object_name = 'posts'
  template_name = 'communities/latest_community_posts.html'

  def get_queryset(self):
    community = get_object_or_404(Community, slug=self.kwargs["slug"])
    today = timezone.now().date()
    start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)
    queryset = Topic.objects.filter(
      community=community,
      created__gte=start_of_day,
      created__lt=end_of_day
    ).exclude(user=self.request.user)
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["community"] = get_object_or_404(Community, slug=self.kwargs["slug"])
    return context


class TopicDetailView(LoginRequiredMixin, DetailView):

  model = Topic
  http_method_names = ["get", "post",]
  context_object_name = 'topic'
  template_name = 'topics/topic.html'

  def get_object(self):
    community = get_object_or_404(Community, slug=self.kwargs['slug'])
    topic = get_object_or_404(
      Topic,
      community=community,
      pk=self.kwargs['topic_pk']
    )

    with transaction.atomic():
      TopicView.objects.get_or_create(
        topic=topic,
        user=self.request.user,
        defaults={'view_count': 1}
      )
    return topic


class CategoryView(LoginRequiredMixin, DetailView):
  
  http_method_names = ["get",]
  context_object_name = 'category'
  template_name = 'categories/category.html'

  def get_object(self):
    category = Category.objects.get(slug=self.kwargs['slug'])
    return category
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    communities = Community.objects.filter(category=self.object)
    context['communities'] = communities
    context['topics'] = Topic.objects.prefetch_related('user').prefetch_related('community').filter(community__in=communities).exclude(user=self.request.user)
    return context


class CommunitiesYouFollowView(LoginRequiredMixin, ListView):
  
  http_method_names = ["get", "post",]
  context_object_name = 'communities'
  template_name = 'communities/communities_you_follow.html'

  def get_queryset(self):
    user = self.request.user
    communities = Community.objects.filter(followed_communities=user)
    return communities


class PostsFromCommunityYouFollowView(LoginRequiredMixin, ListView):
  
  http_method_names = ["get",]
  context_object_name = 'posts'
  template_name = 'communities/posts_from_community_you_follow.html'

  def get_queryset(self):
    community = Community.objects.get(slug=self.kwargs['slug'])
    posts = Topic.objects.filter(community=community).order_by('-created').exclude(user=self.request.user)
    return posts
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context
  

class CommunityTopicsWithMostViews(LoginRequiredMixin, ListView):

  http_method_names = ['get',]
  context_object_name = 'topics'
  template_name = "topics/community_topics_most_views.html"

  def get_queryset(self):
    user = self.request.user
    community = Community.objects.get(slug=self.kwargs['slug'])
    topics = Topic.objects.filter(community=community).exclude(user=user).order_by('topic_views__view_count')
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context