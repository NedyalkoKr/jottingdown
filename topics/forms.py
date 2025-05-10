import re
from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from validators.account_validators import OffensiveWordsValidator, BlacklistDomainsValidator
from .models import Topic


class TopicModelForm(forms.ModelForm):

  content = forms.CharField(
    label="", help_text="", required=True,
    validators=[OffensiveWordsValidator(), BlacklistDomainsValidator()],
    widget=TinyMCE(mce_attrs={
      "menubar": False,
      "branding": False,
      "browser_spellcheck": True,
      "plugins": "fullscreen save link lists media codesample code",
      "toolbar": "backcolor | link | bold | underline | bullist numlist | codesample code | media | fullscreen",
      "width": "100%",
      "height": "460px",
      "link_title": False,
      "link_default_target": '_blank',
      "link_default_protocol": 'https',
      "link_target_list": False,
      "link_assume_external_targets": "https",
      # Add these for multiple uploads
      "file_picker_types": "image",
      "automatic_uploads": True,
      "media_alt_source": False,
      "media_poster": False,
      "media_dimensions": True,
      "images_upload_url": "/upload_image/",
      "content_css": "https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap",
      "content_style": "body { font-family: 'Manrope', sans-serif; font-size: 17px; padding: 20px 40px; max-width: 800px; margin: 0 auto; line-height: 1.7;}",
    }),
  )

  class Meta:
    model = Topic
    fields = ('title', 'content',)
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def clean_content(self):
    content = self.cleaned_data['content']
    content = re.sub(r'\u003c(sup|sub|script|button|form|select|textarea|canvas|menu|nav|header|footer|section|aside|audio)[^\u003e]*\u003e.*?\u003c/\\1\u003e', '', content, flags=re.DOTALL)
    content = re.sub(r'\\sclass="((?!language-)[\\"]*)"', '', content)
    content = re.sub(r'\\s(data-testid|aria-labelledby|aria-hidden|aria-level|srcset|sizes|data-selectable-paragraph|dir|style|utm_campaign|rel)="[\\"]*"', '', content)
    content = re.sub(r'\\sid="[\\"]*"', '', content)
    content = re.sub(r'\\sdata-[^=]*="[\\"]*"', '', content)
    content = re.sub(r'<div[^>]*>\s*(?:&nbsp;|&#160;|\u00A0)\s*</div>', '', content, flags=re.DOTALL)
    if len(content) > 20000:
      msg = f'Post is too big.'
      raise ValidationError(msg)
    return content

  def clean_title(self):
    title = self.cleaned_data['title']
    if len(title) > 120:
      raise forms.ValidationError("Title is too long.")
    return title


class NewMediaTopicModelForm(forms.ModelForm):

  class Meta:
    model = Topic
    fields = ('title', 'image', 'content',)