from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordChangeView, PasswordChangeDoneView, PasswordResetCompleteView
from topics.models import Topic
from core.models import Community
from search.forms import NewSavedSearchFromKeywordModelForm
from .forms import UserProfileSettingsChangeForm, UserPasswordChangeForm, UserLoginForm
User = get_user_model()


class UserLoginView(LoginView):

  form_class = UserLoginForm
  http_method_names = ["get", "post"]
  redirect_authenticated_user = True
  template_name = "users/account/user_login.html"

  def get_success_url(self):
    return reverse('user_topics', kwargs={'username': self.request.user.username })

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['dev_or_prod'] = settings.DEBUG
    # context['GOOGLE_OAUTH_CLIENT_ID'] = settings.GOOGLE_OAUTH_CLIENT_ID
    # context['GOOGLE_LOGIN_URI'] = settings.GOOGLE_LOGIN_URI
    return context


class UserLogoutView(LogoutView):
  next_page = 'user_login'
  template_name = None


class UserTopicsView(LoginRequiredMixin, ListView):

  http_method_names = ["get",]
  context_object_name = 'topics'
  template_name = 'topics/user_topics.html'

  def get_queryset(self):
    topics = Topic.objects.prefetch_related('community').filter(user=self.request.user).order_by('-created')
    return topics


class FollowingUsersView(LoginRequiredMixin, ListView):
  
  http_method_names = ["get",]
  context_object_name = 'following_users'
  template_name = 'users/profile/following_users.html'
  
  def get_queryset(self):
    following_users = self.request.user.following.all()
    return following_users


class UserCommunitiesView(LoginRequiredMixin, ListView):

  context_object_name = 'communities'
  http_method_names = ["get", "post",]
  template_name = 'communities/user_communities.html'

  def get_queryset(self):
    communities = Community.objects.filter(followed_communities=self.request.user).order_by('name')
    return communities


class UserProfileSettingsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):

  model = User
  form_class = UserProfileSettingsChangeForm
  success_message = 'Profile updated successfully.'
  template_name = "users/profile/profile_settings.html"
  http_method_names = ["get", "post",]
  permission_denied_message = 'Profile is private'

  def get_object(self):
    user = User.objects.get(username=self.kwargs['username'])
    return user

  def test_func(self):
    user = get_object_or_404(klass=User, username=self.kwargs.get('username'))
    if self.request.user.username == user.username:
      return True
    return False

  def get_success_url(self):
    return reverse('user_settings', kwargs={'username': self.request.user })


class UserPasswordChangeView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, PasswordChangeView):

  form_class = UserPasswordChangeForm
  http_method_names = ['get', 'post',]
  template_name = 'users/security/change_password.html'
  success_message = 'Password change was successful. Login with your new password.'
  permission_required = ('accounts.full_access_to_entire_platform',)

  # def handle_no_permission(self):
  #   return HttpResponseRedirect(reverse('billing', kwargs={'username': self.request.user}))

  @method_decorator(sensitive_post_parameters('old_password', 'new_password1', 'new_password2',))
  @method_decorator(csrf_protect)
  @method_decorator(never_cache)
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)
  
  def test_func(self):
    user = get_object_or_404(klass=User, username=self.kwargs.get('username'))
    if self.request.user.username == user.username:
      return True
    return False
  
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request  # Pass request to form
    return kwargs

  def form_valid(self, form):
    # Store the username before logout
    username = self.request.user.username
    # Save the password change
    response = super().form_valid(form)
    # Log the user out
    logout(self.request)
    # Redirect to logout URL with the stored username
    return HttpResponseRedirect(reverse('user_logout', kwargs={'username': username}))

  def get_success_url(self):
    username = self.request.user.username
    return reverse_lazy('user_logout', kwargs={'username': username})