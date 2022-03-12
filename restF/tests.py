from django.test import TestCase
from .models import Profile,Project
# Create your tests here.

class ProjectTestClass(TestCase):
  # setup method
  def setUp(self):
    self.git = Project(project_title='gitsearch',project_link='https://ss')

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