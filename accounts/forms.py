from django import forms
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from .models import PasswordChangeLog
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ("email", "username",)


class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = User
    fields = ("email", "username",)
  

class UserProfileSettingsChangeForm(forms.ModelForm):
  
  error_messages = {'name_exist': ('name already exist'),}

  username = forms.CharField(
    min_length=3, max_length=30, required=True, strip=True, disabled=True,
    widget=forms.TextInput(
      attrs={
        "autocomplete": "off",
        "class": "form-control form-control-md",
        "autofocus": False,
      }
    ),
    help_text="Username cannot be changed.",
  )

  email = forms.EmailField(max_length=254, required=True, disabled=True, 
    widget=forms.EmailInput(
      attrs={
        "autocomplete": "off",
        "class": "form-control form-control-md",
        "autofocus": False,
      }
    ),
    help_text="This is the primary email for this account. You can't change it.",
  )

  bio = forms.CharField(max_length="230", required=False, label="About you", help_text="Something about yourself.", widget=forms.Textarea({"rows": "4"}))

  class Meta:
    model = User
    fields = ("username", "email", "bio", "avatar", "x_link", "website_link", "newsletter_link", "yt_link", "github_link",)


class UserPasswordChangeForm(PasswordChangeForm):

  error_messages = {
    'password_incorrect': ('Your old password was entered incorrectly. Please enter it again.'),
    'password_mismatch': ('The two password fields didn\'t match.'),
    'same_password_as_old': ('Can\'t use the old password as a new password.'),
    'same_as_username': ('Can\'t use username as a new password.'),
  }

  old_password = forms.CharField(
    label="Old password",
    min_length=settings.PASSWORD_MIN_LENGTH,
    max_length=settings.PASSWORD_MAX_LENGTH,
    required=True, strip=True,
    help_text="Type in your current password.",
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        "class": "form-control form-control-md",  
        "autofocus": False,
        "autocomplete": "off",
      }
    ),
  )

  new_password1 = forms.CharField(
    label="New Password",
    required=True, strip=True,
    min_length=settings.PASSWORD_MIN_LENGTH,
    max_length=settings.PASSWORD_MAX_LENGTH,
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        "class": "form-control form-control-md",
        "autofocus": False,
        "autocomplete": "new-password",
      }
    ),
    help_text=password_validation.password_validators_help_text_html(),
  )

  new_password2 = forms.CharField(
    label="Password Again",
    help_text="Type in again your new password to confirm it.",
    required=True, strip=True,
    min_length=settings.PASSWORD_MIN_LENGTH,
    max_length=settings.PASSWORD_MAX_LENGTH,
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        "class": "form-control form-control-md",
        "autofocus": False,
        "autocomplete": "new-password",
      }
    )
  )

  def clean_new_password1(self):
    old_password = self.cleaned_data.get("old_password")
    new_password1 = self.cleaned_data.get("new_password1")
    username = self.user.username
    if new_password1 == old_password:
      raise ValidationError(
        self.error_messages['same_password_as_old'],
        code='same_password_as_old',
      )
    if new_password1 == username:
      raise ValidationError(
        self.error_messages['same_as_username'],
        code='same_as_username',
      )
    return new_password1
  
  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop('request', None)  # Pop request if it exists
    super().__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super().clean()
    
    # Check last password change
    last_change = PasswordChangeLog.objects.filter(user=self.user).order_by('-timestamp').first()
    if last_change:
      time_since_last_change = timezone.now() - last_change.timestamp
      if time_since_last_change < timedelta(days=1):
        time_remaining = timedelta(days=1) - time_since_last_change
        hours_remaining = int(time_remaining.total_seconds() // 3600)
        minutes_remaining = int((time_remaining.total_seconds() % 3600) // 60)
        raise ValidationError(
          f"You can only change your password once per day. "
          f"Please wait {hours_remaining} hours and {minutes_remaining} minutes."
        )
    return cleaned_data

  def save(self, commit=True):
    user = super().save(commit=commit)
    if commit and self.request:
      PasswordChangeLog.objects.create(user=user,)
    return user


class UserLoginForm(AuthenticationForm):

  username = forms.EmailField(
    max_length=64, required=True,
    widget=forms.EmailInput(
      attrs={
        "autocomplete": "off",
        "class": "form-control form-control-lg",
        "autofocus": False,
        "data-bs-container": "body",
        "data-bs-toggle": "popover",
        "data-bs-trigger": "hover",
        "data-bs-placement": "right",
        "data-bs-content": "Enter the email you have used to sign up.",
      } 
    ),
  )
  password = forms.CharField(
    min_length=12, max_length=settings.PASSWORD_MAX_LENGTH, required=True, strip=True,
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        "autocomplete": "off",
        "class": "form-control form-control-lg",
        "data-bs-container": "body",
        "data-bs-placement": "right",
        "data-bs-toggle": "popover",
        "data-bs-trigger": "hover",
        "data-bs-content": "Enter your password.",
      },
    ),
  )