from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from core.models import Community
from .models import Topic
from .forms import TopicModelForm


class NewTopicView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

  form_class = TopicModelForm
  context_object_name = 'topic'
  http_method_names = ["get", "post",]
  template_name = 'topics/new_topic.html'
  permission_required = ('accounts.full_access_to_entire_platform',)

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