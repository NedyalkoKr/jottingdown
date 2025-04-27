from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, TemplateView, DetailView, UpdateView, DeleteView, CreateView, ListView
from core.models import Community


class FollowCommunityView(LoginRequiredMixin, View):

  def post(self, request, slug):
    community = get_object_or_404(Community, slug=slug)
    request.user.following_communities.add(community)
    # community.save()
    # messages.success(request, 'You are now following this community')

    if request.htmx:
      # Render the follow/unfollow button partial
      context = {'community': community, 'user': request.user}
      html = render_to_string('communities/partials/_follow_button.html', context)
      return HttpResponse(html)

    referer = request.META.get('HTTP_REFERER', '')
    if 'categories' in referer:
      return redirect('categories')
    return redirect('community', slug=slug)


class UnfollowCommunityView(LoginRequiredMixin, View):
  def post(self, request, slug):
    community = get_object_or_404(Community, slug=slug)
    request.user.following_communities.remove(community)
    # community.save()
    # messages.success(request, 'You are no longer following this community')
    if request.htmx:
      context = {'community': community, 'user': request.user}
      html = render_to_string('communities/partials/_follow_button.html', context)
      return HttpResponse(html)
    referer = request.META.get('HTTP_REFERER', '')
    if 'categories' in referer:
      return redirect('categories')
    return redirect('community', slug=slug)