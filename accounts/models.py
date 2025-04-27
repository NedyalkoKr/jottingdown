from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinLengthValidator
from validators.account_validators import validate_not_all_numbers
from .managers import CustomUserManager
from core.models import Community


class CustomUser(AbstractUser):
  username = models.CharField(
    max_length=30, unique=True,
    help_text=("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
    validators=[MinLengthValidator(limit_value=3, message="Username can't be smaller then 3 chars.")],
    error_messages={
    "max_length": "Username can't be bigger then 30 chars.",
    "unique": "User with that username already exists.",
  })
  email = models.EmailField(
    max_length=64, unique=True, validators=[validate_not_all_numbers],
    help_text='Your email will be used to activate the account and for password resets. So it has to be legit.',
    error_messages={
    'unique': 'User with this email already exists.',
    'max_length': 'Email address can\'t be more then 64 chars.',
  })
  slug = AutoSlugField(populate_from='username', null=True, editable=False)
  date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined', editable=False)
  followers = models.ManyToManyField(to="self", symmetrical=False, blank=True)
  following_communities = models.ManyToManyField(to=Community, related_name='followed_communities', blank=True)
  avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
  bio = models.TextField(max_length=500, blank=True, default='')
  x_link = models.URLField(max_length=350, blank=True, default="",)
  website_link = models.URLField(max_length=350, blank=True, default="",)
  newsletter_link = models.URLField(max_length=350, blank=True, default="",)
  yt_link = models.URLField(max_length=350, blank=True, default="",)
  github_link = models.URLField(max_length=350, blank=True, default="",)
  objects = CustomUserManager()
  USERNAME_FIELD = "email"
  EMAIL_FIELD = "email"
  REQUIRED_FIELDS = ["username"]

  class Meta:
    db_table = 'users'
    verbose_name = 'user'
    verbose_name_plural = 'users'
    unique_together = ('username', 'email')
  
  def __str__(self):
    return self.username


class DeletedUser(models.Model):

  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(unique=True)
  deleted_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'deleted_users'
    verbose_name = 'deleted user'
    verbose_name_plural = 'deleted users'

  def __str__(self):
    return self.username


class PasswordChangeLog(models.Model):

  user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(default=timezone.now)

  class Meta:
    db_table = 'password_changes'
    verbose_name = "password change"
    verbose_name_plural = "password changes"

  def __str__(self):
    return f"{self.user.username} - {self.timestamp}"