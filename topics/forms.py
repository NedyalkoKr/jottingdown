from django import forms
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