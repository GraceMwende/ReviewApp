from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Project(models.Model):
  project_title = models.CharField(max_length=200)
  project_image = models.ImageField(upload_to='projects/',null=True)
  project_description = HTMLField()
  project_link = models.CharField(max_length=200)

  def __str__(self):
    return self.project_title

class Profile(models.Model):
  profile_image = models.ImageField(upload_to='profiles/',null=True)
  bio = models.TextField()
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  contact_info = models.EmailField()

  def __str__(self):
    return self.contact_info