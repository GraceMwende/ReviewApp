from django.shortcuts import render
from .models import Project,Profile

# Create your views here.
def home(request):
  projects = Project.display_projects()
  return render(request,'home.html',{'projects':projects})