from .models import Project,Profile,Review
from django import forms
from django.contrib.auth.models import User

class NewProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['user','profile']

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields= ('username','first_name','last_name','email')

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('bio','profile_image','phone_number')
  
class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = ('rating',)

  