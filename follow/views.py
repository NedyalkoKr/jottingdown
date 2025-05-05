from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse, resolve, Resolver404
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, TemplateView, DetailView, UpdateView, DeleteView, CreateView, ListView
from core.models import Community
User = get_user_model()


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


class FollowPeopleView(LoginRequiredMixin, ListView):

  http_method_names = ["get",]
  context_object_name = 'users_to_follow'
  template_name = "users/follow/follow_people.html"
  # permission_required = ('accounts.full_access_to_entire_platform',)
  
  # def handle_no_permission(self):
  #   return HttpResponseRedirect(reverse('billing', kwargs={'username': self.request.user}))

  def get_queryset(self):
    users_to_follow = User.objects.exclude(username=self.request.user)
    return users_to_follow


class FollowUserView(LoginRequiredMixin, View):

  def post(self, request, slug):
    user_to_follow = get_object_or_404(User, slug=slug)
    
    # Prevent users from following themselves
    if request.user == user_to_follow:
      if request.htmx:
        context = {'user_to_follow': user_to_follow, 'user': request.user}
        html = render_to_string('users/partial/_user_row.html', context)
        return HttpResponse(html)
      referer = request.META.get('HTTP_REFERER', '')
      return redirect(referer or 'follow_people')

    # Add user_to_follow to request.user's following
    request.user.following.add(user_to_follow)
    
    if request.htmx:
      context = {'user_to_follow': user_to_follow, 'user': request.user}
      html = render_to_string('users/partial/_user_row.html', context)
      return HttpResponse(html)
    
    referer = request.META.get('HTTP_REFERER', '')
    return redirect(referer or 'follow_people')


class UnfollowUserView(LoginRequiredMixin, View):

  def post(self, request, slug):
    user_to_unfollow = get_object_or_404(User, slug=slug)
    # Remove user_to_unfollow from request.user's following
    request.user.following.remove(user_to_unfollow)
    
    if request.htmx:
      context = {'user_to_follow': user_to_unfollow, 'user': request.user}
      html = render_to_string('users/partial/_user_row.html', context)
      return HttpResponse(html)
    
    referer = request.META.get('HTTP_REFERER', '')
    return redirect(referer or 'follow_people')