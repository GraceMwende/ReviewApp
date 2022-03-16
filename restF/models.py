from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
  profile_image = models.ImageField(upload_to='profiles/',null=True)
  bio = models.TextField(default='test')
  # project = models.ForeignKey(Project, on_delete=models.CASCADE)
  # projects = models.ManyToManyField(Project)
  # email = models.EmailField()
  phone_number = models.CharField(max_length=10,blank=True,default='0711287999')
  user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')

  def __str__(self):
    return self.user.username 

  @receiver(post_save, sender=User)
  def create_user_profile(sender,instance,created,**kwargs):
    if created:
      Profile.objects.create(user=instance)

  @receiver(post_save, sender=User,dispatch_uid='save_new_user_profile')
  def save_user_profile(sender,instance,created,**kwargs):
    user = instance
    if created:
        # profile = UserProfile(user=user)
        # profile.save()
      instance.profile.save()

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

# Create your models here.
class Project(models.Model):
  project_title = models.CharField(max_length=200)
  project_image = models.ImageField(upload_to='projects/',null=True)
  project_description = HTMLField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  project_link = models.CharField(max_length=200)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='project')

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


class Review(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='review')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.FloatField(default=0)

  def __str__(self):
    return self.user.username
