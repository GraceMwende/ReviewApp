from django.test import TestCase
from .models import Profile,Project
# Create your tests here.

class ProjectTestClass(TestCase):
  # setup method
  def setUp(self):
    self.git = Project(project_title='gitsearch',project_link='https://ss')

  # teardown
  def tearDown(self):
    Project.objects.all().delete()
    
  # Testing instance
  def test_instance(self):
    self.assertTrue(isinstance(self.git,Project))
  
  # Testing saving method
  def test_save_method(self):
    self.git.save_project()
    projects = Project.objects.all()
    self.assertTrue(len(projects)>0)

  # Test delete method
  def test_delete_method(self):
    self.git.save_project()
    self.git.delete_project()
    projects = Project.objects.all()
    self.assertTrue(len(projects)==0)

  # test display projects
  def test_display_projects(self):
    self.git.save_project()
    project = Project.display_projects()
    self.assertTrue(len(project)>0)

class ProfileTestClass(TestCase):
  # setup method
  def setUp(self):
    # create a new project and save
    self.git = Project(project_title='gitsearch',project_link='https://ss')
    self.git.save_project()

    self.grace = Profile(bio='software dev',project=self.git, email='grace@gmail.com',phone_number='0702081966')

  # delete after each test
  def tearDown(self):
    Project.objects.all().delete()
    Profile.objects.all().delete()

  def test_get_project_per_profile(self):
    profile_project = Profile.filter_by_profile()
    self.assertTrue(leb(profile_project)==0)