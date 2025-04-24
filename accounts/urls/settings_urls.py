from django.urls import path
from ..views import UserProfileSettingsUpdateView, UserPasswordChangeView


urlpatterns = [
  path(route='<str:username>/', view=UserProfileSettingsUpdateView.as_view(), name="user_settings"),
  path(route='<str:username>/password-change/', view=UserPasswordChangeView.as_view(), name='password_change'),
]