from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, DeletedUser


@admin.register(DeletedUser)
class DeletedUserAdmin(admin.ModelAdmin):
  list_display = ("username", "email", "deleted_at",)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = CustomUser
  list_display = ("username", "is_active", "date_joined", 'days_since_joined',)
  list_display_links = ["username"]
  list_filter = ("is_active", "date_joined",)
  search_fields = ("username", "email",)
  ordering = ("username",)
  # actions = ['delete_inactive_users']
  actions_on_top = True
  actions_selection_counter = True
  list_per_page = 10
  date_hierarchy = "date_joined"
  filter_horizontal = ('groups', 'user_permissions', 'following_communities', 'followers', 'following')

  fieldsets = (
    ("User details", {"fields": ("username", "email", "password")}),
    ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions",)}),
    ("Following communities", {"fields": ("following_communities",)}),
    ("Followers", {"fields": ("followers",)}),
    ("Following", {"fields": ("following",)}),
  )

  add_fieldsets = (
    ("Create new user", {
      "classes": ("wide",),
      "fields": (
        "username", "email", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions",)
    }),
  )

  def days_since_joined(self, obj):
    delta = timezone.now().date() - obj.date_joined.date()
    return delta.days
  days_since_joined.short_description = 'Days Since Joined'
