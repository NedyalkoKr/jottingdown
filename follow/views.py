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
    referer = request.META.get('HTTP_REFERER', '')
    if 'categories' in referer:
      return redirect('categories')
    return redirect('community', slug=slug)