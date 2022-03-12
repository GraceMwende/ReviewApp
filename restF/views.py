from django.shortcuts import render
from .models import Project,Profile
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
  projects = Project.display_projects()
  return render(request,'home.html',{'projects':projects})

def search_results(request):
  if 'project' in request.GET and request.GET['project']:
    search_term = request.GET.get('project')
    searched_projects = Project.search_by_title(search_term)
    message = f'{search_term}'  

    return render(request,'search.html',{'messages':message,'projects':searched_projects})

  else:
    message="You haven't searched for any item"
    return render(request,'search.html',{'messages':message})
    
@login_required(login_url='/accounts/login/')
def project(request,project_id):
  try:
    project = Project.objects.get(id=project_id)
  except ObjectDoesNotExist:
    raise Http404()
  return render(request,'project.html',{'project':project})
  redirect('/')