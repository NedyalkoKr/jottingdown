from django.http import HttpResponse
from django.urls import reverse, resolve, Resolver404
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
    if request.htmx:
      # Render the follow/unfollow button partial for HTMX
      context = {'community': community, 'user': request.user}
      html = render_to_string('communities/partials/_follow_button.html', context)
      return HttpResponse(html)
    # Redirect to appropriate URL for non-HTMX requests
    return redirect(self.get_success_url(slug))
  
  def get_success_url(self, slug):  
    # Try to resolve the HTTP_REFERER to determine the originating page
    referer = self.request.META.get('HTTP_REFERER')
    if referer:
        try:
            resolved = resolve(self.request.build_absolute_uri(referer))
            # Check if referer is the community page
            if resolved.url_name == 'community' and resolved.kwargs.get('slug'):
                return reverse('community', kwargs={'slug': resolved.kwargs['slug']})
            # Check if referer is the user_communities page
            elif resolved.url_name == 'user_communities' and resolved.kwargs.get('username'):
                return reverse('user_communities', kwargs={'username': resolved.kwargs['username']})
        except Resolver404:
            pass
    # Fallback to user_communities with the current user's username
    return reverse('user_communities', kwargs={'username': self.request.user.username})


class UnfollowCommunityView(LoginRequiredMixin, View):

  def post(self, request, slug):
    community = get_object_or_404(Community, slug=slug)
    request.user.following_communities.remove(community)
    if request.htmx:
        # Render the follow/unfollow button partial for HTMX
        context = {'community': community, 'user': request.user}
        html = render_to_string('communities/partials/_follow_button.html', context)
        return HttpResponse(html)
    # Redirect to appropriate URL for non-HTMX requests
    return redirect(self.get_success_url(slug))
  
  def get_success_url(self, slug):
    # Try to resolve the HTTP_REFERER to determine the originating page
    referer = self.request.META.get('HTTP_REFERER')
    if referer:
        try:
            resolved = resolve(self.request.build_absolute_uri(referer))
            # Check if referer is the community page
            if resolved.url_name == 'community' and resolved.kwargs.get('slug'):
                return reverse('community', kwargs={'slug': resolved.kwargs['slug']})
            # Check if referer is the user_communities page
            elif resolved.url_name == 'user_communities' and resolved.kwargs.get('username'):
                return reverse('user_communities', kwargs={'username': resolved.kwargs['username']})
        except Resolver404:
            pass
    # Fallback to user_communities with the current user's username
    return reverse('user_communities', kwargs={'username': self.request.user.username})