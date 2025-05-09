import re
from django import forms
from tinymce.widgets import TinyMCE
from django.core.exceptions import ValidationError
from validators.account_validators import OffensiveWordsValidator, BlacklistDomainsValidator
from .models import Comment


class CommentModelForm(forms.ModelForm):

  content = forms.CharField(
    label="", validators = [OffensiveWordsValidator(), BlacklistDomainsValidator(),],
    widget=TinyMCE(mce_attrs={
    "menubar": False,
    "branding": False,
    "resize": 'both',
    "content_style": 'body { font-family: "Manrope", sans-serif; font-weight: 500; font-size: 1.3rem; padding-left: 2rem; padding-right: 2rem; }',
    "content_css": "writer",
    "paste_as_text": False,
    "width": "100%",
    "height": "450px",
    "plugins": "fullscreen save link lists codesample emoticons",
    "toolbar": "undo redo | backcolor | emoticons | codesample | bullist | link | bold | underline | fullscreen",
    "color_map": ['rgb(251, 238, 184)', 'Yellow',],
    "visual": False,
    "custom_colors": False,
    "link_title": False,
    "link_default_target": '_blank',
    "link_default_protocol": 'https',
    "link_target_list": False,
    "link_assume_external_targets": "https",
  }))

  def clean_content(self):
    content = self.cleaned_data['content']
    content = re.sub(r'<(sup|sub|script|button|form|select|textarea|canvas|menu|nav|header|footer|section|aside|audio)[^>]*>.*?</\1>', '', content, flags=re.DOTALL)
    content = re.sub(r'\sclass="((?!language-)[^"]*)"', '', content)
    content = re.sub(r'\s(data-testid|aria-labelledby|aria-label|aria-hidden|aria-level|srcset|sizes|data-selectable-paragraph|dir|style|utm_campaign|rel)="[^"]*"', '', content)
    content = re.sub(r'<div[^>]*>\s*(?:&nbsp;|&#160;|\u00A0)\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'\sid="[^"]*"', '', content)
    content = re.sub(r'\sdata-[^=]*="[^"]*"', '', content)
    if len(content) > 10000:
      msg = f'Limit is 10000 characters.'
      raise ValidationError(msg)
    if content is None:
      raise ValidationError('Hey there! You forgot to add some content. Please fill it in.')
    return content

  class Meta:
    model = Comment
    fields = ('content',)