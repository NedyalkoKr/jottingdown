from django import forms
from django.core.exceptions import ValidationError
from .models import SavedSearch


class NewSavedSearchModelForm(forms.ModelForm):
  class Meta:
    model = SavedSearch
    fields = ('name',)


class NewSavedSearchFromKeywordModelForm(forms.ModelForm):

  class Meta:
    model = SavedSearch
    fields = ('name',)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["name"].required = True
    self.fields["name"].help_text = "Choose which keyword or phrase you'd like to use as search query. It has to be from the text." 
  
  def clean_content(self):  
    name = self.cleaned_data['name']
    if len(name) >= 100:
      raise ValidationError(f'Name is too long. It must be less than or 101 characters.')
    return name
