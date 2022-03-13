from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
  project_title = models.CharField(max_length=200)
  project_image = models.ImageField(upload_to='projects/',null=True)
  project_description = HTMLField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  project_link = models.CharField(max_length=200)

  def __str__(self):
    return self.project_title

  def save_project(self):
    self.save()

  def delete_project(self):
    self.delete()

  @classmethod
  def display_projects(cls):
    projects = cls.objects.all()
    return projects

  @classmethod
  def search_by_title(cls,searchterm):
    project = cls.objects.filter(project_title__icontains=searchterm)
    return project

class Profile(models.Model):
  profile_image = models.ImageField(upload_to='profiles/',null=True)
  bio = models.TextField()
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  email = models.EmailField()
  phone_number = models.CharField(max_length=10,blank=True)

  def __str__(self):
    return self.email

  @classmethod
  def filter_by_profile(cls,proj):
    project_filter = cls.objects.filter(id=proj).first()
    project_by_profile = cls.objects.filter(project = project_filter).all()
    return project_by_profile