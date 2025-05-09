from django.shortcuts import render
from django.db.models import F, Func
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from core.models import Community
from .models import Topic
from analytics.models import TopicView  
from .forms import TopicModelForm, NewMediaTopicModelForm


class NewTopicView(LoginRequiredMixin, CreateView):

  form_class = TopicModelForm
  context_object_name = 'topic'
  http_method_names = ["get", "post",]
  template_name = 'topics/new_topic.html'
  # permission_required = ('accounts.full_access_to_entire_platform',)

  def form_valid(self, form):
    instance = form.save(commit=False)
    form.instance.user = self.request.user
    form.instance.community = Community.objects.get(slug=self.kwargs['slug'])
    form.save()
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context
  
  def get_success_url(self, **kwargs):
    return reverse_lazy('new_topic', kwargs={'slug': self.kwargs['slug']})


class UpdateTopicView(LoginRequiredMixin, UpdateView):

  model = Topic
  form_class = TopicModelForm
  context_object_name = 'topic'
  http_method_names = ["get", "post",]
  template_name = 'topics/update_topic.html'
  # permission_required = ('accounts.full_access_to_entire_platform',)

  def get_object(self):
    topic = Topic.objects.get(user=self.request.user, slug=self.kwargs['slug'])
    return topic

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['topics'] = Topic.objects.prefetch_related('community').filter(user=self.request.user).order_by('-created')
    return context
  
  def get_success_url(self, **kwargs):
    return self.request.META.get('HTTP_REFERER', reverse_lazy('user_topics', kwargs={'username': self.request.user.username}))


class TopicDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

  context_object_name = 'topic'
  permission_required = ('accounts.full_access_to_entire_platform',)
  http_method_names = ["get", "post"]
  
  def handle_no_permission(self):
    return HttpResponseRedirect(reverse('billing', kwargs={'username': self.request.user}))

  def get_object(self):
    topic = Topic.objects.get(user=self.request.user, slug=self.kwargs['slug'])
    return topic

  def post(self, request, *args, **kwargs):
    topic = Topic.objects.get(user=self.request.user, slug=self.kwargs['slug'])
    topic.delete()

    if request.headers.get('HX-Request'):
      topics = Topic.objects.prefetch_related('community').filter(user=self.request.user).order_by('-created')
      return render(request, 'topics/partials/u_topics.html', {'topics': topics})
    else:
      return HttpResponseRedirect(self.get_success_url())


class PostsForYouBasedOnCommunitiesYouFollowView(LoginRequiredMixin, ListView):

  http_method_names = ['get',]
  context_object_name = 'topics'
  template_name = "topics/posts_for_you_based_on_communities_you_follow.html"

  def get_queryset(self):
    user = self.request.user
    user_following_communities = user.following_communities.all()
    topics = Topic.objects.prefetch_related('community').prefetch_related('user').filter(community__in=user_following_communities).order_by('-created').exclude(user=self.request.user)
    return topics


class TopicsForYouBasedOnCommunitiesYouFollowView(LoginRequiredMixin, ListView):

  http_method_names = ['get',]
  context_object_name = 'topics'
  template_name = "topics/topics_for_you_based_on_communities_you_follow.html"

  def get_queryset(self):
    user = self.request.user
    user_following_communities = user.following_communities.all()
    topics = Topic.objects.prefetch_related('community').prefetch_related('user').filter(community__in=user_following_communities).order_by('-created').exclude(user=self.request.user)
    return topics


class RandomTopicListView(LoginRequiredMixin, ListView):

  http_method_names = ['get',]
  context_object_name = 'topics'
  template_name = "topics/random_topics.html"

  def get_queryset(self):
    topics = Topic.objects.order_by(Func(function='RANDOM'))
    return topics


class NewMediaTopicView(LoginRequiredMixin, CreateView):

  form_class = NewMediaTopicModelForm
  http_method_names = ["get", "post",]
  template_name = 'topics/new_media_topic.html'
  # permission_required = ('accounts.full_access_to_entire_platform',)

  def form_valid(self, form):
    instance = form.save(commit=False)
    form.instance.user = self.request.user
    form.instance.community = Community.objects.get(slug=self.kwargs['slug'])
    form.instance.is_image = True
    form.save()
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context
  
  def get_success_url(self, **kwargs):
    return reverse_lazy('new_media_topic', kwargs={'slug': self.kwargs['slug']})