from .models import Project
from django import forms

class NewProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['user']