from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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
  project = models.ForeignKey(Project, on_delete=models.CASCADE,default=1)
  # projects = models.ManyToManyField(Project)
  # email = models.EmailField()
  phone_number = models.CharField(max_length=10,blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE,default=2)

  def __str__(self):
    return self.user.username 

  @receiver(post_save, sender=User)
  def create_user_profile(sender,instance,created,**kwargs):
    if created:
      profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender,instance,**kwargs):
    instance.profile

  @classmethod
  def filter_by_profile(cls,proj):
    project_filter = cls.objects.filter(id=proj).first()
    project_by_profile = cls.objects.filter(project = project_filter).all()
    return project_by_profile

# Rate_CHOICES = (
#     ('1','1'),
#     ('2', '2'),
#     ('3','3'),
#     ('4','4'),
#     ('5','5'),
#     ('6','6'),
#     ('7','7'),
#     ('8','8'),
#     ('9','9'),
#     ('10','10'),
# )

class Review(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.FloatField(default=0)

  def __str__(self):
    return self.user.username
