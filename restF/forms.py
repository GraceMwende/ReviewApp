from .models import Project,Profile
from django import forms
from django.contrib.auth.models import User

class NewProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['user']

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields= ('username','first_name','last_name','email')

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('bio','profile_image','phone_number')