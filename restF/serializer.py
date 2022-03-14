from rest_framework import serializers
from .models import Profile,Project

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ('id','project_title','project_image','project_description','project_link','user')

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('id','profile_image','bio','project','phone_number','user')